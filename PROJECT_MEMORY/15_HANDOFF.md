# 15 — HANDOFF

> Arquivo principal de continuidade. Todo novo agente deve começar por este arquivo, confirmar o HEAD e verificar o CI antes de alterar código.

## Estado Atual
- Release histórica: `v1.0.0` → `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- Último HEAD implementado nesta etapa: `5e022a6a2b9d6df031deb17fd4983b8d5860ee90`.
- CI específico desse HEAD: ainda não confirmado; **não declarar CI verde**.
- O projeto continua evoluindo após v1.0.0 sem criar nova fase.

## Onde Parou
A Fase 16 — Long-Term Autonomy permanece concluída e preservada.

Depois dela foram implementados Context, Knowledge, World Model, Goal, Strategy, Communication Bus, Runtime/Orchestrator, Delegation, Agent Registry, capability delegation, recovery, experiência, auditoria e a camada de governança.

Governança atual:
- `PolicyEngine` mínimo com ALLOW/DENY e default DENY;
- loader TOML versionado e validação estrita;
- fingerprint canônico SHA-256;
- `DENEGADA` separado de falha real;
- `GerenciadorPermissoes` / `PedidoPermissao` como fronteira de autorização;
- `GerenciadorPolitica` com reload validado e troca atômica;
- Registry de ferramentas e Sandbox podem exigir Policy antes da execução.

## Checkpoint Engine
Implementado em `src/nexora/runtime/checkpoint.py`.

Contrato atual:
- `Checkpoint` identifica `id`, `execucao_id`, estado lógico, motivo e carimbo UTC.
- `CheckpointEngine.criar()` captura uma cópia profunda do estado.
- `CheckpointEngine.obter()` recupera o snapshot isolado.
- `CheckpointEngine.recuperar()` devolve nova cópia do estado e registra auditoria quando configurada.
- `CheckpointEngine.listar()` permite filtrar por execução.
- O engine não executa ferramentas, não chama subprocessos e não desfaz efeitos externos.
- Auditoria opcional reutiliza `RegistroAuditoria`.
- O componente é deliberadamente em memória nesta etapa; persistência durável e rollback externo ficam fora do MVP.

## Arquitetura real da execução
`Pedido → Permission → Policy → Sandbox/Tool → Checkpoint → Observation → Verification → Audit → Result`

Para delegação, permanece:
`Delegação → Policy → ALLOW/DENY → Executor → Runtime/Verificação → Recovery → Experiência + Auditoria`

O Checkpoint Engine é um boundary de estado, não um executor. A integração automática com Tool/Sandbox ainda não foi feita para evitar acoplamento prematuro.

## Limites / Lacunas verificadas
- CI não confirmado para o HEAD atual.
- Checkpoints ainda são em memória.
- Não existe rollback de efeitos externos.
- Registry/capabilities continuam em memória.
- Execução delegada é síncrona/in-memory.
- Ainda não existe ciclo autônomo completo de planejamento multi-agente, economia e evolução.

## Testes / CI
- Foram adicionados testes para permission boundary, policy lifecycle, tool governance, Sandbox governance e Checkpoint Engine.
- `tests/unit/test_checkpoint.py` cobre isolamento do snapshot, recuperação sem mutação, filtro por execução, auditoria e validações.
- A validação final do HEAD atual precisa ser obtida por CI ou ambiente local antes de marcar o estado como validado.

## Classificação arquitetural
Os componentes pós-release continuam classificados como **ADAPTAR/CRIAR dentro da arquitetura própria da NEXORA**. Não houve cópia de implementação privada externa.

## Próximo Passo
**Validar o conjunto atual e, depois, projetar a integração do Checkpoint com o fluxo de execução somente se houver contrato claro.**

Antes de qualquer novo componente:
1. confirmar o HEAD real;
2. verificar CI;
3. procurar implementação existente e documentação relacionada;
4. preservar Long-Term Autonomy e contratos atuais;
5. evitar duplicação e acoplamento prematuro.

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
