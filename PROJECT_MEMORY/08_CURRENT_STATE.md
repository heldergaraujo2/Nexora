# 08 — ESTADO ATUAL

## Estado
- Fase 16 — Long-Term Autonomy: concluída e preservada.
- Fase 17 — Local Intelligence Foundation: em implementação.
- `ProviderOllama` implementado e integrado ao contrato de Providers.
- Descoberta de modelos locais adicionada sem acoplamento a um modelo específico.

## Fase 17 — progresso
- [x] Provider Ollama via HTTP stdlib.
- [x] Endpoint configurável (`NEXORA_OLLAMA_URL`).
- [x] Modelo configurável (`NEXORA_OLLAMA_MODEL`).
- [x] Perfil inicial Qwen2.5-Coder 7B Q4.
- [x] Health check `/api/tags`.
- [x] `listar_modelos()` no Provider.
- [x] `ModeloLocal` e `DescobridorModelosOllama`.
- [x] Testes unitários do Provider e descoberta.
- [x] Integração mockada Registry → Manager → Ollama.
- [ ] Teste contra daemon Ollama real.
- [ ] Seleção automática de perfil por hardware/capacidade.
- [ ] Detecção de CPU/RAM/GPU/VRAM/OS.

## Arquitetura canônica
`Objetivo → Orchestrator → Plano/Tarefas → AgentRuntime → Permission/Policy/Checkpoint → Idempotency (quando aplicável) → Provider/Tool → Observation → Verification → Analysis → Correction/Recovery → Retest → Audit/Experience → Trace → Result`.

Não criar terceiro Runtime. `core/ciclo.py` permanece legado/compatibilidade até migração segura.

## Governança
- Permission antes da ação.
- Policy default DENY.
- Checkpoint antes da ferramenta.
- Idempotência antes de efeitos externos quando configurada.
- Registry continua sendo a fronteira de execução governada das ferramentas.

## UI futura
A Fase 23 define uma UI extremamente tecnológica, futurista e inovadora, mas simples de usar. A interface deve comunicar a inteligência interna sem expor a complexidade arquitetural ao usuário.

## Próximas fases
17. Local Intelligence Foundation.
18. Coding Workspace Agent.
19. Dev Loop + Programming Experience.
20. Code Knowledge + RAG.
21. Intelligent Model Routing.
22. Hardware & NEXORA Setup.
23. NEXORA UI / Experience Layer.
24. Autonomous Product Engine.
25. Continuous Evolution.

## Testes
Toda funcionalidade nova exige testes; cruzamentos de componentes exigem integração. Teste escrito não equivale a teste aprovado. CI do HEAD deve ser verificado antes de fechar checkpoint.

## Limites conhecidos
Checkpoints/idempotência/registry ainda são in-memory; não há rollback de efeitos externos; World Model/Knowledge e Economy ainda não fecham o loop completo do North Star; Groq requer validação real; ExecutionTrace ainda não possui telemetria persistente universal.
