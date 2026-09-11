# 08 — ESTADO ATUAL

> Estado operacional do repositório e ponto de continuidade. A fonte de verdade é a convergência entre Git, testes, arquitetura e PROJECT_MEMORY.

## Versão / HEAD atual
- Release histórica: v1.0.0, tag apontando para `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- HEAD atual verificado: `68c93b0dc6710fc375fcff237f38737467f245a5`.
- O `main` continua evoluindo após v1.0.0; a versão de pacote permanece `1.0.0`.

## Estado arquitetural real
A Fase 16 — Long-Term Autonomy continua concluída e preservada. Depois dela, a arquitetura evoluiu com contexto, conhecimento, world model, objetivos, estratégias e uma infraestrutura multi-agente com comunicação, delegação, execução, verificação, recuperação, experiência, auditoria e governança.

### Componentes pós-v1.0.0 verificados
- `src/nexora/contexto/engine.py` — `Contexto` e `ContextEngine`.
- `src/nexora/conhecimento/engine.py` — `Conhecimento` e `KnowledgeEngine`.
- `src/nexora/mundo/engine.py` — `Observacao`, `EstadoMundo` e `WorldModelEngine`.
- `src/nexora/objetivos/engine.py` — `ObjetivoMeta` e `GoalEngine`.
- `src/nexora/estrategias/engine.py` — `Estrategia` e `StrategyEngine`.
- `src/nexora/comunicacao/bus.py` — `CommunicationBus`.
- `src/nexora/comunicacao/delegacao.py` — `Delegacao`, `DelegadorAgentes` e `ExecutorDelegacoes`.
- `src/nexora/agentes/registro.py` — `AgenteRegistro` e `RegistroAgentes`, incluindo descoberta por capacidade.
- `src/nexora/runtime/agente.py` — ciclo EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR e publicação opcional no Bus.
- `src/nexora/orquestracao/orquestrador.py` — ciclo de orquestração e publicação opcional no Bus.
- `src/nexora/experiencia/registro.py` — registro de experiências de resultados terminais de delegação.
- `src/nexora/auditoria/registro.py` — auditoria append-only em JSONL.
- `src/nexora/governanca/policy.py` — `PolicyEngine`, `RegraPolitica`, `DecisaoPolitica` e efeitos ALLOW/DENY.

## Fluxo atual de execução delegada
`DELEGAÇÃO → POLICY → ALLOW/DENY → EXECUTOR → RUNTIME/VERIFICAÇÃO → RECOVERY → EXPERIÊNCIA + AUDITORIA`

- Com `ALLOW`, a delegação passa por `ACEITA`, execução do handler/runtime, verificações/retries e termina em `CONCLUIDA` quando bem-sucedida.
- Com `DENY`, o handler não é executado; a delegação termina atualmente como `FALHOU`, com a decisão de política e o motivo registrados na auditoria.
- A integração é síncrona e em memória; não constitui ainda um sistema distribuído.

## Limites atuais verificados
- `PolicyEngine` é um MVP em memória: regras ordenadas, primeira correspondência vence e default `DENY`.
- ADR-009 prevê política declarativa e versionada em TOML/YAML; ainda não existe loader declarativo. Isso é evolução futura, não implementada nesta etapa.
- `RegistroAgentes` e descoberta/capacidades continuam em memória.
- `ExecutorDelegacoes` é síncrono/in-memory e depende de handlers/runtimes explicitamente registrados.
- O runtime fornece verificação e recuperação internas; o executor fornece recovery no nível da delegação.
- Auditoria é append-only em JSONL; experiência registra o resultado terminal da delegação.
- Não existe ainda um ciclo autônomo completo de planejamento → múltiplos agentes → execução → economia/evolução.
- Não foi criada uma nova fase.

## Long-Term Autonomy
- `src/nexora/autonomia/registro.py` permanece preservado.
- `MetaLongoPrazo` e `RegistroAutonomia` continuam responsáveis por metas de longo prazo e persistência JSONL append-only.
- CLI `nexora autonomia definir|atualizar|listar|resumir` permanece parte do sistema.

## Testes / CI
- Última evidência verde: workflow `34647078404`, com Python 3.11, 3.12, 3.13 e 3.14 em sucesso.
- A suíte atual inclui cobertura para execução delegada, integração com Runtime, recovery, experiência, auditoria e PolicyEngine ALLOW/DENY.
- Uma falha inicial do CI da etapa de Policy foi corrigida pela criação/exportação de `src/nexora/experiencia/__init__.py`; a execução posterior ficou verde.

## Estado de fase
**Fases históricas concluídas + evolução arquitetural pós-release em reconciliação.**

Não iniciar um novo componente/fase automaticamente.
