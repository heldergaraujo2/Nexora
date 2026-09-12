# 08 — ESTADO ATUAL

> Estado operacional do repositório e ponto de continuidade. A fonte de verdade é a convergência entre Git, testes, arquitetura e PROJECT_MEMORY. Para o HEAD exato e o último checkpoint validado, consulte sempre `PROJECT_MEMORY/15_HANDOFF.md`.

## Versão / estado
- Release histórica: `v1.0.0`, tag apontando para `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- O `main` continua evoluindo após `v1.0.0`; a versão de pacote permanece `1.0.0`.
- O runtime interno foi reforçado para transformar exceções de execução/verificação em observações controladas.
- O Orquestrador usa `AgenteRuntime` como proprietário do ciclo de execução de cada tarefa.
- A idempotência mínima foi integrada ao caminho governado de ferramentas.
- O roadmap pós-v1.0.0 foi formalizado nas Fases 17–25.
- A Fase 17 já iniciou com o primeiro Provider local oficial da arquitetura: `ProviderOllama`.

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
- Providers: base, Fake, Groq e agora Ollama local.

## Fase 17 — Local Intelligence Foundation
### Implementado neste incremento
- [x] `src/nexora/providers/ollama.py` criado como Provider oficial local.
- [x] Endpoint configurável por `NEXORA_OLLAMA_URL`, padrão `http://localhost:11434`.
- [x] Modelo configurável por `NEXORA_OLLAMA_MODEL`.
- [x] Perfil padrão inicial `qwen2.5-coder:7b-instruct-q4_K_M`.
- [x] Geração via `/api/chat` usando stdlib, sem dependências pip adicionais.
- [x] Health check via `/api/tags`, sem consumir geração.
- [x] Indisponibilidade HTTP/rede normalizada em `ProviderIndisponivel`.
- [x] Streaming e tool-calling não foram declarados até existir implementação/teste específicos.
- [x] Testes unitários do ProviderOllama.
- [x] Teste de integração RegistryProviders → ProviderManager → ProviderOllama com HTTP mockado.
- [x] ADR-015 formaliza o Provider local.

### Ainda pendente na Fase 17
- [ ] Validar o Provider contra uma instalação real do Ollama.
- [ ] Descobrir/listar modelos locais de forma estruturada para a futura camada de seleção.
- [ ] Definir perfis de modelo por capacidade/hardware sem fixar o hardware do criador na arquitetura.
- [ ] Preparar a futura detecção de CPU/RAM/GPU/VRAM/OS.

## Governança de execução
Fluxo canônico:

`Pedido → Permission → Policy → Checkpoint → Idempotency → Tool → Observation → Verification → Audit → Result`

A idempotência é aplicada quando configurada para a operação. O Orchestrator não executa ferramentas diretamente: delega ao Registry existente. A integração com AgentRuntime não contorna Permission/Policy/Checkpoint.

## Long-Term Autonomy
- `src/nexora/autonomia/registro.py` permanece preservado.
- `MetaLongoPrazo` e `RegistroAutonomia` continuam responsáveis por metas de longo prazo e persistência JSONL append-only.
- CLI `nexora autonomia definir|atualizar|listar|resumir` permanece parte do sistema.

## Próxima direção formal
1. **Fase 17 — Local Intelligence Foundation:** concluir validação/descoberta/configuração local.
2. **Fase 18 — Coding Workspace Agent:** ferramentas governadas para trabalhar em workspace real.
3. **Fase 19 — Dev Loop + Programming Experience:** ciclo automático de código/teste/erro/correção e aprendizado por experiências.
4. **Fase 20 — Code Knowledge + RAG:** recuperação contextual sobre código, testes, docs e histórico.
5. **Fase 21 — Intelligent Model Routing:** escolha de Provider/modelo por dificuldade, custo, risco e contexto.
6. **Fase 22 — Hardware & NEXORA Setup:** preparação para instalação/configuração simples conforme hardware.
7. **Fase 23 — NEXORA UI / Experience Layer:** interface extremamente tecnológica, futurista e inovadora, porém simples de usar.
8. **Fase 24 — Autonomous Product Engine:** fechamento progressivo do loop econômico do North Star.
9. **Fase 25 — Continuous Evolution:** evolução contínua com identidade, testes, proveniência e governança.

## Testes / CI
- A política operacional exige testes para toda funcionalidade nova.
- Mudanças que atravessam componentes exigem testes de integração.
- Testes escritos não são considerados equivalentes a testes aprovados.
- O CI correspondente ao commit anterior `f8fb7919...` passou em Python 3.11–3.14.
- O CI do novo HEAD desta etapa está em execução; portanto este incremento **ainda não é um checkpoint validado por CI**.

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
- Ollama foi integrado por contrato, mas a validação real em máquina com daemon/modelo instalado ainda está pendente.

## Estado de fase
**Fase 17 iniciada — ProviderOllama implementado e coberto por testes; CI do HEAD atual pendente.**
