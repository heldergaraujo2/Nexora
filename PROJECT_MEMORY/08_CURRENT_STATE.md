# 08 — ESTADO ATUAL

> Estado operacional do repositório e ponto de continuidade. A fonte de verdade é a convergência entre Git, testes, arquitetura e PROJECT_MEMORY. Para o HEAD exato e o último checkpoint validado, consulte sempre `PROJECT_MEMORY/15_HANDOFF.md`.

## Versão / estado
- Release histórica: `v1.0.0`, tag apontando para `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- O `main` continua evoluindo após `v1.0.0`; a versão de pacote permanece `1.0.0`.
- O runtime interno foi reforçado para transformar exceções de execução/verificação em observações controladas.
- O Orquestrador usa `AgenteRuntime` como proprietário do ciclo de execução de cada tarefa.
- A idempotência mínima foi integrada ao caminho governado de ferramentas.
- O roadmap pós-v1.0.0 foi formalizado nas Fases 17–25.

## Estado arquitetural real
A Fase 16 — Long-Term Autonomy continua concluída e preservada. A arquitetura evoluiu com Context, Knowledge, World Model, Objetivos, Strategy, comunicação, delegação, runtime, recuperação, experiência, auditoria, governança e idempotência.

### Componentes principais verificados
- Context, Knowledge, World Model, Goal e Strategy Engines.
- CommunicationBus, Delegacao e Agent Registry.
- `src/nexora/runtime/agente.py` — runtime generalista `EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR`.
- `src/nexora/runtime/observacao.py` — contrato de observação.
- `src/nexora/runtime/analise.py` — AnalisadorFalhas existente.
- `src/nexora/runtime/correcao.py` — Corrector.
- `src/nexora/runtime/checkpoint.py` — CheckpointEngine para snapshots lógicos em memória.
- `src/nexora/runtime/idempotencia.py` — barreira de idempotência em memória.
- `src/nexora/runtime/ferramenta.py` — contrato `ResultadoFerramenta`.
- `src/nexora/orquestracao/orquestrador.py` — coordenação de objetivos/tarefas com AgentRuntime.
- Experience, Audit, Policy, Permission, Tool Registry e Sandbox.
- Providers existentes incluem base, Fake e Groq; o próximo incremento operacional planejado é o Provider local via Ollama.

## Governança de execução
Fluxo canônico:

`Pedido → Permission → Policy → Checkpoint → Idempotency → Tool → Observation → Verification → Audit → Result`

A idempotência é aplicada quando configurada para a operação. O Orchestrator não executa ferramentas diretamente: delega ao Registry existente. A integração com AgentRuntime não contorna Permission/Policy/Checkpoint.

## Long-Term Autonomy
- `src/nexora/autonomia/registro.py` permanece preservado.
- `MetaLongoPrazo` e `RegistroAutonomia` continuam responsáveis por metas de longo prazo e persistência JSONL append-only.
- CLI `nexora autonomia definir|atualizar|listar|resumir` permanece parte do sistema.

## Próxima direção formal
O roadmap pós-v1.0 passa a priorizar, nesta ordem arquitetural inicial:
1. **Fase 17 — Local Intelligence Foundation:** `OllamaProvider`, configuração de modelos locais e testes de integração HTTP mockada.
2. **Fase 18 — Coding Workspace Agent:** ferramentas governadas para trabalhar em workspace real.
3. **Fase 19 — Dev Loop + Programming Experience:** ciclo automático de código/teste/erro/correção e aprendizado por experiências.
4. **Fase 20 — Code Knowledge + RAG:** recuperação contextual sobre código, testes, docs e histórico.
5. **Fase 21 — Intelligent Model Routing:** escolha de Provider/modelo por dificuldade, custo, risco e contexto.
6. **Fase 22 — Hardware & NEXORA Setup:** preparação para instalação/configuração simples conforme hardware.
7. **Fase 23 — NEXORA UI / Experience Layer:** interface extremamente tecnológica, futurista e inovadora, porém simples de usar.
8. **Fase 24 — Autonomous Product Engine:** fechamento progressivo do loop econômico do North Star.
9. **Fase 25 — Continuous Evolution:** evolução contínua com identidade, testes, proveniência e governança.

A ordem pode ser ajustada por evidência técnica, mas a direção está formalizada.

## Testes / CI
- A política operacional exige testes para toda funcionalidade nova.
- Mudanças que atravessam componentes exigem testes de integração.
- Testes escritos não são considerados equivalentes a testes aprovados.
- CI só pode ser marcado como OK quando o run correspondente ao HEAD concluir com sucesso.
- Antes de iniciar a Fase 17, o estado exato do HEAD e seu CI correspondente deve ser confirmado.

## Limites atuais verificados
- `core/ciclo.py` ainda existe como caminho legado e não deve ser removido até consumidores/testes serem migrados com segurança.
- Checkpoints não possuem persistência durável.
- Não existe rollback de efeitos externos.
- Store de idempotência atual é em memória; não protege reinício de processo ou múltiplas instâncias.
- Não existe estratégia completa de recuperação de operações `IN_PROGRESS` após crash.
- Registry/capabilities são em memória.
- ExecutorDelegacoes é síncrono/in-memory.
- YAML de políticas não foi implementado.
- World Model/Knowledge ainda são infraestrutura, não inteligência mundial completa.
- Economic Engine ainda não fecha o loop oportunidade → produto → mercado → receita → reinvestimento.
- Autonomia econômica completa ainda não existe.
- Groq ainda requer validação real HTTP/tool-calling antes de ser tratado como integração de produção validada.
- `ExecutionTrace` ainda não possui backend persistente/telemetria distribuída nem preenchimento universal de tokens/custo/policy/checkpoint.

## Estado de fase
**Roadmap pós-v1.0 formalizado; próxima fase planejada: Fase 17 — Local Intelligence Foundation.**
