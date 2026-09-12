# 08 — ESTADO ATUAL

## Estado
- Fase 16 — Long-Term Autonomy: concluída e preservada.
- Fase 17 — Local Intelligence Foundation: em implementação avançada.
- Fase 21 — Intelligent Model Routing: fundação implementada e validada em CI.
- `ProviderOllama` implementado e integrado ao contrato de Providers.
- Descoberta de modelos locais, perfis, avaliação hardware × modelo e seleção de candidatos implementados.
- `RoteadorInteligente` agora considera adequação, hardware, capacidades declaradas, health opcional e histórico operacional real medido.

## Fase 17 — progresso
- [x] Provider Ollama via HTTP stdlib.
- [x] Endpoint configurável (`NEXORA_OLLAMA_URL`).
- [x] Modelo configurável (`NEXORA_OLLAMA_MODEL`).
- [x] Perfil inicial Qwen2.5-Coder 7B Q4.
- [x] Health check `/api/tags`.
- [x] `listar_modelos()` no Provider.
- [x] `ModeloLocal` e `DescobridorModelosOllama`.
- [x] Perfis determinísticos de capacidade de modelo.
- [x] Detecção conservadora inicial de CPU/RAM/OS/arquitetura.
- [x] Avaliação hardware × modelo.
- [x] Seleção determinística de modelos adequados.
- [ ] Detecção detalhada de GPU/VRAM por plataforma.
- [ ] Teste contra daemon Ollama real.
- [ ] Instalador/setup automático.

## Fase 21 — Intelligent Model Routing
- [x] Roteador provider/modelo provider-agnostic.
- [x] Filtragem de providers registrados.
- [x] Validação de tool-calling, streaming e contexto.
- [x] Health opcional como requisito de seleção.
- [x] Score determinístico de adequação do modelo.
- [x] Histórico medido de chamadas, sucesso, erro e latência média.
- [x] Ajuste histórico deliberadamente limitado e explicável.
- [x] Amostra mínima de 3 chamadas antes de influenciar o score.
- [x] Testes unitários do histórico e do roteamento.
- [x] CI verde em Python 3.11, 3.12, 3.13 e 3.14.
- [ ] Integrar decisão de roteamento ao `ExecutionTrace` de forma estruturada.
- [ ] Persistir histórico de métricas para sobreviver a reinicialização.
- [ ] Incorporar custo/tokens somente quando houver telemetria real e confiável.

## Arquitetura canônica
`Objetivo → Orchestrator → Plano/Tarefas → AgentRuntime → Permission/Policy/Checkpoint → Idempotency (quando aplicável) → Provider/Tool → Observation → Verification → Analysis → Correction/Recovery → Retest → Audit/Experience → Trace → Result`.

Roteamento ocorre como decisão antes da execução do provider e não cria Runtime paralelo. `core/ciclo.py` permanece legado/compatibilidade até migração segura.

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
Toda funcionalidade nova exige testes; cruzamentos de componentes exigem integração. Teste escrito não equivale a teste aprovado. O CI do HEAD deve ser verificado antes de fechar checkpoint.

## Limites conhecidos
Checkpoints/idempotência/registry e histórico atual de ProviderManager ainda são in-memory; não há rollback de efeitos externos; World Model/Knowledge e Economy ainda não fecham o loop completo do North Star; Groq requer validação real; ExecutionTrace ainda não possui telemetria persistente universal.
