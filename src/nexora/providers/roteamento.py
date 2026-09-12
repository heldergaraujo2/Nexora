"""Roteamento determinístico entre providers e modelos."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from nexora.providers.manager import ProviderManager
from nexora.providers.modelos import PerfilCapacidadeModelo
from nexora.runtime.hardware import PerfilHardware
from nexora.runtime.modelos import avaliar_modelo


@dataclass(frozen=True)
class CandidatoRoteamento:
    provider: str
    modelo: str
    score: float
    adequado: bool
    motivos: tuple[str, ...] = ()


class RoteadorInteligente:
    """Escolhe provider/modelo sem executar a tarefa."""

    def __init__(self, manager: ProviderManager) -> None:
        self._manager = manager

    def _ajuste_historico(self, provider: str) -> tuple[float, list[str]]:
        """Aplica ajuste pequeno baseado somente em metricas reais medidas.

        Menos de tres chamadas nao produz ajuste: a amostra e insuficiente.
        O historico nunca substitui a adequacao funcional do modelo.
        """
        historico = self._manager.estatisticas_provider(provider)
        chamadas = int(historico["chamadas"])
        if chamadas < 3:
            return 0.0, []

        ajuste = 0.0
        motivos: list[str] = []
        taxa_erro = historico["taxa_erro"]
        taxa_sucesso = historico["taxa_sucesso"]
        latencia = historico["latencia_media"]

        if isinstance(taxa_sucesso, float) and taxa_sucesso >= 0.90:
            ajuste += 1.0
            motivos.append("historico_alta_taxa_sucesso")
        elif isinstance(taxa_erro, float) and taxa_erro >= 0.50:
            ajuste -= 2.0
            motivos.append("historico_alta_taxa_erro")

        if isinstance(latencia, float):
            todas = [
                dados["latencia_media"]
                for dados in self._manager.estatisticas_providers().values()
                if isinstance(dados["latencia_media"], float)
            ]
            media_global = (sum(todas) / len(todas)) if todas else None
            if isinstance(media_global, float) and latencia < media_global:
                ajuste += 0.5
                motivos.append("historico_baixa_latencia")
            elif isinstance(media_global, float) and latencia > media_global:
                ajuste -= 0.5
                motivos.append("historico_alta_latencia")

        return ajuste, motivos

    def _custo_historico_por_milhao(self, provider: str) -> float | None:
        """Retorna custo real observado por milhao de tokens, quando confiavel.

        O valor e calculado somente a partir de custo e tokens medidos pelo
        ProviderManager. Uma amostra de menos de tres geracoes precificadas
        nao influencia o roteamento.
        """
        historico = self._manager.estatisticas_provider(provider)
        geracoes = int(historico.get("geracoes_com_custo", 0))
        tokens = int(historico.get("total_tokens", 0))
        custo = float(historico.get("custo_total", 0.0))
        if geracoes < 3 or tokens <= 0 or custo < 0:
            return None
        return (custo / tokens) * 1_000_000

    def _ajuste_custo_historico(self, provider: str, provedores_candidatos: list[str]) -> tuple[float, list[str]]:
        """Favorece custo historico menor com influencia pequena e limitada."""
        custo = self._custo_historico_por_milhao(provider)
        if custo is None:
            return 0.0, []
        custos = [
            valor
            for nome in provedores_candidatos
            if (valor := self._custo_historico_por_milhao(nome)) is not None
        ]
        if len(custos) < 2:
            return 0.0, []
        media = sum(custos) / len(custos)
        if media <= 0:
            return 0.0, []
        # Limite deliberado: custo nunca vence uma diferenca funcional grande.
        diferenca_relativa = (custo - media) / media
        if diferenca_relativa <= -0.10:
            return 0.75, ["historico_custo_real_mais_baixo"]
        if diferenca_relativa >= 0.10:
            return -0.75, ["historico_custo_real_mais_alto"]
        return 0.0, []

    def selecionar(
        self,
        candidatos: list[dict[str, Any]],
        hardware: PerfilHardware,
        *,
        tarefa: str = "general",
        contexto_necessario: int = 0,
        exigir_tool_calling: bool = False,
        exigir_streaming: bool = False,
        exigir_provider_saudavel: bool = False,
        usar_historico: bool = True,
        considerar_custo: bool = True,
    ) -> list[CandidatoRoteamento]:
        """Ordena candidatos por adequacao, capacidades e historico medido.

        A funcao somente decide. Ela nao executa o provider nem a tarefa.
        Capacidades nao declaradas sao tratadas como ausentes.
        O historico e opcional e tem influencia deliberadamente limitada.
        Custo somente participa quando ha custo e tokens reais suficientes.
        """
        avaliados: list[CandidatoRoteamento] = []
        provedores_candidatos = [
            str(candidato.get("provider", "")).strip().lower()
            for candidato in candidatos
            if str(candidato.get("provider", "")).strip()
        ]
        for candidato in candidatos:
            provider = str(candidato.get("provider", "")).strip().lower()
            modelo = str(candidato.get("modelo", "")).strip()
            perfil = candidato.get("perfil")
            if not provider or not modelo or not isinstance(perfil, PerfilCapacidadeModelo):
                continue
            if provider not in self._manager.nomes():
                continue

            motivos: list[str] = []
            capacidades = self._manager.obter_capacidades(provider)
            adequado = True
            if exigir_tool_calling and not capacidades.tool_calling:
                adequado = False
                motivos.append("provider_sem_tool_calling")
            if exigir_streaming and not capacidades.streaming:
                adequado = False
                motivos.append("provider_sem_streaming")
            if contexto_necessario > capacidades.max_context_tokens > 0:
                adequado = False
                motivos.append("provider_contexto_insuficiente")
            if exigir_provider_saudavel and not self._manager.obter_healthcheck(provider)["saudavel"]:
                adequado = False
                motivos.append("provider_indisponivel")

            avaliacao = avaliar_modelo(
                modelo,
                perfil,
                hardware,
                tarefa=tarefa,
                contexto_necessario=contexto_necessario,
            )
            if not avaliacao.adequado:
                adequado = False
            motivos.extend(avaliacao.motivos)

            score = avaliacao.score if adequado else -100.0
            if adequado and usar_historico:
                ajuste, motivos_historico = self._ajuste_historico(provider)
                score += ajuste
                motivos.extend(motivos_historico)
                if considerar_custo:
                    ajuste_custo, motivos_custo = self._ajuste_custo_historico(provider, provedores_candidatos)
                    score += ajuste_custo
                    motivos.extend(motivos_custo)
            avaliados.append(CandidatoRoteamento(provider, modelo, score, adequado, tuple(motivos)))

        return sorted(avaliados, key=lambda item: (-item.adequado, -item.score, item.provider, item.modelo))
