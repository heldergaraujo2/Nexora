# 11 — TASKS

## Histórico — preservado

As seções abaixo registram o planejamento e a execução das fases iniciais. Elas permanecem como histórico e não devem ser interpretadas como estado atual.

## Concluídas originalmente
- [x] Fase 0 (Continuidade e Memória)
- [x] Capability Discovery e integração dos documentos 02–05
- [x] Integração do repositório e memória 00–15
- [x] Propostas A–E aprovadas
- [x] P1–P11 e ADRs correspondentes
- [x] Fase 1 — Fundação
- [x] Fase 2 — Providers & Conectores

## Fases posteriores concluídas
- [x] Fases 3–10 conforme roadmap histórico
- [x] Fase 11 — Economic Engine
- [x] Fase 12 — Security Engine
- [x] Fase 13 — Memory Engine
- [x] Fase 14 — Resource Management
- [x] Fase 15 — Portfolio Engine
- [x] Fase 16 — Long-Term Autonomy

## Reconciliação pós-v1.0.0 — 2026-09-11/12

### Implementado e verificado no código
- [x] Context Engine
- [x] Knowledge Engine
- [x] World Model Engine
- [x] Goal Engine
- [x] Strategy Engine
- [x] Communication Bus
- [x] Integração do Agent Runtime com CommunicationBus
- [x] Publicação do ciclo do Orchestrator no CommunicationBus
- [x] DelegadorAgentes
- [x] Agent Registry
- [x] Capability Registry / descoberta por capacidade
- [x] Delegação baseada em capacidade
- [x] Testes unitários correspondentes
- [x] CI automatizado com matriz Python 3.11–3.14
- [x] AgentRuntime como proprietário do ciclo avançado
- [x] ExecutionTrace mínimo integrado ao AgentRuntime e Orchestrator
- [x] ADR-012 — Orchestrator/AgentRuntime como ciclo canônico
- [x] ADR-013 — inventário e preservação do ciclo legado
- [x] Contrato mínimo de idempotência para efeitos externos
- [x] Testes de duplicidade, conflito de fingerprint, falha, determinismo e concorrência
- [x] ADR-014 — idempotência como barreira antes de retry de efeitos externos
- [x] Integração da barreira de idempotência ao RegistryFerramentas
- [x] Chave de idempotência explícita persistida em Tarefa/Plano
- [x] Roteamento do Orchestrator para idempotência quando o Registry estiver configurado
- [x] Testes unitários e de integração do caminho Orchestrator → Registry → Idempotency → Tool

### Correção de teste relacionada à reconciliação
- [x] Alinhar as expectativas dos testes de Runtime/Orchestrator ao contrato real do CommunicationBus (`PENDENTE` sem assinante; `ENTREGUE` quando há callback).
- [x] Não alterar o comportamento do Bus.

## Estado atual das tarefas
- [x] Auditar os commits pós-Fase 16.
- [x] Auditar os componentes de contexto, conhecimento, mundo, objetivos, estratégia, agentes e comunicação.
- [x] Comparar os componentes com os requisitos arquiteturais.
- [x] Identificar limites e lacunas da infraestrutura de agentes.
- [x] Reconciliar a numeração do roadmap para refletir as Fases 11–16 reais.
- [x] Atualizar a memória operacional principal.
- [x] Definir a idempotência mínima antes de qualquer retry externo.
- [x] Integrar idempotência ao caminho canônico do Registry de ferramentas.
- [x] Cobrir a integração com testes de duplicidade e não repetição.
- [ ] Confirmar CI verde no HEAD atual.
- [ ] Fazer nova auditoria de superfície pública de `core/ciclo.py` antes de remoção/simplificação.
- [ ] Evoluir `ExecutionTrace` para spans/eventos/persistência somente quando houver necessidade real.
- [ ] Evoluir idempotência para persistência durável/multi-processo quando houver requisito de recuperação após crash.
- [ ] Implementar precondições, autorização explícita e recuperação/compensação antes de qualquer retry de efeito externo.
- [ ] Depois da estabilização de execução: evidência de pesquisa, economia computacional e evolução do World Model.

## Regra do próximo incremento
Idempotência está integrada ao caminho de ferramentas quando configurada, mas **retry de efeitos externos continua proibido automaticamente**. A próxima evolução de segurança deve ser orientada por evidência e testes.

Sequência obrigatória:

`Permission → Policy → Checkpoint → Idempotency → Tool → Observation → Verification → Audit → Result`

Qualquer retry externo futuro deverá depender de identidade de operação, autorização explícita, precondições e estratégia de recuperação verificável.