# 15 — HANDOFF

> Arquivo principal de continuidade. Todo novo agente deve começar por este arquivo, confirmar o HEAD e verificar o CI antes de alterar código.

## Estado Atual
- Release histórica: `v1.0.0` → `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- HEAD de código validado: `f67f270c25609559264c19ef7a2561cc359873b8`.
- CI do HEAD de código: Run #138 (`34658836451`) — **SUCCESS** em Python 3.11, 3.12, 3.13 e 3.14.
- Depois da validação foram feitas apenas atualizações documentais sequenciais; o HEAD documental final é posterior ao HEAD de código validado.
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

## Fluxo de Ferramentas Fechado
Implementado no `RegistryFerramentas`:

`Pedido → Permission → Policy → Checkpoint → Tool → Observation → Verification → Audit → Result`

E integrado ao Orchestrator:

`Goal/Plan/Task → Orchestrator → Registry → Permission/Policy → Checkpoint → Tool → Observation → Verification → Audit → Result → Orchestrator`

Contrato:
- autorização ocorre antes da ação;
- checkpoint ocorre imediatamente antes da ferramenta;
- a ferramenta é o único executor da ação registrada;
- observação e verificação são opcionais para manter compatibilidade;
- quando configurados, produzem `ResultadoFerramenta`;
- `RegistroAuditoria` pode ser injetado no Registry;
- sucesso gera `ferramenta.resultado`;
- exceção do executor gera `ferramenta.falhou` e a exceção original é propagada;
- auditoria não copia parâmetros nem o resultado bruto, reduzindo risco de exposição de dados sensíveis;
- tarefas sem ferramenta continuam usando o caminho existente de Provider.

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

## Validação
- Correção do teste integrado para usar o argumento correto `origem=` no `PolicyEngine`.
- HEAD de código `f67f270c25609559264c19ef7a2561cc359873b8` validado por CI Run #138 (`34658836451`).
- Todos os quatro jobs do matrix Python 3.11–3.14 concluíram com `success`.
- A atualização documental subsequente não altera código executável.

## Limites / Lacunas verificadas
- Checkpoints ainda são em memória.
- Não existe rollback de efeitos externos.
- Registry/capabilities continuam em memória.
- Execução delegada é síncrona/in-memory.
- Ainda não existe ciclo autônomo completo de planejamento multi-agente, economia e evolução.
- YAML de políticas ainda não implementado.

## Testes / CI
- Foram adicionados testes para permission boundary, policy lifecycle, tool governance, Sandbox governance e Checkpoint Engine.
- `tests/unit/test_tools_registry.py` cobre auditoria de resultado, auditoria de falha e o fluxo observado/verificado.
- `tests/integration/test_orquestrador_ferramentas.py` cobre o caminho Orchestrator → Registry e confirma que o Provider não é chamado quando a tarefa usa ferramenta.
- CI Run #138 (`34658836451`) está verde em Python 3.11–3.14.

## Classificação arquitetural
Os componentes pós-release continuam classificados como **ADAPTAR/CRIAR dentro da arquitetura própria da NEXORA**. Não houve cópia de implementação privada externa.

## Próximo Passo
**Com o fluxo Orchestrator → Tool Registry validado, o próximo trabalho deve começar por uma auditoria arquitetural do limite entre Orchestrator, Agent Runtime e Delegation/Recovery, procurando especificamente se o caminho de ferramenta contorna sem querer o ciclo EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR.**

Não criar nova fase automaticamente.

Antes de qualquer novo componente:
1. confirmar o HEAD real;
2. verificar CI;
3. procurar implementação existente e documentação relacionada;
4. preservar Long-Term Autonomy e contratos atuais;
5. evitar duplicação e acoplamento prematuro;
6. só implementar depois de identificar a lacuna arquitetural concreta.

## Instruções para o próximo agente
1. Ler este HANDOFF e `08_CURRENT_STATE.md`.
2. Confirmar o HEAD real do `main`.
3. Verificar o CI do HEAD de código antes de alterar código.
4. Não assumir que v1.0.0 é o estado atual.
5. Não criar nova fase sem comando explícito do coordenador.
6. Antes de alterar um arquivo, ler seu conteúdo atual e trabalhar com o SHA atual.
7. Antes de implementar algo novo, procurar código, testes e PROJECT_MEMORY para evitar duplicação.
8. Preservar `Long-Term Autonomy` e os contratos já validados.
9. Manter GitHub como fonte de verdade e validar alterações com CI.
