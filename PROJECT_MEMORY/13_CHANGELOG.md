# 13 — CHANGELOG

## Fase 21 — Persistência opcional do histórico do ProviderManager — 2026-09-12

O histórico operacional do `ProviderManager` passou a poder sobreviver a reinicializações sem transformar o componente em um banco de dados ou alterar o comportamento in-memory padrão.

### Persistência
- [x] `ProviderManager` aceita `persistencia_path` explícito.
- [x] `NEXORA_PROVIDER_HISTORY_PATH` permite configuração por ambiente.
- [x] Sem caminho configurado, o comportamento permanece in-memory.
- [x] Histórico JSON possui `schema_version`.
- [x] Escrita usa arquivo temporário + `os.replace`.
- [x] Histórico inválido/incompatível é ignorado sem derrubar o provider manager.
- [x] São persistidas somente métricas realmente medidas: chamadas, sucessos, erros, tempo total e últimas falhas.
- [x] ADR-018 registrada.

### Testes / CI
- [x] Testes cobrem persistência, reload, falhas, schema, atomicidade, limpeza do temporário e variável de ambiente.
- [x] CI run `34702844025` passou em Python 3.11, 3.12, 3.13 e 3.14.

### Limite preservado
- [ ] O caminho real do `Orquestrador` ainda executa diretamente a instância selecionada; o próximo incremento deve fazer essa execução alimentar as métricas do `ProviderManager` sem duplicar chamadas.
- [ ] Tokens/custo permanecem pendentes até existir telemetria real e confiável.

## Fase 21 — Integração real do roteamento com ExecutionTrace — 2026-09-12

O roteamento inteligente deixou de ser apenas uma função de decisão isolada e passou a participar do caminho real `Orquestrador → AgentRuntime`.

### ProviderManager / seleção
- [x] `ProviderManager.obter_com_modelo()` permite instanciar explicitamente o modelo escolhido pelo roteador.
- [x] Não existe fallback silencioso para outro modelo quando a factory não suporta configuração por modelo.

### Orchestrator / Runtime / Trace
- [x] `Orquestrador` aceita `RoteadorInteligente`, `ProviderManager`, candidatos e perfil de hardware de forma opcional, preservando compatibilidade do caminho legado.
- [x] A decisão é feita antes da execução do provider.
- [x] O provider é instanciado com o modelo efetivamente selecionado.
- [x] `ExecutionTrace.provider` e `ExecutionTrace.model` refletem a execução selecionada.
- [x] `ExecutionTrace.metadata.routing_decision` registra provider, modelo, score, adequação e motivos dos candidatos avaliados.
- [x] `AgentRuntime` continua sendo o único proprietário do ciclo de execução.
- [x] Não foi criado terceiro Runtime.

### Testes / CI
- [x] Teste de integração cobre `RoteadorInteligente → Orquestrador → AgentRuntime → ExecutionTrace`.
- [x] O teste confirma que o provider legado de fallback não é chamado quando o roteamento inteligente está configurado.
- [x] O teste confirma seleção do modelo de coding e propagação para o trace.
- [x] CI run #243 (`34702264099`) passou em Python 3.11, 3.12, 3.13 e 3.14 no commit `386e810af8502a03a2bdc66d2d9c3d3360813e62`.
- [x] Falhas intermediárias dos runs #240 e #241 foram diagnosticadas pelos logs e corrigidas antes do fechamento do checkpoint.

## Fase 17 — Provider local Ollama — 2026-09-12

A NEXORA iniciou oficialmente a Fase 17 — Local Intelligence Foundation.

### Provider
- [x] Criado `src/nexora/providers/ollama.py`.
- [x] Implementado sobre o contrato Provider existente.
- [x] HTTP via stdlib, sem dependências pip adicionais.
- [x] Endpoint padrão `http://localhost:11434`.
- [x] Endpoint configurável por `NEXORA_OLLAMA_URL`.
- [x] Modelo configurável por `NEXORA_OLLAMA_MODEL`.
- [x] Perfil padrão inicial `qwen2.5-coder:7b-instruct-q4_K_M`.
- [x] Geração via `/api/chat`.
- [x] Health check via `/api/tags`, sem consumir geração.
- [x] Indisponibilidade HTTP/rede normalizada para `ProviderIndisponivel`.
- [x] Streaming e tool-calling não declarados antes de implementação/testes específicos.

### Integração
- [x] Provider pode ser registrado no `RegistryProviders` existente.
- [x] Provider pode ser executado pelo `ProviderManager` existente.
- [x] Não foi criado Runtime paralelo.
- [x] ADR-015 registrada.

