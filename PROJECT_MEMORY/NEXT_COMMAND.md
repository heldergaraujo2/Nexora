# NEXT COMMAND — CHECKPOINT RUNTIME FECHADO

> Canal de continuidade da coordenação da NEXORA. A release `v1.0.0` continua válida como marco histórico; o código avançou depois dela.

## Estado atual

- O HEAD real deve ser obtido diretamente do `main` no início de cada sessão.
- Último checkpoint de código executável validado: `d69e7c9947dfc79fdd51f28dae66e97a0d3e75f4`.
- Run #147 (`34659962617`) foi SUCCESS em Python 3.11, 3.12, 3.13 e 3.14.
- A suíte registrou 232 testes passando em Python 3.14.
- Os 2 warnings encontrados nesse run foram corrigidos em `tests/unit/test_policy_loader.py` no commit `a608056d700519f2f62447f23c1148bd621c4be2`.
- As alterações posteriores foram de documentação/continuidade.
- Long-Term Autonomy permanece concluída e preservada.
- Nenhuma nova fase foi criada.

## Checkpoint fechado

A consistência interna do Runtime foi reconciliada.

Coding Agent e Research Agent agora passam o erro de validação por `Observacao.erro` para o `AnalisadorFalhas` e mantêm falhas de validação corrigíveis como retentáveis.

O ciclo do Runtime permanece:

`EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR`

## Próximo trabalho

**Auditar e reconciliar `Orquestrador` ↔ `AgenteRuntime`.**

Hoje existem dois caminhos:

`Orquestrador → ExecutorCiclo → VerificadorCiclo`

`AgenteRuntime → EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR`

A próxima implementação deve evitar dupla execução/verificação e preservar as responsabilidades:
- Orchestrator: objetivo, plano, tarefas, dependências e lifecycle.
- AgentRuntime: ciclo de execução avançado, análise, correção, recovery e reteste.
- Registry: fronteira de execução de ferramentas.
- Permission/Policy/Checkpoint: governança antes da ação.
- Provider: fronteira de inteligência/modelo.

## Regras de continuidade

1. Confirmar HEAD real.
2. Verificar CI do HEAD real.
3. Ler `PROJECT_MEMORY/15_HANDOFF.md`.
4. Ler `PROJECT_MEMORY/08_CURRENT_STATE.md` e `13_CHANGELOG.md`.
5. Auditar arquivos e testes existentes antes de editar.
6. Não criar uma segunda NEXORA.
7. Não criar nova fase automaticamente.
8. Não duplicar componentes já existentes.
9. Usar SHA atual de cada arquivo antes de atualizar.
10. Validar toda alteração com testes e CI Python 3.11–3.14.
11. Atualizar a continuidade após a validação.

## Observação de tooling

`src/nexora/runtime/analise.py` apresenta uma anomalia registrada no HANDOFF: o SHA exposto pelo Git tree aparece com 39 caracteres. Não inventar SHA nem forçar atualização desse arquivo; resolver a identidade do blob antes de qualquer alteração.
