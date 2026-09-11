# 08 — ESTADO ATUAL

> Estado operacional do repositório e ponto de continuidade. A fonte de verdade é a convergência entre Git, testes, arquitetura e PROJECT_MEMORY.

## Versão / HEAD atual
- Release histórica: v1.0.0, tag apontando para `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- HEAD atual do `main`: `f67f270c25609559264c19ef7a2561cc359873b8`.
- O `main` continua evoluindo após v1.0.0; a versão de pacote permanece `1.0.0`.
- CI do HEAD atual: **Run #138 (`34658836451`) — SUCCESS**, com Python 3.11, 3.12, 3.13 e 3.14 verdes.

## Estado arquitetural real
A Fase 16 — Long-Term Autonomy continua concluída e preservada. Depois dela, a arquitetura evoluiu com contexto, conhecimento, world model, objetivos, estratégias e infraestrutura multi-agente com comunicação, delegação, execução, verificação, recuperação, experiência, auditoria e governança.

### Componentes pós-v1.0.0 verificados
- Context, Knowledge, World Model, Goal e Strategy Engines.
- `src/nexora/comunicacao/bus.py` — CommunicationBus.
- `src/nexora/comunicacao/delegacao.py` — Delegacao, DelegadorAgentes e ExecutorDelegacoes.
- `src/nexora/agentes/registro.py` — Agent Registry e descoberta por capacidade.
- `src/nexora/runtime/agente.py` — ciclo de execução/verificação/análise/correção/reteste.
- `src/nexora/orquestracao/orquestrador.py` — orquestração e roteamento opcional de tarefas com ferramenta.
- `src/nexora/experiencia/registro.py` — experiências de resultados terminais.
- `src/nexora/auditoria/registro.py` — auditoria append-only em JSONL.
- `src/nexora/governanca/policy.py` — PolicyEngine ALLOW/DENY.
- `src/nexora/governanca/policy_loader.py` — loader TOML versionado e estrito.
- `src/nexora/governanca/permissoes.py` — fronteira explícita de autorização.
- `src/nexora/governanca/policy_manager.py` — reload validado e troca atômica.
- `src/nexora/tools/registry.py` — execução de ferramentas governada, com checkpoint, observação, verificação e auditoria opcional.
- `src/nexora/runtime/sandbox.py` — allowlist + Policy opcional antes de subprocesso.
- `src/nexora/runtime/checkpoint.py` — CheckpointEngine para snapshots lógicos em memória.
- `src/nexora/runtime/ferramenta.py` — contrato `ResultadoFerramenta` para consolidar resultado observado/verificado.

## Fluxo arquitetural
`Goal/Plan/Task → Orchestrator → Registry → Permission/Policy → Checkpoint → Tool → Observation → Verification → Audit → Result → Orchestrator`

No Registry de ferramentas, o fluxo efetivamente implementado é: autorização antes da ação; checkpoint antes da execução; execução da ferramenta; observação/verificação opcionais; auditoria do resultado ou da falha; retorno do resultado bruto quando os estágios de observação/verificação não estão configurados e `ResultadoFerramenta` quando estão configurados.

O Checkpoint Engine atualmente é explícito e desacoplado: captura/recupera estado lógico, mas não executa ferramentas nem desfaz efeitos externos.

A integração Orchestrator → Registry é opcional e preserva o caminho existente de Provider para tarefas sem ferramenta. O teste integrado valida o caminho completo sem chamar o Provider quando uma ferramenta está configurada.

## Limites atuais verificados
- Checkpoints ainda não possuem persistência durável.
- Não existe rollback de efeitos externos.
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
- `tests/unit/test_tools_registry.py` cobre governança, checkpoint, observação, verificação, auditoria de resultado e auditoria de falha.
- `tests/integration/test_orquestrador_ferramentas.py` valida o fluxo integrado Orchestrator → Tool Registry.
- CI Run #138 (`34658836451`) está verde em Python 3.11–3.14 para o HEAD `f67f270...`.

## Estado de fase
**Fases históricas concluídas + evolução arquitetural pós-release em reconciliação.**

Não iniciar um novo componente/fase automaticamente.
