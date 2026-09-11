# 15 — HANDOFF

> Arquivo principal de continuidade. Todo novo agente deve começar por este arquivo, confirmar o HEAD e verificar o CI antes de alterar código.

## Estado Atual
- Release histórica: `v1.0.0` → `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- Último HEAD de código validado: `eccff2d3390807cfc0c7e839f6a055a0b1a867c5`.
- A documentação está sendo sincronizada com esse estado; os commits documentacionais subsequentes gerarão novo HEAD e novo CI.
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
- `PolicyEngine` mínimo com ALLOW/DENY e auditoria da decisão;
- loader declarativo TOML versionado para políticas;
- validação estrita do schema de política;
- rastreabilidade da decisão com versão e origem da política.

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
- `carregar_policy_toml()` fornece a entrada declarativa, mantendo parser e motor de decisão separados.

## Política declarativa
- Schema atual: `[policy]`, `version = 1`, `default = "deny"` e `[[policy.rules]]` com `effect`, `requester`, `executor` e `task` opcionais.
- Loader baseado em `tomllib`, sem dependência externa.
- Campos desconhecidos, versão inválida, tipos ambíguos, efeitos inválidos, regras malformadas e TOML inválido são rejeitados.
- Default continua sendo DENY e não há execução de código proveniente da configuração.
- `DecisaoPolitica` preserva `versao` e `origem`; a auditoria registra esses metadados.
- YAML permanece fora do escopo atual.

## Limites / Lacunas verificadas
- Ainda não há identidade explícita de regra/match ID na decisão auditada.
- Ainda não há fingerprint/hash do conteúdo da política; a origem identifica o caminho do arquivo.
- Não há hot reload de políticas.
- Não há estado `DENEGADA` no enum atual; por isso uma negação de política termina como `FALHOU`, com motivo auditado.
- Registry/capabilities continuam em memória.
- Execução delegada é síncrona/in-memory; não há fila distribuída, workers persistentes ou transporte externo.
- Ainda não existe um ciclo autônomo completo de planejamento multi-agente, execução, economia e evolução.

## Testes / CI
- Workflow de código `34649533683` confirmou Python 3.11, 3.12, 3.13 e 3.14: **success** em todos os jobs.
- A etapa de Policy teve uma falha inicial por ausência do pacote `nexora.experiencia`; `src/nexora/experiencia/__init__.py` foi criado/exportado e o CI posterior ficou verde.
- A suíte atual cobre delegação, runtime, recovery, experiência, auditoria, Policy ALLOW/DENY, loader TOML e metadados de rastreabilidade.
- Os commits documentacionais desta sincronização ainda precisam passar pelo CI antes de serem considerados o novo estado documental validado.

## Classificação arquitetural
Os componentes pós-release continuam classificados como **ADAPTAR/CRIAR dentro da arquitetura própria da NEXORA**, quando aplicável. Não houve cópia de implementação privada externa.

## Próximo Passo
**Não iniciar uma nova fase automaticamente.**

Próxima evolução recomendada para análise arquitetural: auditar a governança de decisão antes de implementar outro componente, especialmente:
1. identidade explícita da regra que produziu a decisão;
2. distinção semântica entre `DENY` e `FALHOU` / eventual estado `DENEGADA`;
3. fingerprint/hash da política para rastreabilidade forte;
4. lifecycle de carregamento e eventual reload seguro;
5. fronteira de permissões para ações sensíveis.

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
