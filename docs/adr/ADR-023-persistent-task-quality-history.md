# ADR-023 — Histórico persistente de qualidade por tarefa/provider/modelo

- **Status:** Accepted — foundation
- **Data:** 2026-09-12

## Contexto

A NEXORA já possui `AvaliadorResultado`, capaz de produzir um sinal explícito de qualidade baseado em critérios e evidências reais. O próximo passo necessário para evolução do roteamento é preservar esse sinal por contexto operacional, sem misturar modelos ou tipos de tarefa.

## Decisão

1. Criar `HistoricoAvaliacao` como componente separado do histórico operacional de chamadas.
2. A chave lógica do histórico é `provider + modelo + tipo_tarefa`.
3. Cada registro acumula somente:
   - quantidade de avaliações;
   - quantidade de sucessos;
   - soma dos scores observados.
4. O histórico é opcionalmente persistido em JSON versionado por `NEXORA_EVALUATION_HISTORY_PATH` ou caminho explícito.
5. Escrita é atômica (`arquivo temporário + os.replace`).
6. Dados inválidos são ignorados com segurança no carregamento.
7. `tipo_tarefa` pode ser declarado explicitamente na `Tarefa`; sem declaração, o Orchestrator mantém uma classificação determinística mínima (`coding` ou `general`).
8. A avaliação é registrada pelo Orchestrator após o AgentRuntime produzir o resultado avaliado.
9. O histórico **não influencia o roteamento nesta etapa**.
10. Qualidade só poderá entrar no score do roteador depois de histórico suficiente, critérios estáveis e testes específicos contra mistura de contexto.
11. Nenhuma métrica de qualidade é estimada quando não existe avaliação real.

## Fluxo

```text
Tarefa
  ↓
AgentRuntime
  ↓
Verification
  ↓
Evaluation (quando configurada)
  ↓
Orchestrator
  ↓
HistoricoAvaliacao(provider, modelo, tipo_tarefa)
  ↓
Persistência opcional
```

## Limites

- Não há avaliação semântica automática por padrão.
- O histórico não é distribuído.
- Não existe ainda janela temporal, decaimento ou detecção de mudança de distribuição.
- O roteador ainda não usa qualidade como sinal de decisão.
- Não se deve interpretar `score_medio` como verdade universal fora do tipo de tarefa e do par provider/modelo correspondente.

## Próximo passo

Definir e testar o limiar mínimo de amostra para qualidade e, somente depois, integrar `qualidade + confiabilidade + latência + tokens + custo` ao score de roteamento sem misturar `provider/modelo/tipo_tarefa`.
