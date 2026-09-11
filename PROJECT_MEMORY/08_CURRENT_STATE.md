# 08 — ESTADO ATUAL

> Estado operacional do repositório e ponto de continuidade. A fonte de verdade é a convergência entre Git, testes, arquitetura e PROJECT_MEMORY.

## Versão / HEAD atual
- Release histórica: v1.0.0, tag apontando para `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- Último HEAD implementado nesta etapa: `5e022a6a2b9d6df031deb17fd4983b8d5860ee90`.
- O `main` continua evoluindo após v1.0.0; a versão de pacote permanece `1.0.0`.
- CI do HEAD atual ainda não foi confirmado.

## Estado arquitetural real
A Fase 16 — Long-Term Autonomy continua concluída e preservada. Depois dela, a arquitetura evoluiu com contexto, conhecimento, world model, objetivos, estratégias e infraestrutura multi-agente com comunicação, delegação, execução, verificação, recuperação, experiência, auditoria e governança.

### Componentes pós-v1.0.0 verificados
- Context, Knowledge, World Model, Goal e Strategy Engines.
- `src/nexora/comunicacao/bus.py` — CommunicationBus.
- `src/nexora/comunicacao/delegacao.py` — Delegacao, DelegadorAgentes e ExecutorDelegacoes.
- `src/nexora/agentes/registro.py` — Agent Registry e descoberta por capacidade.
- `src/nexora/runtime/agente.py` — ciclo de execução/verificação/análise/correção/reteste.
- `src/nexora/orquestracao/orquestrador.py` — orquestração.
- `src/nexora/experiencia/registro.py` — experiências de resultados terminais.
- `src/nexora/auditoria/registro.py` — auditoria append-only em JSONL.
- `src/nexora/governanca/policy.py` — PolicyEngine ALLOW/DENY.
- `src/nexora/governanca/policy_loader.py` — loader TOML versionado e estrito.
- `src/nexora/governanca/permissoes.py` — fronteira explícita de autorização.
- `src/nexora/governanca/policy_manager.py` — reload validado e troca atômica.
- `src/nexora/tools/registry.py` — execução de ferramentas opcionalmente governada.
- `src/nexora/runtime/sandbox.py` — allowlist + Policy opcional antes de subprocesso.
- `src/nexora/runtime/checkpoint.py` — CheckpointEngine para snapshots lógicos em memória.

## Fluxo arquitetural
`Pedido → Permission → Policy → Sandbox/Tool → Checkpoint → Observation → Verification → Audit → Result`

O Checkpoint Engine atualmente é explícito e desacoplado: captura/recupera estado lógico, mas não executa ferramentas nem desfaz efeitos externos.

## Limites atuais verificados
- Checkpoints ainda não possuem persistência durável.
- Não existe rollback de efeitos externos.
- Integração automática Checkpoint ↔ Tool/Sandbox ainda não foi acoplada.
- Registry/capabilities continuam em memória.
- `ExecutorDelegacoes` é síncrono/in-memory.
- Ainda não existe ciclo autônomo completo de planejamento multi-agente, economia e evolução.
- Não foi criada uma nova fase.

## Long-Term Autonomy
- `src/nexora/autonomia/registro.py` permanece preservado.
- `MetaLongoPrazo` e `RegistroAutonomia` continuam responsáveis por metas de longo prazo e persistência JSONL append-only.
- CLI `nexora autonomia definir|atualizar|listar|resumir` permanece parte do sistema.

## Testes / CI
- Testes específicos de Checkpoint estão em `tests/unit/test_checkpoint.py`.
- Cobertura inclui isolamento do snapshot, recuperação sem mutação, filtro por execução, auditoria e validações.
- CI do HEAD atual ainda não confirmado; não marcar como verde sem evidência.

## Estado de fase
**Fases históricas concluídas + evolução arquitetural pós-release em reconciliação.**

Não iniciar um novo componente/fase automaticamente.
