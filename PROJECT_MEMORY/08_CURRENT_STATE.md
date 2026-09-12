# 08 — ESTADO ATUAL

## Estado
- Fase 16 — Long-Term Autonomy: concluída e preservada.
- Fase 17 — Local Intelligence Foundation: em implementação avançada.
- Fase 21 — Intelligent Model Routing: fundação implementada e integrada ao caminho real de execução.
- `ProviderOllama` implementado e integrado ao contrato de Providers.
- Descoberta de modelos locais, perfis, avaliação hardware × modelo e seleção de candidatos implementados.
- `RoteadorInteligente` considera adequação, hardware, capacidades declaradas, health opcional e histórico operacional real medido por modelo quando há amostra suficiente.
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
- [x] Histórico específico por `provider + modelo` para chamadas, sucesso/erro e latência.
- [x] Quando há pelo menos 3 chamadas do par, confiabilidade e latência não misturam modelos diferentes do mesmo provider.
- [x] Fallback para histórico agregado do provider quando o par ainda não tem amostra suficiente.
- [x] Ajuste histórico deliberadamente limitado e explicável.
- [x] Amostra mínima de 3 chamadas antes de influenciar o score histórico.
- [x] Ponte de decisão para `ExecutionTrace.metadata`.
- [x] Integração real `RoteadorInteligente → Orquestrador → AgentRuntime → ExecutionTrace`.
- [x] Instanciação explícita do provider com o modelo selecionado, sem fallback silencioso.
- [x] Persistência opcional e versionada do histórico do `ProviderManager`.
- [x] Configuração por argumento ou `NEXORA_PROVIDER_HISTORY_PATH`.
- [x] Escrita atômica e tolerância a histórico inválido/incompatível.
- [x] Caminho real `Orquestrador → AgentRuntime → Provider` alimenta métricas do `ProviderManager` sem duplicar a execução.
- [x] Telemetria real de tokens no `ProviderManager` e no `ExecutionTrace`, sem estimativas.
- [x] Histórico evoluído para schema v3 com custo real e posteriormente v4 com métricas por modelo.
- [x] `PricingRegistry` versionado por provider/modelo, com fonte e data de vigência.
- [x] Preços públicos Groq para `openai/gpt-oss-120b` e `openai/gpt-oss-20b` registrados em snapshot 2026-09-12.
- [x] `ProviderManager` calcula custo somente com tokens reais + preço exato conhecido.
- [x] `ExecutionTrace.cost` recebe custo real no caminho do Orquestrador.
- [x] Roteador compara custo real por modelo, sem misturar modelos do mesmo provider.
- [x] Amostra mínima de 3 gerações precificadas permanece obrigatória para influência do custo.
- [x] Custo nunca substitui adequação funcional; ajuste máximo por custo: ±0.75 ponto.
- [x] Custo histórico pode ser explicitamente desativado com `considerar_custo=False`.
- [x] Testes dedicados cobrem separação/persistência por modelo, custo, amostra insuficiente e falhas por modelo.
- [x] Testes adicionais cobrem confiabilidade e latência específicas do modelo.
- [ ] CI do checkpoint atual ainda precisa ser confirmado verde no HEAD final.

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
Checkpoints/idempotência/registry continuam in-memory; não há rollback de efeitos externos; World Model/Knowledge e Economy ainda não fecham o loop completo do North Star; Groq requer validação real; ExecutionTrace ainda não possui telemetria persistente universal. O histórico do ProviderManager pode sobreviver a reinicializações via JSON versionado e inclui tokens medidos quando o provider os fornece, além de custo somente quando existe pricing autoritativo. O custo permanece desconhecido quando não há preço publicado ou uso mensurável; a NEXORA não estima custo. O snapshot de preços precisa ser atualizado quando os providers alterarem suas tarifas. O histórico de confiabilidade/latência agora é granular por provider/modelo quando existe amostra suficiente; ainda não representa qualidade semântica, valor da tarefa ou custo futuro previsto. A descoberta automática de todos os candidatos e a telemetria universal continuam futuras.
