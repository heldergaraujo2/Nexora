# 15 — HANDOFF

> Arquivo principal de continuidade. Todo novo agente deve começar por este arquivo, confirmar o HEAD e verificar o CI antes de alterar código.

## Estado Atual
- Release histórica: `v1.0.0` → `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- HEAD de código validado antes desta atualização documental: `68c93b0dc6710fc375fcff237f38737467f245a5`.
- A documentação está sendo sincronizada com esse estado; os commits documentacionais subsequentes devem gerar novo HEAD e novo CI.
- O projeto não está congelado em v1.0.0.
- Não foi criada uma nova fase.

## Onde Parou
A Fase 16 — Long-Term Autonomy permanece concluída e preservada.

Depois dela foram implementados e validados:
- Context Engine;
- Knowledge Engine;
- World Model Engine;
- Goal Engine;
- Strategy Engine;
- Communication Bus;
- Agent Runtime / Orchestrator com comunicação;
- DelegadorAgentes;
- Agent Registry / Capability Registry;
- delegação por capacidade;
- `ExecutorDelegacoes`;
- integração de delegação com `AgenteRuntime`;
- recovery de delegações;
- registro de experiências;
- auditoria append-only;
- `PolicyEngine` mínimo com ALLOW/DENY e auditoria da decisão.

## Arquitetura real da execução delegada
`Delegação → Policy → ALLOW/DENY → Executor → Runtime/Verificação → Recovery → Experiência + Auditoria`

- `AgenteRegistro` descreve agente, capacidades, tags, prioridade, disponibilidade e metadados.
- `RegistroAgentes` registra, lista, descobre por capacidade e seleciona deterministicamente o melhor agente disponível.
- `CommunicationBus` transporta mensagens e mantém correlação/estado; não executa providers nem ferramentas.
- `DelegadorAgentes` cria e publica delegações.
- `ExecutorDelegacoes` recebe solicitações, consulta a Policy, executa handlers/runtimes registrados e atualiza o estado terminal.
- `AgenteRuntime` mantém o ciclo de execução/verificação/análise/correção/reteste.
- Recovery de delegação trata falhas do handler até `max_tentativas`.
- `RegistroExperiencias` registra o resultado terminal.
- `RegistroAuditoria` persiste eventos relevantes em JSONL append-only.
- `PolicyEngine` aplica regras ordenadas e default DENY antes da execução.

## Limites / Lacunas verificadas
- Policy ainda é um MVP em memória, com regras construídas em código.
- ADR-009 prevê política declarativa/versionada em TOML/YAML; ainda falta o loader declarativo e seu versionamento/validação.
- Não há estado `DENEGADA` no enum atual; por isso uma negação de política termina como `FALHOU`, com motivo auditado.
- Registry/capabilities continuam em memória.
- Execução delegada é síncrona/in-memory; não há fila distribuída, workers persistentes ou transporte externo.
- Ainda não existe um ciclo autônomo completo de planejamento multi-agente, execução, economia e evolução.

## Testes / CI
- Última evidência verde de código: workflow `34647078404`.
- Python 3.11, 3.12, 3.13 e 3.14: **success**.
- A etapa de Policy teve uma falha inicial por ausência do pacote `nexora.experiencia`; `src/nexora/experiencia/__init__.py` foi criado/exportado e o CI posterior ficou verde.
- A suíte atual cobre delegação, runtime, recovery, experiência, auditoria e Policy ALLOW/DENY além dos componentes anteriores.

## Classificação arquitetural
Os componentes pós-release continuam classificados como **ADAPTAR/CRIAR dentro da arquitetura própria da NEXORA**, quando aplicável. Não houve cópia de implementação privada externa.

## Próximo Passo
**Não iniciar uma nova fase automaticamente.**

Próxima evolução recomendada para análise arquitetural: avaliar a transformação do `PolicyEngine` MVP em uma política declarativa/versionada compatível com ADR-009 (TOML/YAML), incluindo validação, carregamento seguro, versionamento e auditoria, antes de implementar.

Essa é uma recomendação técnica, não uma autorização automática de implementação.

## Instruções para o próximo agente
1. Ler este HANDOFF e `08_CURRENT_STATE.md`.
2. Confirmar o HEAD real do `main`.
3. Verificar o CI do HEAD real antes de alterar código.
4. Não assumir que v1.0.0 é o estado atual.
5. Não criar nova fase sem comando explícito do coordenador.
6. Antes de alterar um arquivo, ler seu conteúdo atual e trabalhar com o SHA atual.
7. Antes de implementar algo novo, procurar código, testes e PROJECT_MEMORY para evitar duplicação.
8. Preservar `Long-Term Autonomy` e os contratos já validados.
9. Manter GitHub como fonte de verdade e validar alterações com CI.
