# 08 — ESTADO ATUAL

## Estado
- Fase 16 — Long-Term Autonomy: concluída e preservada.
- Fase 17 — Local Intelligence Foundation: em implementação avançada.
- Fase 21 — Intelligent Model Routing: fundação implementada e integrada ao caminho real de execução.
- `ProviderOllama` implementado e integrado ao contrato de Providers.
- Descoberta de modelos locais, perfis, avaliação hardware × modelo e seleção de candidatos implementados.
- `RoteadorInteligente` considera adequação, hardware, capacidades declaradas, health opcional e histórico operacional real medido.
- `Orquestrador` pode usar o roteador inteligente para selecionar provider + modelo e registrar a decisão no `ExecutionTrace`.

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
- [x] Ponte de decisão para `ExecutionTrace.metadata`.
- [x] Integração real `RoteadorInteligente → Orquestrador → AgentRuntime → ExecutionTrace`.
- [x] Instanciação explícita do provider com o modelo selecionado, sem fallback silencioso.
- [x] Persistência opcional e versionada do histórico do `ProviderManager`.
- [x] Configuração por argumento ou `NEXORA_PROVIDER_HISTORY_PATH`.
- [x] Escrita atômica e tolerância a histórico inválido/incompatível.
- [x] Caminho real `Orquestrador → AgentRuntime → Provider` alimenta métricas do `ProviderManager` sem duplicar a execução.
- [x] Teste de integração confirma execução única, métricas atualizadas, persistência e trace correto.
- [x] Telemetria real de tokens no `ProviderManager` e no `ExecutionTrace`, sem estimativas.
- [x] Uso de tokens persistido no schema v2 do histórico do provider.
- [x] Teste de integração confirma tokens, métricas do manager, persistência e trace sem duplicar execução.
- [x] CI run `34704095484` passou em Python 3.11, 3.12, 3.13 e 3.14.
- [ ] Telemetria de custo real, somente quando houver pricing autoritativo/versionado por provider/modelo.

## Arquitetura canônica
`Objetivo → Orchestrator → Plano/Tarefas → Seleção de executor/agente → Roteador Inteligente → AgentRuntime → Permission/Policy/Checkpoint → Idempotency (quando aplicável) → Provider/Tool → Observation → Verification → Analysis → Correction/Recovery → Retest → Audit/Experience → ExecutionTrace → Result`.

O roteamento é decisão antes da execução; o provider/modelo escolhido é refletido no trace. O `AgentRuntime` continua sendo o único proprietário do ciclo de execução. `core/ciclo.py` permanece legado/compatibilidade até migração segura.

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
Checkpoints/idempotência/registry continuam em-memory; não há rollback de efeitos externos; World Model/Knowledge e Economy ainda não fecham o loop completo do North Star; Groq requer validação real; ExecutionTrace ainda não possui telemetria persistente universal. O histórico do ProviderManager agora pode sobreviver a reinicializações via JSON versionado e inclui tokens medidos quando o provider os fornece, mas ainda não é um backend distribuído. O custo permanece ausente quando não há pricing autoritativo; a NEXORA não estima custo. O roteamento inteligente está integrado ao caminho real, mas a descoberta automática de todos os candidatos e a telemetria universal continuam futuras.
