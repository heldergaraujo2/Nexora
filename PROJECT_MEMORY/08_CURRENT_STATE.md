# 08 — ESTADO ATUAL

> Estado operacional do repositório e ponto de continuidade. A fonte de verdade é a convergência entre Git, testes, arquitetura e PROJECT_MEMORY.

## Versão / HEAD atual
- Release histórica: v1.0.0, tag apontando para `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- HEAD atual de código validado: `eccff2d3390807cfc0c7e839f6a055a0b1a867c5`.
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
- `src/nexora/governanca/policy_loader.py` — loader declarativo TOML versionado, com validação estrita e default DENY.
- `src/nexora/config/loaders.py` — suporte genérico a carregamento TOML via `tomllib`.

## Fluxo atual de execução delegada
`DELEGAÇÃO → POLICY → ALLOW/DENY → EXECUTOR → RUNTIME/VERIFICAÇÃO → RECOVERY → EXPERIÊNCIA + AUDITORIA`

- Com `ALLOW`, a delegação passa por `ACEITA`, execução do handler/runtime, verificações/retries e termina em `CONCLUIDA` quando bem-sucedida.
- Com `DENY`, o handler não é executado; a delegação termina atualmente como `FALHOU`, com a decisão de política e o motivo registrados na auditoria.
- A decisão auditada inclui efeito, permitido, motivo, versão da política e origem do arquivo quando a política foi carregada de configuração.
- A integração é síncrona e em memória; não constitui ainda um sistema distribuído.

## Política declarativa atual
- O `PolicyEngine` mantém o motor de decisão separado do parser/configuração.
- `carregar_policy_toml()` lê políticas declarativas com `[policy]`, `version = 1`, `default = "deny"` e `[[policy.rules]]`.
- O loader rejeita versão inválida, campos desconhecidos, efeitos inválidos, regras malformadas e tipos incompatíveis; não executa código proveniente do TOML.
- A política carregada preserva `versao` e `origem` na `DecisaoPolitica` e na auditoria.
- YAML ainda não foi implementado; TOML foi adotado primeiro por usar `tomllib` da biblioteca padrão.
- `pyproject.toml` requer Python `>=3.11` por causa do uso de `tomllib` sem dependência externa.

## Limites atuais verificados
- `PolicyEngine` é um MVP determinístico: regras ordenadas, primeira correspondência vence e default `DENY`.
- Ainda não existe identidade explícita de regra/match ID na decisão auditada.
- Ainda não existe fingerprint/hash do conteúdo da política; a origem atualmente identifica o caminho do arquivo.
- Não existe hot reload de políticas.
- Não existe estado `DENEGADA` no enum de delegação; DENY termina atualmente como `FALHOU`.
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
- HEAD de código validado: `eccff2d3390807cfc0c7e839f6a055a0b1a867c5`.
- Workflow `34649533683` confirmou Python 3.11, 3.12, 3.13 e 3.14 em **success**.
- A suíte atual inclui cobertura para execução delegada, integração com Runtime, recovery, experiência, auditoria, PolicyEngine ALLOW/DENY, loader TOML e metadados de rastreabilidade da decisão.

## Estado de fase
**Fases históricas concluídas + evolução arquitetural pós-release em reconciliação.**

Não iniciar um novo componente/fase automaticamente.
