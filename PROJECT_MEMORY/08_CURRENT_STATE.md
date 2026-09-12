# 08 — ESTADO ATUAL

> Estado operacional do repositório e ponto de continuidade. A fonte de verdade é a convergência entre Git, testes, arquitetura e PROJECT_MEMORY.

## Versão / HEAD atual
- Release histórica: `v1.0.0`, tag apontando para `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- HEAD atual do `main`: `a608056d700519f2f62447f23c1148bd621c4be2`.
- O `main` continua evoluindo após `v1.0.0`; a versão de pacote permanece `1.0.0`.
- O último CI do HEAD anterior de código `d69e7c9947dfc79fdd51f28dae66e97a0d3e75f4` foi validado pelo Run #147 (`34659962617`) com sucesso em Python 3.11, 3.12, 3.13 e 3.14.
- O commit atual `a608056...` contém apenas correção de warnings de regex nos testes do Policy Loader; deve ser validado pelo CI próprio deste HEAD antes de qualquer novo código.

## Estado arquitetural real
A Fase 16 — Long-Term Autonomy continua concluída e preservada. Depois dela, a arquitetura evoluiu com Context, Knowledge, World Model, Objetivos, Strategy, infraestrutura multi-agente, comunicação, delegação, runtime, recuperação, experiência, auditoria e governança.

### Componentes pós-v1.0.0 verificados
- Context, Knowledge, World Model, Goal e Strategy Engines.
- `src/nexora/comunicacao/bus.py` — CommunicationBus.
- `src/nexora/comunicacao/delegacao.py` — Delegacao, DelegadorAgentes e ExecutorDelegacoes.
- `src/nexora/agentes/registro.py` — Agent Registry e descoberta por capacidade.
- `src/nexora/runtime/agente.py` — runtime generalista com EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR.
- `src/nexora/runtime/observacao.py` — contrato de observação usado pelo ciclo de agentes.
- `src/nexora/runtime/analise.py` — AnalisadorFalhas existente; os agentes especializados atuais fazem a ponte do erro de verificação para `Observacao.erro` e, quando necessário, classificam a falha como retentável.
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
O fluxo de ferramenta validado é:

`Pedido → Permission → Policy → Checkpoint → Tool → Observation → Verification → Audit → Result`

A integração com Orchestrator está validada para tarefas que possuem `ferramenta`:

`Goal/Plan/Task → Orchestrator → Registry → Permission/Policy → Checkpoint → Tool → Observation → Verification → Audit → Result → Orchestrator`

Regras preservadas:
- autorização ocorre antes da ação;
- DENY impede a execução;
- `DENEGADA` é semanticamente diferente de `FALHOU`;
- checkpoint ocorre imediatamente antes da ferramenta e somente depois da autorização;
- a ferramenta continua sendo o executor da ação;
- observação/verificação/auditoria são opcionais para manter compatibilidade;
- quando observação/verificação estão configuradas, o Registry produz `ResultadoFerramenta`;
- parâmetros e resultado bruto não são copiados para a auditoria do Registry;
- tarefas sem ferramenta continuam usando o caminho Provider existente.

## Runtime dos agentes — estado da reconciliação
Foi encontrada e corrigida a incompatibilidade arquitetural mais imediata do runtime: `AgenteRuntime` produz observações estruturadas como `Observacao`, permitindo que `AnalisadorFalhas` leia `Observacao.erro`.

As correções recentes em agentes especializados foram:
- Coding Agent: passa `Observacao` ao analisador, registra o último erro de validação e força falhas de validação a permanecerem retentáveis neste agente.
- Research Agent: mesma ponte de observação/erro e tratamento de falhas de validação como retentáveis.

Essas correções preservam o runtime generalista e evitam que uma falha de validação de saída seja tratada imediatamente como irreversível pelo agente especializado.

O próximo problema arquitetural ainda aberto é a existência de dois caminhos de execução:
1. `Orquestrador → ExecutorCiclo → Verificador`; e
2. `AgenteRuntime → EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR`.

O caminho de ferramenta já passa pelo Registry e sua governança, mas ainda não foi feita a integração final do Orchestrator com o `AgenteRuntime`. Essa integração deve ser projetada para eliminar duplicação de execução/verificação sem quebrar contratos legados.

## Long-Term Autonomy
- `src/nexora/autonomia/registro.py` permanece preservado.
- `MetaLongoPrazo` e `RegistroAutonomia` continuam responsáveis por metas de longo prazo e persistência JSONL append-only.
- CLI `nexora autonomia definir|atualizar|listar|resumir` permanece parte do sistema.
- Nenhuma alteração recente removeu, substituiu ou enfraqueceu essa camada.

## Testes / CI
- O CI Run #147 (`34659962617`) executou a suíte completa no HEAD `d69e7c9947dfc79fdd51f28dae66e97a0d3e75f4`.
- Python 3.11: SUCCESS.
- Python 3.12: SUCCESS.
- Python 3.13: SUCCESS.
- Python 3.14: SUCCESS.
- A suíte registrou **232 passed, 2 warnings** no Run #147.
- Os dois warnings eram `SyntaxWarning` por escapes em expressões regulares nos testes de `test_policy_loader.py`; o commit `a608056d700519f2f62447f23c1148bd621c4be2` os corrigiu usando regex raw strings.
- Após `a608056...`, o CI ainda deve ser verificado antes de considerar este checkpoint documental final.
- Testes relevantes: `test_runtime_agente.py`, `test_runtime_analise.py`, `test_runtime_correcao.py`, `test_agentes_coding.py`, `test_agentes_pesquisa.py`, `test_tools_registry.py`, `test_checkpoint.py`, `test_permissoes.py`, `test_policy.py`, `test_policy_loader.py`, `test_policy_manager.py`, `test_sandbox_governanca.py` e `test_orquestrador_ferramentas.py`.

## Limites atuais verificados
- Checkpoints ainda não possuem persistência durável.
- Não existe rollback de efeitos externos.
- Registry/capabilities continuam em memória.
- `ExecutorDelegacoes` é síncrono/in-memory.
- YAML de políticas ainda não foi implementado.
- O ciclo autônomo completo de planejamento multi-agente, economia e evolução ainda não está fechado.
- Orchestrator ainda não usa `AgenteRuntime` como executor/verificador único.
- `core/ciclo.py` continua como caminho legado; sua anotação de callable deve ser revisada quando esse limite for reconciliado, sem alterar comportamento sem testes.

## Estado de fase
**Reconciliação do Runtime concluída no nível de consistência interna; integração Orchestrator ↔ Agent Runtime permanece como próximo trabalho arquitetural, não como fase nova.**

Não criar nova fase automaticamente.
