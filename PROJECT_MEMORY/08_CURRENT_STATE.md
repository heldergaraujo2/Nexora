# 08 — ESTADO ATUAL

> Estado operacional do repositório e ponto de continuidade. A fonte de verdade é a convergência entre Git, testes, arquitetura e PROJECT_MEMORY. Para o HEAD exato e o último checkpoint validado, consulte sempre `PROJECT_MEMORY/15_HANDOFF.md`.

## Versão / estado
- Release histórica: `v1.0.0`, tag apontando para `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- O `main` continua evoluindo após `v1.0.0`; a versão de pacote permanece `1.0.0`.
- O runtime interno foi reforçado para transformar exceções de execução/verificação em observações controladas.
- O Orquestrador agora usa `AgenteRuntime` como proprietário do ciclo de execução de cada tarefa.

## Estado arquitetural real
A Fase 16 — Long-Term Autonomy continua concluída e preservada. A arquitetura evoluiu com Context, Knowledge, World Model, Objetivos, Strategy, comunicação, delegação, runtime, recuperação, experiência, auditoria e governança.

### Componentes principais verificados
- Context, Knowledge, World Model, Goal e Strategy Engines.
- CommunicationBus, Delegacao e Agent Registry.
- `src/nexora/runtime/agente.py` — runtime generalista `EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR`.
- `src/nexora/runtime/observacao.py` — contrato de observação.
- `src/nexora/runtime/analise.py` — AnalisadorFalhas existente.
- `src/nexora/runtime/correcao.py` — Corrector.
- `src/nexora/runtime/checkpoint.py` — CheckpointEngine para snapshots lógicos em memória.
- `src/nexora/runtime/ferramenta.py` — contrato `ResultadoFerramenta`.
- `src/nexora/orquestracao/orquestrador.py` — coordenação de objetivos/tarefas com AgentRuntime.
- Experience, Audit, Policy, Permission, Tool Registry e Sandbox.

## Reconciliação Orchestrator ↔ AgentRuntime — EM IMPLEMENTAÇÃO
A ADR-012 define o limite arquitetural: Orchestrator coordena; AgentRuntime executa o ciclo avançado. `core/ciclo.py` permanece legado/compatibilidade até migração segura.

Implementado neste checkpoint:
- [x] `Orquestrador` deixou de importar/instanciar `ExecutorCiclo` e `VerificadorCiclo` para execução normal.
- [x] Cada tarefa é encaminhada a uma instância do `AgenteRuntime`.
- [x] Provider continua sendo usado para tarefas sem ferramenta.
- [x] Tarefas com ferramenta continuam atravessando `RegistryFerramentas`.
- [x] Retry implícito de ferramentas foi deliberadamente limitado a uma tentativa nesta primeira integração, evitando repetir efeitos externos sem uma camada explícita de idempotência.
- [x] Resultado do runtime é normalizado para o resultado de tarefa do Orchestrator, preservando tentativas e histórico.
- [x] Exceções de execução/verificação do AgentRuntime viram `Observacao` e podem ser analisadas pelo fluxo de falha, em vez de escaparem diretamente.
- [x] Testes de integração adicionados para sucesso após retry de provider e para falha de provider sem exceção escapar do Orchestrator.

## Governança de execução
Fluxo preservado:

`Pedido → Permission → Policy → Checkpoint → Tool → Observation → Verification → Audit → Result`

O Orchestrator não executa ferramentas diretamente: delega ao Registry existente. A integração com AgentRuntime não contorna Permission/Policy/Checkpoint.

## Long-Term Autonomy
- `src/nexora/autonomia/registro.py` permanece preservado.
- `MetaLongoPrazo` e `RegistroAutonomia` continuam responsáveis por metas de longo prazo e persistência JSONL append-only.
- CLI `nexora autonomia definir|atualizar|listar|resumir` permanece parte do sistema.

## Testes / CI
- O último CI previamente validado foi o Run #157 no HEAD `52ef09f...`.
- Este checkpoint adicionou testes de integração para a nova fronteira Orchestrator ↔ AgentRuntime.
- O novo HEAD deve ser validado pelo CI antes de ser considerado checkpoint de código validado.

## Limites atuais verificados
- `core/ciclo.py` ainda existe como caminho legado e não deve ser removido até consumidores/testes serem migrados.
- Checkpoints não possuem persistência durável.
- Não existe rollback de efeitos externos.
- Retry/idempotência para efeitos externos ainda requer uma camada própria.
- Registry/capabilities continuam em memória.
- ExecutorDelegacoes é síncrono/in-memory.
- YAML de políticas não foi implementado.
- O ciclo autônomo completo de planejamento multi-agente, economia e evolução ainda não está fechado.
- Groq ainda requer validação real da integração HTTP/tool-calling antes de ser tratado como validado em produção.

## Estado de fase
**Reconciliação Orchestrator ↔ AgentRuntime em implementação incremental; não foi criada nova fase.**
