# 15 — HANDOFF

> Arquivo principal de continuidade. Todo novo agente deve começar por este arquivo, confirmar o HEAD e verificar o CI antes de alterar código.

## Estado Atual
- Release histórica: `v1.0.0` → `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- Último HEAD implementado: `8745681cb21a71690a2360f0b7851ca2d3e50027`.
- CI específico desse HEAD: ainda não há workflow associado retornado pelo conector; portanto **não declarar CI verde** para os commits mais recentes.
- O projeto não está congelado em v1.0.0.
- Não foi criada uma nova fase.

## Onde Parou
A Fase 16 — Long-Term Autonomy permanece concluída e preservada.

Depois dela foram implementados:
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
- rastreabilidade da decisão com versão e origem;
- identidade explícita e única das regras;
- fingerprint canônico SHA-256 do conteúdo semântico;
- distinção entre negação de política e falha de execução por `EstadoDelegacao.DENEGADA`;
- `GerenciadorPermissoes` / `PedidoPermissao` como fronteira explícita antes de ações sensíveis;
- `GerenciadorPolitica` com reload validado e troca atômica da política ativa;
- integração da fronteira de permissões ao `RegistryFerramentas`;
- integração da fronteira de permissões ao `Sandbox`, preservando a allowlist e impedindo `subprocess.run` quando a política nega.

## Arquitetura real da execução
`Pedido → Permission → Policy → Sandbox/Tool → Checkpoint → Observation → Verification → Audit → Result`

Para delegação, permanece:
`Delegação → Policy → ALLOW/DENY → Executor → Runtime/Verificação → Recovery → Experiência + Auditoria`

- `AgenteRegistro` descreve agente, capacidades, tags, prioridade, disponibilidade e metadados.
- `CommunicationBus` transporta mensagens e mantém correlação/estado; não executa providers nem ferramentas.
- `ExecutorDelegacoes` recebe solicitações, consulta a Policy, executa handlers/runtimes registrados e atualiza o estado terminal.
- `AgenteRuntime` mantém o ciclo de execução/verificação/análise/correção/reteste.
- `RegistroExperiencias` registra o resultado terminal.
- `RegistroAuditoria` persiste eventos relevantes em JSONL append-only.
- `PolicyEngine` aplica regras ordenadas e default DENY antes da execução.
- `GerenciadorPermissoes` avalia pedidos e audita a decisão, sem executar a ação.
- `GerenciadorPolitica` permite reload somente após carregamento/validação, mantendo a política anterior se a nova for rejeitada.
- `RegistryFerramentas` pode operar sem governança para compatibilidade retroativa, ou exigir permissão antes do executor.
- `Sandbox` mantém sua allowlist; quando configurado com `GerenciadorPermissoes`, a política é verificada antes do subprocesso.
- A auditoria do Sandbox registra apenas o comando-base no contexto de permissão, evitando registrar argumentos potencialmente sensíveis.

## Política declarativa
- Schema atual: `[policy]`, `version = 2`, `default = "deny"` e `[[policy.rules]]` com `id` obrigatório, `effect`, `requester`, `executor` e `task` opcionais.
- Cada regra possui identidade explícita, não vazia e única.
- `DecisaoPolitica.regra_id` identifica deterministicamente a regra vencedora.
- `PolicyEngine` calcula fingerprint SHA-256 canônico sobre versão, default e regras semânticas, preservando ordem e excluindo origem.
- Auditoria registra `regra_id`, efeito, permitido, motivo, versão, origem e fingerprint.
- Loader usa `tomllib`, sem dependência externa, e não executa código da configuração.
- Campos desconhecidos, versão inválida, tipos ambíguos, efeitos inválidos, IDs ausentes/duplicados, regras malformadas e TOML inválido são rejeitados.
- Default continua DENY. YAML permanece fora do escopo.

## Estado de delegação e governança
- `DENEGADA` representa decisão de governança que impede a execução antes do handler.
- `FALHOU` continua reservado para falhas reais de execução/verificação ou recovery esgotado.
- Uma negação gera os eventos de decisão/negação previstos na auditoria e preserva `delegacao.resultado`.
- `tentativas` permanece `0` quando a política nega a execução.

## Limites / Lacunas verificadas
- Não há CI confirmado para os dois últimos commits desta etapa.
- Não existe ainda um `Checkpoint` concreto no runtime; a palavra checkpoint na cadeia arquitetural representa o próximo boundary a implementar.
- Registry/capabilities continuam em memória.
- Execução delegada é síncrona/in-memory; não há fila distribuída, workers persistentes ou transporte externo.
- Ainda não existe ciclo autônomo completo de planejamento multi-agente, economia e evolução.

## Testes / CI
- CI anteriormente validado: workflow `34653209175`, Python 3.11–3.14, todos os jobs success no HEAD histórico `dec0bbd4430bbe5883476112704ea78c97b90be3`.
- Foram adicionados testes específicos para `GerenciadorPermissoes`, `GerenciadorPolitica`, Registry de ferramentas governado e Sandbox governado.
- O arquivo `tests/unit/test_sandbox_governanca.py` cobre compatibilidade sem política, ALLOW, DENY sem subprocesso, precedência da allowlist e auditoria da decisão.
- A validação desses testes ainda precisa ser executada pelo CI ou por ambiente local antes de marcar o HEAD atual como validado.

## Classificação arquitetural
Os componentes pós-release continuam classificados como **ADAPTAR/CRIAR dentro da arquitetura própria da NEXORA**. Não houve cópia de implementação privada externa.

## Próximo Passo
**Checkpoint Engine mínimo**, somente após validar o conjunto atual.

Objetivo do próximo bloco:
1. procurar novamente por qualquer implementação parcial de checkpoint/persistência de estado;
2. definir contrato mínimo de checkpoint sem duplicar `execution_store` ou memória existente;
3. criar checkpoint explícito entre Permission/Policy e execução quando necessário;
4. integrar com Tool/Sandbox somente se o contrato justificar;
5. testar criação, recuperação, idempotência e auditoria.

Não iniciar nova fase. Preservar todos os contratos existentes.

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
