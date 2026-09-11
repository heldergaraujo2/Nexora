"""Delegacao e execucao explicita de tarefas entre agentes."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable
import uuid

from ..agentes.registro import RegistroAgentes
from ..auditoria.registro import RegistroAuditoria
from ..experiencia.registro import RegistroExperiencias
from ..governanca.policy import PolicyEngine
from .bus import CommunicationBus, MensagemAgente


class EstadoDelegacao(str, Enum):
    SOLICITADA = "solicitada"
    ACEITA = "aceita"
    CONCLUIDA = "concluida"
    FALHOU = "falhou"
    CANCELADA = "cancelada"


@dataclass
class Delegacao:
    solicitante: str
    executor: str
    tarefa: str
    prioridade: float = 0.5
    contexto: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    estado: EstadoDelegacao = EstadoDelegacao.SOLICITADA
    resultado: Any = None
    erro: str | None = None
    mensagem_id: str | None = None
    tentativas: int = 0

    def __post_init__(self) -> None:
        if not self.solicitante.strip() or not self.executor.strip():
            raise ValueError("solicitante e executor sao obrigatorios")
        if not self.tarefa.strip():
            raise ValueError("tarefa deve ser uma string nao vazia")
        if not 0 <= self.prioridade <= 1:
            raise ValueError("prioridade deve estar entre 0 e 1")

    def para_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "solicitante": self.solicitante,
            "executor": self.executor,
            "tarefa": self.tarefa,
            "prioridade": self.prioridade,
            "contexto": dict(self.contexto),
            "estado": self.estado.value,
            "resultado": self.resultado,
            "erro": self.erro,
            "mensagem_id": self.mensagem_id,
            "tentativas": self.tentativas,
        }


class DelegadorAgentes:
    """Coordena o contrato de delegacao sem executar a tarefa delegada."""

    def __init__(self, bus: CommunicationBus, registro: RegistroAgentes | None = None) -> None:
        self.bus = bus
        self.registro = registro
        self._delegacoes: dict[str, Delegacao] = {}

    def delegar(
        self,
        *,
        solicitante: str,
        executor: str,
        tarefa: str,
        prioridade: float = 0.5,
        contexto: dict[str, Any] | None = None,
    ) -> Delegacao:
        delegacao = Delegacao(
            solicitante=solicitante,
            executor=executor,
            tarefa=tarefa,
            prioridade=prioridade,
            contexto={} if contexto is None else contexto,
        )
        self._delegacoes[delegacao.id] = delegacao
        mensagem = MensagemAgente(
            remetente=solicitante,
            destinatario=executor,
            tipo="delegacao.solicitada",
            payload=delegacao.para_dict(),
            correlacao_id=delegacao.id,
        )
        delegacao.mensagem_id = mensagem.id
        try:
            self.bus.enviar(mensagem)
        except Exception:
            self._delegacoes.pop(delegacao.id, None)
            raise
        return delegacao

    def delegar_por_capacidade(
        self,
        *,
        solicitante: str,
        capacidade: str,
        tarefa: str,
        prioridade: float = 0.5,
        contexto: dict[str, Any] | None = None,
    ) -> Delegacao:
        """Seleciona automaticamente o agente disponivel mais bem classificado."""
        if self.registro is None:
            raise RuntimeError("registro de agentes nao configurado")
        agente = self.registro.melhor_para(capacidade)
        if agente is None:
            raise LookupError(f"nenhum agente disponivel para a capacidade: {capacidade}")
        contexto_final = {} if contexto is None else dict(contexto)
        contexto_final.setdefault("capacidade_solicitada", capacidade)
        return self.delegar(
            solicitante=solicitante,
            executor=agente.id,
            tarefa=tarefa,
            prioridade=prioridade,
            contexto=contexto_final,
        )

    def atualizar(
        self,
        delegacao_id: str,
        *,
        estado: EstadoDelegacao,
        resultado: Any = None,
        erro: str | None = None,
    ) -> Delegacao:
        delegacao = self._delegacoes.get(delegacao_id)
        if delegacao is None:
            raise KeyError(delegacao_id)
        delegacao.estado = estado
        delegacao.resultado = resultado
        delegacao.erro = erro
        tipo = (
            "delegacao.resultado"
            if estado in {EstadoDelegacao.CONCLUIDA, EstadoDelegacao.FALHOU, EstadoDelegacao.CANCELADA}
            else "delegacao.estado"
        )
        self.bus.publicar(
            remetente=delegacao.executor,
            destinatario=delegacao.solicitante,
            tipo=tipo,
            payload=delegacao.para_dict(),
            correlacao_id=delegacao.id,
            resposta_a=delegacao.mensagem_id,
        )
        return delegacao

    def obter(self, delegacao_id: str) -> Delegacao | None:
        return self._delegacoes.get(delegacao_id)

    def listar(self, *, solicitante: str | None = None, executor: str | None = None) -> list[Delegacao]:
        itens = list(self._delegacoes.values())
        if solicitante is not None:
            itens = [item for item in itens if item.solicitante == solicitante]
        if executor is not None:
            itens = [item for item in itens if item.executor == executor]
        return itens


class ExecutorDelegacoes:
    """Liga mensagens de delegacao a handlers explicitamente registrados."""

    def __init__(
        self,
        bus: CommunicationBus,
        delegador: DelegadorAgentes,
        *,
        max_tentativas: int = 1,
        experiencias: RegistroExperiencias | None = None,
        auditoria: RegistroAuditoria | None = None,
        policy: PolicyEngine | None = None,
    ) -> None:
        if max_tentativas < 1:
            raise ValueError("max_tentativas deve ser maior ou igual a 1")
        self.bus = bus
        self.delegador = delegador
        self.max_tentativas = max_tentativas
        self.experiencias = experiencias
        self.auditoria = auditoria
        self.policy = policy
        self._handlers: dict[str, Callable[[Delegacao], Any]] = {}
        self._inscrito = False

    def registrar(self, agent_id: str, handler: Callable[[Delegacao], Any]) -> None:
        if not agent_id.strip():
            raise ValueError("agent_id deve ser uma string nao vazia")
        self._handlers[agent_id] = handler
        if not self._inscrito:
            self.bus.assinar("*", self._receber)
            self._inscrito = True

    def registrar_runtime(self, agent_id: str, runtime: Any) -> None:
        """Registra um AgenteRuntime como executor da delegacao."""
        if not hasattr(runtime, "executar") or not callable(runtime.executar):
            raise TypeError("runtime deve expor um metodo executar(objetivo)")

        def executar_runtime(delegacao: Delegacao) -> Any:
            return runtime.executar(delegacao.tarefa)

        self.registrar(agent_id, executar_runtime)

    def _auditar(self, evento: str, delegacao: Delegacao, dados_extra: dict[str, Any] | None = None) -> None:
        if self.auditoria is None:
            return
        dados = {
            "solicitante": delegacao.solicitante,
            "executor": delegacao.executor,
            "tarefa": delegacao.tarefa,
            "estado": delegacao.estado.value,
            "tentativas": delegacao.tentativas,
            "erro": delegacao.erro,
        }
        if dados_extra:
            dados.update(dados_extra)
        self.auditoria.registrar(
            evento,
            entidade="delegacao",
            entidade_id=delegacao.id,
            dados=dados,
        )

    def _registrar_experiencia(self, delegacao: Delegacao) -> None:
        if self.experiencias is None:
            return
        self.experiencias.registrar(
            "delegacao",
            delegacao.estado is EstadoDelegacao.CONCLUIDA,
            metadados={
                "delegacao_id": delegacao.id,
                "solicitante": delegacao.solicitante,
                "executor": delegacao.executor,
                "tarefa": delegacao.tarefa,
                "estado": delegacao.estado.value,
                "tentativas": delegacao.tentativas,
                "erro": delegacao.erro,
            },
        )

    def _receber(self, mensagem: MensagemAgente) -> None:
        if mensagem.tipo != "delegacao.solicitada":
            return
        handler = self._handlers.get(mensagem.destinatario)
        if handler is None:
            return
        delegacao_id = mensagem.correlacao_id
        if delegacao_id is None:
            return
        delegacao = self.delegador.obter(delegacao_id)
        if delegacao is None or delegacao.estado is not EstadoDelegacao.SOLICITADA:
            return

        if self.policy is not None:
            decisao = self.policy.autorizar(delegacao)
            self._auditar(
                "politica.decisao",
                delegacao,
                {
                    "efeito": decisao.efeito.value,
                    "permitido": decisao.permitido,
                    "motivo": decisao.motivo,
                    "regra_id": decisao.regra_id,
                    "versao": decisao.versao,
                    "origem": decisao.origem,
                },
            )
            if not decisao.permitido:
                self.delegador.atualizar(
                    delegacao_id,
                    estado=EstadoDelegacao.FALHOU,
                    erro=f"execucao negada pela politica: {decisao.motivo}",
                )
                self._auditar("delegacao.falhou", delegacao)
                self._registrar_experiencia(delegacao)
                return

        self.delegador.atualizar(delegacao_id, estado=EstadoDelegacao.ACEITA)
        self._auditar("delegacao.aceita", delegacao)
        while delegacao.tentativas < self.max_tentativas:
            delegacao.tentativas += 1
            try:
                resultado = handler(delegacao)
            except Exception as exc:
                delegacao.erro = str(exc)
                if delegacao.tentativas >= self.max_tentativas:
                    self.delegador.atualizar(delegacao_id, estado=EstadoDelegacao.FALHOU, erro=str(exc))
                    self._auditar("delegacao.falhou", delegacao)
                    self._registrar_experiencia(delegacao)
                    return
                continue
            sucesso = getattr(resultado, "sucesso", True)
            if sucesso:
                self.delegador.atualizar(delegacao_id, estado=EstadoDelegacao.CONCLUIDA, resultado=resultado)
                self._auditar("delegacao.concluida", delegacao)
            else:
                erro = getattr(resultado, "saida_final", "verificacao da tarefa falhou")
                self.delegador.atualizar(delegacao_id, estado=EstadoDelegacao.FALHOU, resultado=resultado, erro=str(erro))
                self._auditar("delegacao.falhou", delegacao)
            self._registrar_experiencia(delegacao)
            return
