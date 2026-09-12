# 15 — HANDOFF

> **ARQUIVO PRINCIPAL DE CONTINUIDADE DA NEXORA.** GitHub é a fonte de verdade. Um novo agente deve confirmar o HEAD real de `main` e o CI correspondente antes de continuar.

## 1. Identidade imutável
- Nome: **NEXORA**.
- Slogan: **“NEXORA — Encontre oportunidades. Crie valor. Gere recursos.”**
- North Star longa: “Construir uma inteligência artificial capaz de aprender continuamente sobre o mundo, identificar oportunidades, criar valor através de produtos, serviços, software e inovação, transformar esse valor em recursos de forma legal e sustentável, e utilizar esses recursos para ampliar continuamente sua própria capacidade de criar ainda mais valor para seu criador.”
- North Star curta: “Criar valor continuamente para ampliar continuamente a capacidade de criar valor.”
- NEXORA é uma plataforma, não apenas um modelo de IA.
- Loop central: `OBSERVAR → PESQUISAR → ENTENDER → IDENTIFICAR OPORTUNIDADE → PLANEJAR → CRIAR → TESTAR → VALIDAR → LANÇAR → MEDIR → APRENDER → MELHORAR → GERAR RECURSOS → AMPLIAR CAPACIDADE → NOVA OPORTUNIDADE`.

## 2. Fonte de verdade
- Repositório: `heldergaraujo2/Nexora`.
- Branch oficial: `main`.
- Release histórica: `v1.0.0` → `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- Roadmap pós-v1.0: `PROJECT_MEMORY/07_ROADMAP.md`, Fases 17–25.
- Incremento atual de histórico provider/modelo: `3a221d9781fcff2b146deba5968c3e899c96d6de`.
- Documentação do checkpoint atual: `8a009deb0a305bd8a1f3fe14d0da1a3f0c0fd61c`.
- CI run #306 (`34712549133`) passou em Python 3.11, 3.12, 3.13 e 3.14.
- O run anterior #305 (`34710516102`) falhou em um teste que usava 3 sucessos + 2 falhas e esperava limiar de erro de 50%; 2/5 = 40%. O teste foi corrigido para 3 sucessos + 3 falhas e o novo CI ficou verde.

## 3. Arquitetura canônica atual

```text
Objetivo
  ↓
Orchestrator
  ↓
Plano / Tarefas
  ↓
Seleção do executor/agente
  ↓
Roteador Inteligente (decisão provider/modelo)
  ↓
AgentRuntime  ← proprietário do ciclo avançado
  ↓
Permission / Policy / Checkpoint
  ↓
Idempotency (quando configurada para a operação)
  ↓
Provider ou Tool
  ↓
Observation
  ↓
Verification
  ↓
Analysis
  ↓
Correction / Recovery
  ↓
Retest
  ↓
Audit / Experience
  ↓
ExecutionTrace
  ↓
Resultado
  ↓
