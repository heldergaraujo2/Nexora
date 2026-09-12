# 08 — ESTADO ATUAL

> Estado operacional do repositório e ponto de continuidade. A fonte de verdade é a convergência entre Git, testes, arquitetura e PROJECT_MEMORY. Para o HEAD exato e o último checkpoint validado, consulte sempre `PROJECT_MEMORY/15_HANDOFF.md`.

## Versão / estado
- Release histórica: `v1.0.0`, tag apontando para `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- O `main` continua evoluindo após `v1.0.0`; a versão de pacote permanece `1.0.0`.
- O último checkpoint de código validado nesta etapa foi o commit `d69e7c9947dfc79fdd51f28dae66e97a0d3e75f4`, validado pelo Run #147 (`34659962617`) em Python 3.11, 3.12, 3.13 e 3.14.
- Depois dele foram feitas correções de qualidade e atualizações de continuidade. O `15_HANDOFF.md` é a referência para o HEAD atual.

## Estado arquitetural real
A Fase 16 — Long-Term Autonomy continua concluída e preservada. Depois dela, a arquitetura evoluiu com Context, Knowledge, World Model, Objetivos, Strategy, infraestrutura multi-agente, comunicação, delegação, runtime, recuperação, experiência, auditoria e governança.

### Componentes pós-v1.0.0 verificados
- Context, Knowledge, World Model, Goal e Strategy Engines.
- `src/nexora/comunicacao/bus.py` — CommunicationBus.
- `src/nexora/comunicacao/delegacao.py` — Delegacao, DelegadorAgentes e ExecutorDelegacoes.
- `src/nexora/agentes/registro.py` — Agent Registry e descoberta por capacidade.
- `src/nexora/runtime/agente.py` — runtime generalista com EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR.
- `src/nexora/runtime/observacao.py` — contrato de observação.
- `src/nexora/runtime/analise.py` — AnalisadorFalhas existente.
- `src/nexora/runtime/correcao.py` — Corrector para retry/rerun/troca de provider/ajuste de prompt.
- `src/nexora/runtime/checkpoint.py` — CheckpointEngine para snapshots lógicos em memória.
- `src/nexora/runtime/ferramenta.py` — contrato `ResultadoFerramenta`.
- `src/nexora/orquestracao/orquestrador.py` — orquestração e roteamento opcional de tarefas com ferramenta.
- `src/nexora/experiencia/registro.py` — experiências de resultados terminais.
- `src/nexora/auditoria/registro.py` — auditoria append-only em JSONL.
- `src/nexora/governanca/policy.py` — PolicyEngine ALLOW/DENY, default DENY e fingerprint canônico SHA-256.
- `src/nexora/governanca/policy_loader.py` — loader TOML versão 2, declarativo e estrito.
- `src/nexora/governanca/permissoes.py` — fronteira explícita de autorização.
- `src/nexora/governanca/policy_manager.py` — reload validado e troca atômica.
- `src/nexora/tools/registry.py` — execução de ferramentas governada, com checkpoint, observação, verificação e auditoria opcional.
- `src/nexora/runtime/sandbox.py` — allowlist + Policy opcional antes de subprocesso.

## Governança de execução
Fluxo validado:

`Pedido → Permission → Policy → Checkpoint → Tool → Observation → Verification → Audit → Result`

Integração Orchestrator → Registry validada:

`Goal/Plan/Task → Orchestrator → Registry → Permission/Policy → Checkpoint → Tool → Observation → Verification → Audit → Result → Orchestrator`

Regras preservadas:
- autorização antes da ação;
- DENY impede execução;
- `DENEGADA` é diferente de `FALHOU`;
- checkpoint depois da autorização e antes da ferramenta;
- Registry continua sendo o executor governado da ferramenta;
- observação/verificação/auditoria são opcionais por compatibilidade;
- tarefas sem ferramenta preservam Provider;
- auditoria não copia parâmetros nem resultado bruto potencialmente sensível.

## Runtime dos agentes — etapa fechada
A inconsistência encontrada entre a observação produzida pelo runtime e o formato esperado pelo analisador foi reconciliada sem fundir ainda o Orchestrator ao Runtime.

Coding Agent e Research Agent agora:
- usam `Observacao` no caminho de análise;
- transportam o último erro de validação para `Observacao.erro`;
- tratam falhas de validação corrigíveis como retentáveis no agente especializado;
- continuam usando o `AgenteRuntime` e seu ciclo avançado.

Isso evita que erros como saída vazia, sintaxe inválida ou ausência de citação sejam imediatamente tratados como irreversíveis.

## Long-Term Autonomy
- `src/nexora/autonomia/registro.py` permanece preservado.
- `MetaLongoPrazo` e `RegistroAutonomia` continuam responsáveis por metas de longo prazo e persistência JSONL append-only.
- CLI `nexora autonomia definir|atualizar|listar|resumir` permanece parte do sistema.

## Testes / CI
- Run #147 (`34659962617`) no HEAD `d69e7c9947dfc79fdd51f28dae66e97a0d3e75f4`: **SUCCESS** em Python 3.11, 3.12, 3.13 e 3.14.
- Python 3.14 registrou **232 passed, 2 warnings**.
- Os 2 warnings eram `SyntaxWarning` nos testes de `test_policy_loader.py` por escapes inválidos em regex.
- O commit `a608056d700519f2f62447f23c1148bd621c4be2` corrigiu os warnings com regex raw.
- Os commits posteriores são de documentação/continuidade.
- O próximo agente deve verificar o CI do HEAD atual antes de iniciar código.

Testes relevantes: `test_runtime_agente.py`, `test_runtime_analise.py`, `test_runtime_correcao.py`, `test_agentes_coding.py`, `test_agentes_pesquisa.py`, `test_tools_registry.py`, `test_checkpoint.py`, `test_permissoes.py`, `test_policy.py`, `test_policy_loader.py`, `test_policy_manager.py`, `test_sandbox_governanca.py` e `test_orquestrador_ferramentas.py`.

## Limites atuais verificados
- Checkpoints não possuem persistência durável.
- Não existe rollback de efeitos externos.
- Registry/capabilities continuam em memória.
- `ExecutorDelegacoes` é síncrono/in-memory.
- YAML de políticas não foi implementado.
- O ciclo autônomo completo de planejamento multi-agente, economia e evolução ainda não está fechado.
- Orchestrator ainda não usa `AgenteRuntime` como executor/verificador único.
- `core/ciclo.py` permanece como caminho legado; sua anotação de callable deve ser revisada com testes antes de qualquer mudança comportamental.

## Estado de fase
**Reconciliação interna do Runtime concluída no nível de consistência; integração Orchestrator ↔ Agent Runtime permanece como próximo trabalho arquitetural, não como fase nova.**
