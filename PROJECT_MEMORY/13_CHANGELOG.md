# 13 — CHANGELOG

## Orchestrator → Tool Registry — 2026-09-11

O `main` continuou evoluindo após `v1.0.0`, sem criar nova fase.

### Integração
- [x] `Orquestrador` aceita `RegistryFerramentas` opcional.
- [x] Tarefas com `ferramenta` configurada são encaminhadas ao Registry existente.
- [x] Tarefas sem ferramenta preservam o caminho existente de Provider.
- [x] O fluxo integrado mantém `Permission → Policy → Checkpoint → Tool → Observation → Verification → Audit → Result`.
- [x] Foi criado teste de integração cobrindo o caminho Orchestrator → Registry e confirmando que o Provider não é chamado para a tarefa com ferramenta.
- [x] Correção do teste integrado: `origem=` é o argumento correto do `PolicyEngine`.

### Validação
- [x] HEAD validado: `f67f270c25609559264c19ef7a2561cc359873b8`.
- [x] CI Run #138 (`34658836451`) concluído com SUCCESS em Python 3.11, 3.12, 3.13 e 3.14.

## Fechamento do fluxo de ferramenta — 2026-09-11

O `main` continuou evoluindo após `v1.0.0`, sem criar nova fase.

### Tool → Observation → Verification → Audit → Result
- [x] `RegistryFerramentas` mantém a autorização antes da ação.
- [x] Checkpoint permanece imediatamente antes da execução da ferramenta.
- [x] `ResultadoFerramenta` consolida resultado, observação e verificação quando esses estágios estão configurados.
- [x] `RegistryFerramentas` aceita `RegistroAuditoria` opcional.
- [x] Execução bem-sucedida gera `ferramenta.resultado`, sem registrar parâmetros potencialmente sensíveis.
- [x] Falha do executor gera `ferramenta.falhou` com tipo/mensagem da exceção e propaga a exceção original.
- [x] Auditoria de resultado registra ferramenta, solicitante, sucesso, observação e verificação sem copiar o resultado bruto.
- [x] Testes cobrem resultado bruto legado, resultado observado/verificado e falha auditada.

### Limites deliberados
- [ ] Persistência durável de checkpoints ainda não implementada.
- [ ] Rollback de efeitos externos ainda não implementado.
- [ ] Observação/verificação e auditoria são opcionais no Registry para preservar compatibilidade.

## Checkpoint Engine — 2026-09-11

O `main` continuou evoluindo após `v1.0.0`, sem criar nova fase.

### Checkpoint
- [x] Criado `src/nexora/runtime/checkpoint.py` com `Checkpoint` imutável e `CheckpointEngine`.
- [x] Captura de estado com cópia profunda, evitando que alterações posteriores no estado original contaminem o snapshot.
- [x] Recuperação devolve nova cópia e não executa ferramentas nem tenta desfazer efeitos externos.
- [x] Checkpoints podem ser filtrados por `execucao_id`.
- [x] Criação e recuperação podem ser registradas no `RegistroAuditoria`.
- [x] Validações cobrem identificadores, motivo, tipo de estado e checkpoint inexistente.
- [x] Testes em `tests/unit/test_checkpoint.py`.

### Limites deliberados
- [ ] Persistência durável de checkpoints ainda não implementada.
- [ ] Rollback de efeitos externos ainda não implementado.
- [x] Integração Tool/Sandbox com governança/checkpoint foi feita de forma explícita e mínima, sem transformar o CheckpointEngine em executor.

## Evolução multiagente e governança de execução — 2026-09-11

A tag `v1.0.0` permanece ancorada em `c49d3d2df314bb8c2d849c4466736f15841e8893`. O `main` continuou evoluindo sem criar uma nova fase.

### Execução delegada
- [x] `ExecutorDelegacoes` introduz a camada explícita de execução das delegações recebidas pelo CommunicationBus.
- [x] Integração opcional com `AgenteRuntime`, preservando execução, verificação, análise, correção e reteste.
- [x] Recovery no nível da delegação com `max_tentativas`.

### Experiência e auditoria
- [x] Resultados terminais podem ser registrados no `RegistroExperiencias`.
- [x] `RegistroAuditoria` fornece log append-only em JSONL.
- [x] Executor registra aceite, conclusão e falha.

### Policy / Governança
- [x] `PolicyEngine` mínimo com ALLOW/DENY, filtros, ordem determinística e default DENY.
- [x] Executor consulta a política antes da execução.
- [x] Decisão auditada com efeito, permitido, motivo, versão, origem e fingerprint.
- [x] Loader declarativo TOML versão 2 com schema estrito e IDs únicos.
- [x] Fingerprint canônico SHA-256 da semântica da política.
- [x] `DENEGADA` separa negação de governança de falha de execução.
- [x] `GerenciadorPermissoes` / `PedidoPermissao` estabelecem uma fronteira explícita de autorização sem executar a ação.
- [x] `GerenciadorPolitica` implementa reload validado e troca atômica, preservando a política anterior quando a nova é rejeitada.
- [x] Registry de ferramentas pode exigir permissão antes do executor, preservando compatibilidade sem governança configurada.
- [x] Sandbox mantém allowlist e pode exigir Policy antes de `subprocess.run`; DENY impede a execução.
- [x] Contexto de auditoria do Sandbox registra somente o comando-base, evitando copiar argumentos potencialmente sensíveis.
- [ ] YAML ainda não implementado.

### Correção de empacotamento
- [x] Criado/exportado `src/nexora/experiencia/__init__.py`, corrigindo importação no CI.

### Validação
- [x] CI verde para Python 3.11–3.14 no HEAD atual `f67f270c25609559264c19ef7a2561cc359873b8`.
- [x] Run #138 (`34658836451`) concluído com SUCCESS.
- [x] Testes adicionados para permission boundary, policy lifecycle, tool governance, Sandbox governance, Checkpoint Engine, auditoria de resultados e integração Orchestrator → Tool Registry.

## Reconciliação pós-v1.0.0 — 2026-09-11

Foram identificados e reconciliados os componentes arquiteturais pós-release anteriores a esta etapa: Context, Knowledge, World Model, Goal, Strategy, Communication Bus, Runtime/Orchestrator, Delegation, Agent Registry, capability delegation e testes correspondentes.

## v1.0.0 — Release — 2026-09-11

- Fase 16 — Long-Term Autonomy concluída no commit `c49d3d2...`.
- `MetaLongoPrazo` e `RegistroAutonomia` com persistência JSONL determinística.
- CLI `nexora autonomia definir|atualizar|listar|resumir`.
- Suite documentada naquele ponto: 128 testes passando.
- Tag `v1.0.0` criada em `c49d3d2...`.
