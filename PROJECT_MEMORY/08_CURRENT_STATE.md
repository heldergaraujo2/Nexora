# 08 — ESTADO ATUAL

> Estado operacional do repositório e ponto de continuidade. A fonte de verdade é a convergência entre Git, testes, arquitetura e PROJECT_MEMORY.

## Versão / HEAD atual
- Release histórica: v1.0.0, tag apontando para `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- HEAD atual: `16a425a8c2dacdaa841b9678f6f6651155adee07`.
- O `main` está 41 commits à frente do commit da tag v1.0.0: 39 commits de evolução pós-release + 2 commits de correção dos testes de integração do CommunicationBus.
- A versão de pacote continua `1.0.0`; isso não significa que a arquitetura esteja congelada.

## Estado arquitetural real
A Fase 16 — Long-Term Autonomy continua concluída e preservada. Depois dela, o código evoluiu com uma camada transversal de contexto, conhecimento, world model, objetivos, estratégias, comunicação e arquitetura multi-agente.

### Componentes pós-v1.0.0 verificados
- `src/nexora/contexto/engine.py` — `Contexto` e `ContextEngine`, montagem determinística de contexto.
- `src/nexora/conhecimento/engine.py` — `Conhecimento` e `KnowledgeEngine`, conhecimento com fonte, evidências, confiança e validação; busca lexical no MVP.
- `src/nexora/mundo/engine.py` — `Observacao`, `EstadoMundo` e `WorldModelEngine`, registro de evidências e resolução determinística por confiança.
- `src/nexora/objetivos/engine.py` — `ObjetivoMeta` e `GoalEngine`, criação, priorização e progresso de metas.
- `src/nexora/estrategias/engine.py` — `Estrategia` e `StrategyEngine`, avaliação e ranking determinístico de estratégias.
- `src/nexora/comunicacao/bus.py` — `CommunicationBus`, mensagens tipadas em memória, assinatura, correlação e estados PENDENTE/ENTREGUE/LIDA.
- `src/nexora/comunicacao/delegacao.py` — `Delegacao` e `DelegadorAgentes`, solicitação/atualização de delegações e correlação de respostas.
- `src/nexora/agentes/registro.py` — `AgenteRegistro` e `RegistroAgentes`, catálogo de agentes, capacidades, tags, prioridade, disponibilidade e descoberta determinística.
- `src/nexora/runtime/agente.py` — publicação opcional do ciclo do runtime no bus.
- `src/nexora/orquestracao/orquestrador.py` — publicação opcional do ciclo de orquestração no bus.

## Limites atuais verificados
- Registry de agentes/capacidades é em memória; não há persistência/versionamento completo do registry.
- Descoberta por capacidade é exata após normalização e seleciona pelo maior `prioridade`, com desempate por `id`.
- `DelegadorAgentes` envia a solicitação e publica o resultado quando `atualizar()` é chamado; ele não executa automaticamente a tarefa delegada.
- O CommunicationBus é infraestrutura de transporte/registro; não chama providers nem executa ferramentas.
- Runtime e Orchestrator publicam eventos, mas a integração atual não constitui ainda um ciclo autônomo completo de execução entre múltiplos agentes.
- Os engines de Context, Knowledge, World Model, Goals e Strategy são MVPs determinísticos e em memória, sem afirmar capacidades semânticas, persistência ou autonomia que ainda não existem.

## Long-Term Autonomy
- `src/nexora/autonomia/registro.py` permanece preservado.
- `MetaLongoPrazo` e `RegistroAutonomia` continuam responsáveis por metas de longo prazo e persistência JSONL append-only.
- CLI `nexora autonomia definir|atualizar|listar|resumir` permanece parte do sistema.

## Testes
- Última execução CI observada no HEAD anterior à correção: `163 passed, 2 failed`.
- As duas falhas estavam em `test_runtime_comunicacao.py` e `test_orquestrador_comunicacao.py`: os testes esperavam `ENTREGUE` sem assinante, enquanto o CommunicationBus define `ENTREGUE` quando há entrega a callbacks e mantém `PENDENTE` quando não há assinantes.
- Os dois testes foram corrigidos de forma mínima para refletir o contrato existente, sem alterar o CommunicationBus.
- Nova execução CI foi disparada pelo commit `836ade6...`; resultado final deve ser registrado no próximo refresh do Handoff antes do commit de documentação.

## Estado de fase
Não foi criada uma nova fase. O estado correto é:
**Fases históricas concluídas + evolução arquitetural pós-release em reconciliação.**

Não iniciar um novo componente/fase automaticamente.