Orchestrator
```

### Regra fundamental
**Não criar um terceiro ciclo de execução.** O Orchestrator coordena; o AgentRuntime executa o ciclo do agente. `core/ciclo.py` permanece legado/compatibilidade até migração segura.

## 4. ADRs de execução
### ADR-012
Orchestrator = coordenador de alto nível; AgentRuntime = limite canônico do ciclo de execução.

### ADR-013
`core/ciclo.py` permanece contrato legado/compatibilidade até evidência suficiente para migração segura.

### ADR-014
Idempotência é barreira explícita antes de efeitos externos; store atual é concorrente em memória e não habilita retry automático.

### ADR-015
`ProviderOllama` é integração local via contrato Provider, não dependência arquitetural obrigatória.

### ADR-016
Detecção inicial de hardware é conservadora, somente leitura e não presume GPU/VRAM que não possam ser detectadas com segurança.

### ADR-017
Roteamento inteligente é provider/modelo agnóstico, determinístico e explicável. Considera adequação do modelo, hardware, capabilities, health opcional e histórico operacional medido. O roteador decide; o AgentRuntime executa.

### ADR-018
Histórico do `ProviderManager` possui persistência JSON opcional, versionada, configurável por caminho explícito ou `NEXORA_PROVIDER_HISTORY_PATH`, com escrita atômica e tolerância a dados inválidos. O schema atual é v4 e inclui métricas por provider e por modelo, mantendo compatibilidade de leitura com schemas anteriores.

### ADR-021
Histórico específico `provider + modelo` é usado pelo roteamento quando há pelo menos 3 chamadas. Confiabilidade e latência não são misturadas entre modelos quando existe amostra específica suficiente. Custo usa somente telemetria real e pricing exato, também com amostra mínima de 3 gerações precificadas. Sem amostra específica suficiente, o roteador pode recorrer ao histórico agregado do provider.

## 5. Trabalho implementado e preservado
- AgentRuntime é o proprietário do ciclo `EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR`.
- ExecutionTrace transporta contexto estruturado e métricas reais quando disponíveis, sem inventar valores.
- Orchestrator encaminha tarefas para AgentRuntime e ferramentas para Registry.
- Idempotência mínima está integrada ao caminho governado de ferramentas.
- Long-Term Autonomy da Fase 16 permanece concluída e não deve ser substituída.

### Fase 17 — Local Intelligence Foundation
Implementado:
- `src/nexora/providers/ollama.py`.
- Configuração por ambiente e argumentos.
- Geração `/api/chat` com `stream=false`.
- Health check `/api/tags`.
- Normalização de indisponibilidade para `ProviderIndisponivel`.
- Descoberta estruturada de modelos locais.
- Perfis determinísticos de modelo.
- Detecção inicial de CPU/RAM/OS/arquitetura.
- Avaliação hardware × modelo e seleção de candidatos.
- Testes unitários e de integração correspondentes.

Pendente:
- validar contra Ollama real instalado;
- detecção detalhada de GPU/VRAM por plataforma;
- instalador/setup automático.

### Fase 21 — Intelligent Model Routing
Implementado:
- `RoteadorInteligente` provider/modelo agnóstico.
- Filtragem por registro, hardware e adequação do modelo.
- Requisitos opcionais de tool-calling, streaming, contexto e health.
- Métricas reais do `ProviderManager` por provider.
- Histórico mínimo de três chamadas antes de influenciar score.
- Histórico específico por `provider + modelo` para confiabilidade e latência.
- Fallback para histórico agregado do provider quando a amostra específica é insuficiente.
- Sinais determinísticos e explicáveis de sucesso, erro e latência relativa.
- Custo histórico específico por modelo somente com custo real medido e pelo menos três gerações precificadas.
- Ponte `routing_trace.py` para serialização da decisão.
- `Orquestrador` pode executar a decisão inteligente e instanciar o modelo selecionado via `ProviderManager.obter_com_modelo()`.
- `ExecutionTrace` recebe `provider`, `model` e `metadata.routing_decision` da execução real.
- Teste de integração cobre `RoteadorInteligente → Orquestrador → AgentRuntime → ExecutionTrace`.
- Histórico do `ProviderManager` pode ser persistido/recarregado por JSON versionado e caminho configurável.
- `ProviderManager.executar_instancia()` permite medir a instância já selecionada sem duplicar a chamada.
- `Orquestrador` alimenta as métricas reais do provider durante a execução governada pelo `AgentRuntime`.
- Telemetria real de tokens é propagada ao trace e persistida quando fornecida pelo provider.
- Compatibilidade com providers legados que retornam objetos com `.text` foi preservada.
- Testes unitários cobrem confiabilidade e latência específicas do modelo.
- CI run #306 (`34712549133`) passou em Python 3.11–3.14.

Próximo incremento recomendado:
1. definir um sinal de **qualidade/resultado de tarefa baseado em evidência real**, sem inventar métricas;
2. capturar resultado de verificação, critérios de sucesso e conclusão efetiva da tarefa;
3. futuramente manter histórico de qualidade por `tipo_de_tarefa + provider + modelo`;
4. só então incorporar qualidade ao score junto de capacidade, confiabilidade, latência, tokens e custo;
5. em paralelo, avançar Fase 18 quando a fundação de roteamento estiver suficientemente estável.

## 6. Governança — NÃO QUEBRAR
Fluxo canônico:
`Pedido → Permission → Policy → Checkpoint → Idempotency → Tool → Observation → Verification → Audit → Result`

- Policy default DENY.
- Permission ocorre antes da ação.
- Checkpoint ocorre antes da ferramenta.
- Idempotência, quando habilitada, ocorre antes do efeito.
- Registry é o executor governado da ferramenta.
- Orchestrator não deve executar ferramenta contornando o Registry.
- Sandbox é governança/controle de subprocesso, não isolamento OS forte.
- Auditoria JSONL é append-only por convenção, não prova criptográfica de imutabilidade.

## 7. Direção de desenvolvimento
1. **Fase 17 — Local Intelligence Foundation:** concluir validação/descoberta/configuração local.
2. **Fase 18 — Coding Workspace Agent:** ferramentas governadas para workspace real.
3. **Fase 19 — Dev Loop + Programming Experience:** código → teste → erro → correção → reteste → experiência.
4. **Fase 20 — Code Knowledge + RAG:** conhecimento recuperável sobre código e histórico.
5. **Fase 21 — Intelligent Model Routing:** seleção de modelo/provider por adequação, histórico medido, risco, contexto e custo real.
6. **Fase 22 — Hardware & NEXORA Setup:** instalação e configuração simples conforme hardware.
7. **Fase 23 — NEXORA UI / Experience Layer:** UI extremamente tecnológica/futurista/inovadora, mas simples e intuitiva.
8. **Fase 24 — Autonomous Product Engine:** aproximação do loop econômico completo.
9. **Fase 25 — Continuous Evolution:** evolução contínua governada.

## 8. Provider local e hardware
Hardware de desenvolvimento considerado: Ryzen 5 5600 + ~16 GB DDR4 + Radeon RX 6600 8 GB.

Esse hardware orienta o perfil inicial, mas **não é requisito fixo da NEXORA**.

O perfil inicial é um modelo de código local quantizado na classe Qwen2.5-Coder 7B Q4. O código permanece agnóstico ao modelo.

Ollama não é o núcleo da NEXORA; é apenas um Provider.

## 9. UI — requisito de produto
A UI final deve transmitir tecnologia, futuro, inovação, inteligência e sensação de sistema vivo **sem transformar isso em complexidade de uso**.

Regra: a complexidade fica na arquitetura interna; a interface principal permanece limpa, intuitiva e visualmente impactante.

## 10. Testes — regra permanente
Para cada funcionalidade nova:
1. implementar;
2. criar/atualizar testes;
3. executar os testes relevantes;
4. adicionar integração quando houver cruzamento de componentes;
5. validar CI correspondente ao HEAD;
6. atualizar PROJECT_MEMORY;
7. registrar commit/handoff.

**Nunca confundir teste escrito com teste aprovado.**

## 11. Limites reais
- Checkpoints são em memória.
- Não existe rollback de efeitos externos.
- Store de idempotência atual é em memória; não protege reinício de processo ou múltiplas instâncias.
- Não existe estratégia completa de recuperação de operações `IN_PROGRESS` após crash.
- Registry/capabilities continuam em memória.
- Histórico do ProviderManager agora pode sobreviver a reinicializações, recebe métricas do caminho real e possui métricas específicas por modelo, mas ainda não é distribuído.
- ExecutorDelegacoes é síncrono/in-memory.
- YAML de política não existe.
- World Model/Knowledge ainda são infraestrutura, não inteligência mundial completa.
- Economic Engine ainda não fecha o loop oportunidade → produto → mercado → receita → reinvestimento.
- Autonomia econômica completa ainda não existe.
- Groq ainda requer validação real HTTP/tool-calling antes de ser tratado como integração de produção validada.
- `ExecutionTrace` ainda não possui backend persistente/telemetria distribuída nem preenchimento universal de tokens/custo/policy/checkpoint.
- Ollama foi integrado por contrato, mas a validação real em máquina com daemon/modelo instalado ainda está pendente.
- A integração inteligente de roteamento está disponível de forma opt-in no Orchestrator; a configuração automática global de candidatos ainda é futura.
- Qualidade semântica da tarefa ainda não é sinal do roteador.
- Custo futuro não é previsto; somente custo real medido é considerado.

## 12. O que NÃO fazer
- Não criar outra NEXORA.
- Não criar outro repositório.
- Não criar outro Runtime de execução.
- Não duplicar Permission, Policy, Checkpoint ou Tool Registry.
- Não apagar Long-Term Autonomy.
- Não transformar NEXORA em wrapper de Ollama/Aider/Continue/OpenHands ou outro produto externo.
- Não tratar sandbox como isolamento OS forte.
- Não tratar auditoria como histórico criptograficamente inviolável.
- Não chamar infraestrutura de autonomia completa antes de fechar o loop real do North Star.
- Não introduzir retry de efeito externo sem idempotência, autorização, precondições e verificação.
- Não preencher métricas com valores inventados.
- Não remover `core/ciclo.py` apenas porque a busca interna não encontrou consumidores adicionais.
- Não transformar a UI em um painel complexo apenas para parecer tecnológico.

## 13. Regra operacional
A cada avanço significativo:
`AUDITAR → DECIDIR → IMPLEMENTAR → TESTAR → ATUALIZAR PROJECT_MEMORY → COMMIT → PUSH → VERIFICAR CI → HANDOFF`.

O repositório deve permanecer sempre em estado reproduzível e documentado. O North Star é a direção; testes, arquitetura e GitHub são as evidências do estado real.

## 14. Estado do checkpoint atual
- **CI do histórico provider/modelo: OK.** Run #306 (`34712549133`), Python 3.11/3.12/3.13/3.14: todos `success`.
- **HEAD funcional validado:** `3a221d9781fcff2b146deba5968c3e899c96d6de`.
- **HEAD de documentação:** `8a009deb0a305bd8a1f3fe14d0da1a3f0c0fd61c`.
- **Estado de testes:** CI verde após correção do teste de limiar de taxa de erro.
- **Checkpoint atual:** histórico específico por provider/modelo para confiabilidade/latência está validado.
- **Próxima ação:** projetar e implementar, com testes, um sinal de qualidade/resultado de tarefa baseado em evidência real antes de usar qualidade no roteamento.
