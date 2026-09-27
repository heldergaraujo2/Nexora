# 08 — ESTADO ATUAL

## Estado
- Fase 16 — Long-Term Autonomy: concluída e preservada.
- Fase 17 — Local Intelligence Foundation: em implementação avançada.
- Fase 21 — Intelligent Model Routing: fundação implementada e integrada ao caminho real de execução.
- `ProviderOllama` implementado e integrado ao contrato de Providers.
- Descoberta de modelos locais, perfis, avaliação hardware × modelo e seleção de candidatos implementados.
- `RoteadorInteligente` considera adequação, hardware, capacidades declaradas, health opcional e histórico operacional real medido por modelo quando há amostra suficiente.
- `Orquestrador` pode usar o roteador inteligente para selecionar provider + modelo e registrar a decisão no `ExecutionTrace`.

## Fase 17 — progresso
- [x] Provider Ollama via HTTP stdlib.
- [x] Endpoint configurável (`NEXORA_OLLAMA_URL`).
- [x] Modelo configurável (`NEXORA_OLLAMA_MODEL`).
- [x] Perfil inicial Qwen2.5-Coder 7B Q4.
- [x] Health check `/api/tags`.
- [x] `listar_modelos()` no Provider.
- [x] `ModeloLocal` e `DescobridorModelosOllama`.
- [x] Perfis determinísticos de capacidade de modelo.
- [x] Detecção conservadora inicial de CPU/RAM/OS/arquitetura.
- [x] Avaliação hardware × modelo.
- [x] Seleção determinística de modelos adequados.
- [ ] Detecção detalhada de GPU/VRAM por plataforma.
- [ ] Teste contra daemon Ollama real.
- [ ] Instalador/setup automático.

## Fase 21 — Intelligent Model Routing
- [x] Roteador provider/modelo provider-agnostic.
- [x] Filtragem de providers registrados.
- [x] Validação de tool-calling, streaming e contexto.
- [x] Health opcional como requisito de seleção.
- [x] Score determinístico de adequação do modelo.
- [x] Histórico medido de chamadas, sucesso, erro e latência média.
- [x] Histórico específico por `provider + modelo` para chamadas, sucesso/erro e latência.
- [x] Quando há pelo menos 3 chamadas do par, confiabilidade e latência não misturam modelos diferentes do mesmo provider.
- [x] Fallback para histórico agregado do provider quando o par ainda não tem amostra suficiente.
- [x] Ajuste histórico deliberadamente limitado e explicável.
- [x] Amostra mínima de 3 chamadas antes de influenciar o score histórico.
- [x] Ponte de decisão para `ExecutionTrace.metadata`.
- [x] Integração real `RoteadorInteligente → Orquestrador → AgentRuntime → ExecutionTrace`.
- [x] Instanciação explícita do provider com o modelo selecionado, sem fallback silencioso.
- [x] Persistência opcional e versionada do histórico do `ProviderManager`.
- [x] Configuração por argumento ou `NEXORA_PROVIDER_HISTORY_PATH`.
- [x] Escrita atômica e tolerância a histórico inválido/incompatível.
- [x] Caminho real `Orquestrador → AgentRuntime → Provider` alimenta métricas do `ProviderManager` sem duplicar a execução.
- [x] Telemetria real de tokens no `ProviderManager` e no `ExecutionTrace`, sem estimativas.
- [x] Histórico evoluído para schema v4 com métricas por modelo.
- [x] `PricingRegistry` versionado por provider/modelo, com fonte e data de vigência.
- [x] Preços públicos Groq para `openai/gpt-oss-120b` e `openai/gpt-oss-20b` registrados em snapshot 2026-09-12.
- [x] `ProviderManager` calcula custo somente com tokens reais + preço exato conhecido.
- [x] `ExecutionTrace.cost` recebe custo real no caminho do Orquestrador.
- [x] Roteador compara custo real por modelo, sem misturar modelos do mesmo provider.
- [x] Amostra mínima de 3 gerações precificadas permanece obrigatória para influência do custo.
- [x] Custo nunca substitui adequação funcional; ajuste máximo por custo: ±0.75 ponto.
- [x] Custo histórico pode ser explicitamente desativado com `considerar_custo=False`.
- [x] Testes dedicados cobrem separação/persistência por modelo, custo, amostra insuficiente e falhas por modelo.
- [x] Testes adicionais cobrem confiabilidade e latência específicas do modelo.
- [x] Histórico persistente de avaliação por `provider + modelo + tipo de tarefa`.
- [x] Gate de qualidade com amostra mínima configurável.
- [x] Qualidade só influencia quando pelo menos dois candidatos possuem evidência suficiente do mesmo tipo de tarefa.
- [x] Peso de maturidade da amostra: 0,5 no limiar mínimo e até 1,0 em `2 × min_amostra`.
- [x] Influência da qualidade permanece limitada a ±1,0 e não substitui outros sinais.
- [x] Testes cobrem gate, isolamento, maturidade da amostra e impacto conservador no ranking.

## Sinal de avaliação de resultado — foundation
- [x] Criado `ResultadoAvaliacao` com sucesso, score normalizado, critérios, evidências e metadados.
- [x] Criado `AvaliadorResultado` para composição determinística de avaliadores explícitos.
- [x] `AgenteRuntime` aceita avaliador opcional sem alterar o comportamento legado quando ausente.
- [x] Avaliação é registrada no `ResultadoAgente`, métricas, `ExecutionTrace.metadata.evaluation`, registrador e CommunicationBus.
- [x] Ausência de critérios não produz qualidade artificial.
- [x] ADR-022 registrada.
- [x] Testes unitários cobrem contrato, agregação, ausência de critérios e integração com Runtime/Trace.

