# 13 — CHANGELOG

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
- [ ] CI correspondente ao HEAD atual ainda precisa ser confirmado.

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
- [ ] CI do novo HEAD ainda precisa ser confirmado antes de marcar o checkpoint como validado.

## Fechamento da reconciliação do Runtime — 2026-09-12

O `main` continua evoluindo após `v1.0.0`, sem criar nova fase. Este checkpoint fechou a etapa de consistência interna do runtime antes da integração Orchestrator ↔ AgentRuntime.

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

## Orchestrator → Tool Registry — 2026-09-11

- [x] `Orquestrador` aceita `RegistryFerramentas` opcional.
- [x] Tarefas com ferramenta são encaminhadas ao Registry existente.
- [x] Tarefas sem ferramenta preservam Provider.
- [x] O fluxo mantém `Permission → Policy → Checkpoint → Tool → Observation → Verification → Audit → Result`.

## Fechamento do fluxo de ferramenta — 2026-09-11

- [x] Registry mantém autorização antes da ação.
- [x] Checkpoint permanece imediatamente antes da ferramenta.
- [x] `ResultadoFerramenta` consolida resultado, observação e verificação.
- [x] Auditoria evita copiar resultado bruto potencialmente sensível.

## Checkpoint Engine — 2026-09-11

- [x] `Checkpoint` imutável e `CheckpointEngine` criados.
- [x] Snapshot com cópia profunda.
- [x] Recuperação devolve cópia isolada.
- [x] Criação/recuperação podem ser auditadas.
- [ ] Persistência durável ainda não implementada.
- [ ] Rollback de efeitos externos ainda não implementado.

## Evolução multiagente e governança — 2026-09-11

- [x] ExecutorDelegacoes com integração opcional ao AgentRuntime.
- [x] Recovery de delegação com `max_tentativas`.
- [x] Registro de experiências e auditoria JSONL.
- [x] PolicyEngine ALLOW/DENY, default DENY e fingerprint SHA-256.
- [x] Loader TOML v2 estrito.
- [x] Permission boundary explícita.
- [x] Policy Manager com reload validado e troca atômica.
- [x] Sandbox com allowlist e Policy opcional.

## v1.0.0 — Release — 2026-09-11

- Fase 16 — Long-Term Autonomy concluída no commit `c49d3d2...`.
- `MetaLongoPrazo` e `RegistroAutonomia` com persistência JSONL determinística.
- CLI `nexora autonomia definir|atualizar|listar|resumir`.