### Testes
- [x] Testes unitários cobrem configuração, ambiente, payload, resposta, erros e health check.
- [x] Teste de integração cobre `RegistryProviders → ProviderManager → ProviderOllama` com HTTP mockado.
- [ ] Validação contra uma instalação real de Ollama ainda pendente.

## Integração de idempotência no caminho de ferramentas — 2026-09-12

A NEXORA avançou uma barreira de segurança para efeitos externos sem habilitar retry automático.

### Contrato
- [x] `StoreIdempotenciaMemoria` fornece identidade, fingerprint determinístico e estados `IN_PROGRESS`, `SUCCEEDED`, `FAILED`.
- [x] Reivindicação atômica informa se a chamada é a primeira dona da execução.
- [x] Reutilização da chave com fingerprint diferente gera conflito.
- [x] Reutilização de operação `SUCCEEDED` devolve o resultado armazenado sem executar novamente.
- [x] Operação `IN_PROGRESS` não é repetida.
- [x] Operação `FAILED` não recebe retry automático.

### Registry / Orchestrator / Planning
- [x] `RegistryFerramentas` aceita store de idempotência opcional.
- [x] Ordem canônica passou a ser `Permission → Policy → Checkpoint → Idempotency → Tool → Observation → Verification → Audit → Result` quando a barreira está habilitada.
- [x] Sem store configurado, o comportamento legado permanece preservado.
- [x] `Orquestrador` usa automaticamente `objetivo:tarefa:ferramenta` como identidade quando o Registry possui idempotência.
- [x] Planner/Tarefa pode declarar `idempotencia_chave` explicitamente.
- [x] A chave explícita é persistida no contrato de `Tarefa` e exposta no resultado da etapa.

### Testes
- [x] Testes unitários de idempotência no Registry cobrem execução única, duplicidade, conflito, `IN_PROGRESS`, `FAILED` e auditoria.
- [x] Testes de integração cobrem Orchestrator → Registry → Idempotency → Tool.
- [x] Teste de `Tarefa` cobre persistência da chave explícita.

## Reconciliação Orchestrator ↔ AgentRuntime — 2026-09-12

A NEXORA avançou na reconciliação do ciclo de execução sem criar nova fase.

### Arquitetura
- [x] ADR-012 registrada: Orchestrator é coordenador de alto nível; AgentRuntime é o limite canônico do ciclo de execução do agente.
- [x] `Orquestrador` deixou de depender de `ExecutorCiclo`/`VerificadorCiclo` para o caminho normal.
- [x] Cada tarefa agora possui um único ciclo de execução via `AgenteRuntime`.
- [x] `core/ciclo.py` permanece preservado como compatibilidade durante a migração.
- [x] Resultado do `AgenteRuntime` é normalizado no contrato de resultado do Orchestrator.

### Runtime / resiliência
- [x] Exceções de execução no `AgenteRuntime` são convertidas em `Observacao` com erro, permitindo análise controlada.
- [x] Exceções de verificação também são convertidas em observação controlada.
- [x] O ciclo avançado `EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR` foi preservado.

### Ferramentas / governança
- [x] Tarefas com ferramenta continuam usando `RegistryFerramentas` como executor governado.
- [x] A primeira integração não introduz retry automático de ferramentas, evitando repetir efeitos externos sem idempotência explícita.
- [x] Permission/Policy/Checkpoint continuam pertencendo à fronteira de governança existente.

### Testes
- [x] Adicionado `tests/integration/test_orquestrador_agent_runtime.py`.
- [x] Teste cobre recuperação de falha de provider através do runtime.
- [x] Teste cobre exceção de provider sem propagação indevida pelo Orchestrator.

## Fechamento da reconciliação do Runtime — 2026-09-12

O `main` continua evoluindo após `v1.0.0`, sem criar nova fase.

### Runtime / agentes
- [x] `AgenteRuntime` usa `Observacao` estruturada no caminho de análise de falhas.
- [x] Coding Agent transporta erros de validação para `Observacao.erro`.
- [x] Research Agent transporta erros de validação para `Observacao.erro`.
- [x] Falhas de validação corrigíveis permanecem retentáveis nos agentes especializados.
- [x] O ciclo generalista `EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR` foi preservado.
- [x] Não foi introduzida uma terceira camada de execução.

## Correção de warnings do Policy Loader — 2026-09-12

- [x] Corrigidos os escapes inválidos nas regex de `tests/unit/test_policy_loader.py`.
- [x] Commit: `a608056d700519f2f62447f23c1148bd621c4be2`.

## v1.0.0 — Release — 2026-09-11

- Fase 16 — Long-Term Autonomy concluída no commit `c49d3d2...`.
- `MetaLongoPrazo` e `RegistroAutonomia` com persistência JSONL determinística.
- CLI `nexora autonomia definir|atualizar|listar|resumir`.