## Arquitetura canônica
`Objetivo → Orchestrator → Plano/Tarefas → Seleção de executor/agente → Roteador Inteligente → AgentRuntime → Permission/Policy/Checkpoint → Idempotency (quando aplicável) → Provider/Tool → Observation → Verification → Analysis → Correction/Recovery → Retest → Audit/Experience → Evaluation (quando configurada) → ExecutionTrace → Result`.

O roteamento é decisão antes da execução; o provider/modelo escolhido é refletido no trace. O `AgentRuntime` continua sendo o único proprietário do ciclo de execução. `core/ciclo.py` permanece legado/compatibilidade até migração segura.

## Governança
- Permission antes da ação.
- Policy default DENY.
- Checkpoint antes da ferramenta.
- Idempotência antes de efeitos externos quando configurada.
- Registry continua sendo a fronteira de execução governada das ferramentas.

## UI futura
A Fase 23 define uma UI extremamente tecnológica, futurista e inovadora, mas simples de usar. A interface deve comunicar a inteligência interna sem expor a complexidade arquitetural ao usuário.

## Próximas fases
17. Local Intelligence Foundation.
18. Coding Workspace Agent.
19. Dev Loop + Programming Experience.
20. Code Knowledge + RAG.
21. Intelligent Model Routing.
22. Hardware & NEXORA Setup.
23. NEXORA UI / Experience Layer.
24. Autonomous Product Engine.
25. Continuous Evolution.
\n## Fase 26 — Ecosystem Integration Foundation — 2026-09-27\n\nA NEXORA incorporou uma camada própria inspirada em padrões públicos de Graphiti/AgentMemory/Letta/LangGraph/PydanticAI/MCP/OpenSandbox/OpenTelemetry/AgentSynth/A-Evolve/Dream Cycle e ecossistemas relacionados, sem transformar o projeto em wrapper de terceiros.\n\n### [x] Memory híbrida\n- `src/nexora/memoria/hibrida.py` combina ranking lexical, semantic hook, graph hook, RRF e decay temporal.\n\n### [x] World Model temporal\n- `src/nexora/world/grafo_temporal.py` fornece entidades, fatos com validade temporal e consultas as-of.\n\n### [x] Retry seguro\n- `src/nexora/runtime/retry.py` tipa retry por domínio e bloqueia efeitos externos não idempotentes.\n- `AgenteRuntime` usa `RetryPolicy` e `TracerGenAI` opcionais.\n\n### [x] Checkpoint durável opcional\n- `CheckpointEngine` agora pode persistir snapshots JSON versionados e atomicamente.\n- Sem `persistencia_path`, comportamento in-memory permanece compatível.\n\n### [x] Sandbox backend\n- `SandboxBackend` permite backend intercambiável.\n- subprocesso local continua padrão.\n- adapter Docker permanece fail-closed até integração explícita.\n\n### [x] MCP boundary\n- Contratos Tool/Resource/Prompt adicionados.\n- `MCPToolAdapter` importa tools para o `RegistryFerramentas`, preservando Permission/Policy/Checkpoint/Idempotency.\n\n### [x] Research guardrails\n- orçamento de consultas/fontes/domínios.\n- bloqueio conservador de localhost/private/link-local/reserved IP.\n- ResearchAgent aplica o filtro antes de montar contexto.\n\n### [x] GenAI observability\n- spans e eventos independentes de SDK externo.\n- AgentRuntime pode emitir span por tentativa.\n\n### [x] Evolution\n- candidatos, hipóteses, rollback, avaliação e gate contra regressão/risco/evidência insuficiente.\n- DreamCycle coordena melhoria sem promoção automática fora do gate.\n\n### [x] Economy foundation\n- scoring de oportunidade por valor esperado, custo, risco e mercado.\n- máquina de estados descoberta → protótipo → validação → lançamento → medição → melhoria → receita → reinvestimento.\n- nenhuma transação financeira automática.\n\n### Testes novos\n- Memory híbrida\n- Grafo temporal\n- Retry policy\n- Sandbox backend\n- MCP Registry/Adapter\n- GenAI tracing\n- Evolution/DreamCycle\n- Economy lifecycle\n- Research guardrails\n- Checkpoint persistence\n\nReferência completa: `docs/ECOSYSTEM_HARVEST.md`.\n\n## Validação da Ecosystem Integration Foundation — 2026-09-27\n\n- [x] HEAD validado: `abbbd856207bac518cd311f591bfa5fe679525ac`.\n- [x] CI #416 (`36345435513`) — GREEN em Python 3.11/3.12/3.13/3.14.\n- [x] 392 testes passando.\n- [x] Correção de compatibilidade do Sandbox preservou o símbolo `subprocess` usado por testes existentes.\n- [x] Research reconciliation normaliza marcadores `[fonte:N]` antes de agrupar claims.\n- [x] Browser adapter fail-closed adicionado.\n- [x] Gate de reinvestimento exige autorização humana para efeito financeiro.\n
## Checkpoint documental final — 2026-09-27
- HEAD mais recente no momento deste registro: `6e09c1b4096947a028bfe94ad981947df1295e1a`.
- Run #421 (`36345499730`) confirmado GREEN em Python 3.11/3.12/3.13/3.14.
- Os 392 testes continuam passando no checkpoint de código imediatamente anterior; as alterações posteriores deste checkpoint são apenas documentação de continuidade.
