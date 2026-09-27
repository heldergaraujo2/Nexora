# NEXT COMMAND — VERIFICAÇÃO DE QUALIDADE DA EVIDÊNCIA

> Canal de continuidade da coordenação da NEXORA. A release `v1.0.0` continua válida como marco histórico; o código avançou depois dela.

## Estado atual — 2026-09-12

- `AgentRuntime` permanece o único proprietário do ciclo avançado.
- `core/ciclo.py` permanece legado/compatibilidade e não deve ser removido prematuramente.
- Quality Routing foi validado pelo CI em Python 3.11–3.14.
- Research Agent possui contrato estruturado `claim → evidence → source`.
- Evidências preservam título, URL, trecho, consulta e confiança explícita quando disponível.
- Citações para fontes inexistentes não criam evidência.
- `source_id` mantém compatibilidade com `[fonte:N]`.
- `source_ref` é fingerprint SHA-256 determinístico e não representa prova de veracidade.
- Evidências são propagadas para `ResultadoAgente`, métricas e `ExecutionTrace.metadata`.
- Foi implementado `verificacao_evidencia.py` com estados `SUSTENTADA`, `INSUFICIENTE` e `INDETERMINADA`, usando somente sinais lexicais determinísticos.
- A adequação lexical é um sinal de cobertura textual, não uma prova semântica.

## CI

- Run #357 (`34725783075`) — SUCCESS — Python 3.11/3.12/3.13/3.14.
- Os commits de implementação da adequação foram feitos depois desse Run; o CI correspondente ao HEAD atual permanece **PENDENTE** até nova execução terminar.

## Incremento implementado

**Verificação de adequação da evidência.**

Contrato:

```text
Claim
  ↓
Citation
  ↓
Source exists?
  ├── não → sem evidência
  └── sim
       ↓
Evidence adequacy
       ├── sustentada
       ├── insuficiente
       └── indeterminada
```

Implementação:
- `src/nexora/runtime/verificacao_evidencia.py`.
- `AfirmacaoPesquisa` agora inclui `adequacao`.
- ResearchAgent registra contagens de evidências sustentadas, insuficientes e indeterminadas.
- `ExecutionTrace.metadata.research_evidence` recebe o resultado estruturado.
- `confianca` continua `None` sem avaliador real.
- ADR `ADR-027-evidence-adequacy-verification.md`.
- Testes unitários dedicados e testes do ResearchAgent para integração.

## Próximo trabalho obrigatório

**Verificação de qualidade da evidência além de sobreposição lexical.**

Objetivo: evoluir de cobertura textual para sinais adicionais de adequação sem fingir que o sistema já possui compreensão semântica ou prova de verdade.

Restrições:
- qualquer novo sinal deve ser determinístico ou possuir avaliador explicitamente responsável;
- não fabricar confiança;
- preservar compatibilidade;
- testar casos positivos, negativos e ambíguos;
- CI verde antes de marcar o incremento como OK.

## Protocolo

`AUDITAR → DECIDIR → IMPLEMENTAR → TESTAR → ATUALIZAR PROJECT_MEMORY → COMMIT → PUSH → VERIFICAR CI → HANDOFF`

GitHub é a fonte de verdade.
# NEXT COMMAND — ECOSYSTEM INTEGRATION\n\n## Estado atual — 2026-09-27\n\nA auditoria de ecossistema foi implementada como uma camada própria da NEXORA. Consulte `docs/ECOSYSTEM_HARVEST.md`.\n\n### Capacidades adicionadas\n- Memory híbrida / RRF / decay.\n- World Model temporal.\n- RetryPolicy tipado e seguro.\n- Checkpoint persistente opcional.\n- Sandbox backend plugável.\n- MCP contracts + adapter governado.\n- Research budget e source safety.\n- GenAI tracing.\n- EvolutionEngine + DreamCycle.\n- Opportunity Engine + Economic Loop.\n\n### Regra\nNão substituir a NEXORA por frameworks externos. Usar adapters apenas quando uma integração real reduzir custo/risco sem criar duplicação arquitetural.\n\n### Próxima sequência obrigatória\n1. Confirmar HEAD e CI.\n2. Ler `PROJECT_MEMORY/15_HANDOFF.md`.\n3. Auditar Memory/Knowledge/Context existentes antes de integrar `MemoriaHibrida` e `GrafoTemporal`.\n4. Auditar Verification/Tool Registry antes de adicionar outcome verification.\n5. Criar adapters reais opcionais somente após contratos internos estarem estabilizados.\n6. Rodar testes e CI Python 3.11–3.14.\n7. Atualizar Current State/Changelog/Handoff.\n\n### Limites\n- Nenhum framework externo é dependência obrigatória.\n- Docker/OpenSandbox/browser/MCP de rede ainda não estão habilitados por padrão.\n- Sem prova semântica automática.\n- Sem transações financeiras automáticas.\n- Evolution não altera produção sem gate.\n