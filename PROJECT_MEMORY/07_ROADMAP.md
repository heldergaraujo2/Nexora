# 07 — ROADMAP

## Roadmap Global — histórico canônico

```
FASE PRÉVIA · CAPABILITY DISCOVERY · CONCLUÍDA
FASE ZERO   · CONTINUIDADE E MEMÓRIA · CONCLUÍDA
FASE UM     · FUNDAÇÃO · CONCLUÍDA
FASE DOIS   · PROVIDER SYSTEM · CONCLUÍDA
FASE TRÊS   · CONTEXTO E MEMÓRIA · CONCLUÍDA
FASE QUATRO · PLANEJAMENTO · CONCLUÍDA
FASE 4.5    · MULTI-AGENT ORCHESTRATION · CONCLUÍDA
FASE CINCO  · NEXORA AGENT RUNTIME · CONCLUÍDA
FASE SEIS   · CODING AGENT · CONCLUÍDA
FASE SETE   · RESEARCH ENGINE · CONCLUÍDA
FASE OITO   · EXPERIENCE ENGINE · CONCLUÍDA
FASE NOVE   · EXPERIMENTATION ENGINE · CONCLUÍDA
FASE DEZ    · EVOLUTION ENGINE · CONCLUÍDA
FASE ONZE   · ECONOMIC ENGINE · CONCLUÍDA
FASE DOZE   · SECURITY ENGINE · CONCLUÍDA
FASE TREZE  · MEMORY ENGINE · CONCLUÍDA
FASE QUATORZE · RESOURCE MANAGEMENT · CONCLUÍDA
FASE QUINZE · PORTFOLIO ENGINE · CONCLUÍDA
FASE DEZESSEIS · LONG-TERM AUTONOMY · CONCLUÍDA
```

## Reconciliação de numeração
A numeração histórica acima permanece canônica e baseada nos commits reais das fases 11–16:
- Fase 11: Economic Engine
- Fase 12: Security Engine
- Fase 13: Memory Engine
- Fase 14: Resource Management
- Fase 15: Portfolio Engine
- Fase 16: Long-Term Autonomy (`v1.0.0`)

A referência antiga que chamava Long-Term Autonomy de Fase 14 estava dessincronizada com a implementação real.

## Evolução pós-v1.0.0
A evolução pós-release passa agora a ter uma direção explícita. Ela **não substitui nem reabre a Fase 16**: a Long-Term Autonomy permanece concluída e protegida.

A prioridade daqui em diante é transformar a infraestrutura já construída em uma NEXORA operacionalmente capaz de trabalhar como uma inteligência de desenvolvimento e, progressivamente, como uma inteligência geral orientada ao North Star.

### Princípio arquitetural
NEXORA não será um simples wrapper de Ollama, Aider, Continue, OpenHands ou de qualquer outro agente/modelo. Esses componentes podem ser Providers, executores, referências ou integrações especializadas. A inteligência, governança, memória, planejamento, experiência, verificação e evolução devem continuar pertencendo à arquitetura NEXORA.

---

# ROADMAP PÓS-v1.0 — NOVA LINHA DE EVOLUÇÃO

## FASE 17 · LOCAL INTELLIGENCE FOUNDATION
**Objetivo:** tornar a NEXORA capaz de utilizar inteligência local de forma econômica, offline e controlada.

### Entregas
- `OllamaProvider` como Provider oficial da arquitetura.
- Descoberta/configuração de modelos locais.
- Perfil inicial recomendado para hardware intermediário: Qwen2.5-Coder 7B quantizado, sem tornar o sistema dependente desse modelo.
- Health check e tratamento de indisponibilidade do runtime local.
- Configuração por ambiente/modelo.
- Testes unitários e integração HTTP mockada.
- Preparação para detecção futura de CPU/RAM/GPU/VRAM/OS.

### Critério de conclusão
NEXORA consegue executar tarefas por Provider local sem quebrar Providers existentes e sem depender de internet.

---

## FASE 18 · CODING WORKSPACE AGENT
**Objetivo:** transformar o Coding Agent em um agente operacional capaz de trabalhar em um workspace real sob governança.

### Ferramentas-alvo
- leitura e busca de arquivos;
- edição/criação controlada;
- execução de comandos;
- execução de testes;
- inspeção de diff/status;
- operações Git governadas;
- observação de resultados;
- recuperação de falhas.

### Regra
Toda ferramenta atravessa a cadeia de governança existente. Não criar um segundo executor paralelo.

### Critério de conclusão
A NEXORA consegue receber uma tarefa de programação, alterar um workspace autorizado, executar testes, analisar falhas, corrigir e retestar usando o AgentRuntime canônico.

---

## FASE 19 · DEV LOOP + PROGRAMMING EXPERIENCE
**Objetivo:** fechar o ciclo de desenvolvimento iterativo e fazer a NEXORA aprender com o próprio trabalho.

### Loop canônico
`TAREFA → ENTENDER → PLANEJAR → EDITAR → TESTAR → OBSERVAR ERRO → ANALISAR → CORRIGIR → RETESTAR → VALIDAR → REGISTRAR EXPERIÊNCIA`

### Entregas
- experiências de programação estruturadas;
- registro de falhas e soluções;
- decisões técnicas reutilizáveis;
- relação entre mudança, teste, erro e correção;
- recuperação de experiências relevantes antes de novas tarefas;
- métricas do ciclo de desenvolvimento.

### Critério de conclusão
Uma falha já conhecida pode ser recuperada como experiência e utilizada para melhorar uma nova execução, sem inventar conhecimento.

---

## FASE 20 · CODE KNOWLEDGE + RAG
**Objetivo:** criar memória recuperável sobre o próprio código, documentação e histórico de desenvolvimento.

### Fontes
- código;
- testes;
- documentação;
- PROJECT_MEMORY;
- commits;
- diffs;
- issues;
- falhas;
- soluções;
- decisões;
- experiências.

### Requisito
O sistema deve preservar proveniência e diferenciar fato, evidência, inferência e hipótese.

### Critério de conclusão
A NEXORA consegue localizar contexto relevante do próprio projeto antes de planejar alterações, reduzindo repetição de erros e perda de contexto.

---

## FASE 21 · INTELLIGENT MODEL ROUTING
**Objetivo:** escolher automaticamente o Provider/modelo adequado ao custo, dificuldade, risco e contexto da tarefa.

### Estratégia inicial
- modelo local para tarefas simples/repetitivas;
- Provider remoto de maior capacidade quando necessário;
- Groq como Provider disponível, sem exclusividade;
- fallback controlado;
- limites de custo e orçamento;
- telemetria real de latência/tokens/custo quando disponível.

### Regra
Routing não pode contornar Permission, Policy, Checkpoint, Idempotency, Audit ou Verification.

### Critério de conclusão
NEXORA escolhe o recurso computacional de forma automática e justificável, mantendo controle de custo e risco.

---

## FASE 22 · HARDWARE & NEXORA SETUP
**Objetivo:** preparar a distribuição da NEXORA para usuários instalarem o sistema sem configuração técnica complexa.

### Visão futura
Um instalador `NEXORA-Setup` deverá:
- detectar CPU, RAM, GPU, VRAM, sistema operacional e espaço disponível;
- verificar/instalar o runtime local quando permitido;
- selecionar um perfil de modelo compatível;
- baixar o modelo de sua fonte oficial/licenciada, quando necessário;
- configurar Providers;
- executar health checks;
- validar o ambiente;
- iniciar a NEXORA.

### Regra de distribuição
Não redistribuir binários ou pesos de modelos dentro do instalador sem verificar previamente licença e direitos de distribuição. Preferir instalação/download de fontes oficiais quando apropriado.

### Critério de conclusão
Um usuário com hardware compatível consegue chegar ao primeiro uso da NEXORA com configuração mínima.

---

## FASE 23 · NEXORA UI / EXPERIENCE LAYER
**Objetivo:** criar a interface visual definitiva da NEXORA.

### Direção visual obrigatória
A UI deverá ter uma **pegada extremamente tecnológica, futurista e inovadora, mas simples de usar**.

A complexidade deve estar escondida na arquitetura, não exposta ao usuário.

### Princípios
- visual tecnológico sem excesso de elementos;
- hierarquia visual clara;
- poucos controles principais;
- feedback de estado em tempo real;
- sensação de sistema inteligente vivo;
- animações discretas e funcionais;
- visual premium/futurista;
- acessibilidade e legibilidade acima de efeitos;
- desktop-first inicialmente, com arquitetura preparada para evolução;
- operações avançadas disponíveis sem poluir a interface principal.

### Conceito de experiência
O usuário deve perceber a NEXORA como uma inteligência operacional avançada, não como uma tela cheia de configurações.

### Critério de conclusão
A UI permite executar as capacidades principais da NEXORA de forma intuitiva, enquanto transmite visualmente a identidade tecnológica e inovadora do produto.

---

## FASE 24 · AUTONOMOUS PRODUCT ENGINE
**Objetivo:** aproximar a NEXORA do loop econômico real do North Star.

### Loop-alvo
`OBSERVAR → PESQUISAR → ENTENDER → OPORTUNIDADE → SCORE → PLANEJAR → CRIAR → TESTAR → VALIDAR → LANÇAR → DISTRIBUIR → MEDIR → MELHORAR → GERAR RECURSOS → REINVESTIR`

### Entregas futuras
- descoberta de oportunidades;
- avaliação de mercado;
- criação de protótipos/produtos;
- validação;
- lançamento governado;
- distribuição;
- métricas;
- aprendizado econômico;
- reinvestimento de recursos;
- expansão da capacidade computacional/operacional.

### Critério de conclusão
NEXORA consegue fechar de forma verificável ciclos completos de criação de valor e geração de recursos dentro das permissões, políticas e limites definidos.

---

## FASE 25 · CONTINUOUS EVOLUTION
**Objetivo:** permitir evolução contínua sem perder identidade, segurança, rastreabilidade ou controle.

### Princípios
- toda mudança importante é testada;
- experiências alimentam futuras decisões;
- decisões possuem proveniência;
- mudanças são auditáveis;
- regressões são detectadas;
- capacidades novas são avaliadas antes de promoção;
- nenhuma evolução pode quebrar o North Star ou a governança.

### Critério de conclusão
A NEXORA consegue melhorar sua própria capacidade de criar valor continuamente, mantendo continuidade e controle.

---

# Regras permanentes do roadmap

1. **Não criar outra NEXORA.**
2. **Não criar outro Runtime de execução.** O `AgentRuntime` permanece o proprietário do ciclo avançado.
3. **Não contornar Permission, Policy, Checkpoint, Idempotency, Observation, Verification ou Audit.**
4. **Não remover a Fase 16 — Long-Term Autonomy.**
5. **Não transformar NEXORA em wrapper de ferramenta/modelo externo.**
6. **Toda funcionalidade nova nasce com testes.**
7. **Testes escritos não equivalem a testes aprovados.** O incremento só é considerado validado após execução bem-sucedida e, quando aplicável, CI verde.
8. **Mudanças que atravessam componentes exigem testes de integração.**
9. **Não habilitar retry de efeitos externos sem idempotência, autorização, precondições, verificação e recuperação explícitas.**
10. **Não inventar tokens, custos, latência, evidências ou resultados.**
11. **GitHub é a fonte de verdade.**
12. **PROJECT_MEMORY deve acompanhar o estado real do código.**
13. **A UI deve ser simples para o usuário, mesmo quando a arquitetura interna for extremamente sofisticada.**
14. **O roadmap pode ser reorganizado por evidência técnica, mas nenhuma mudança deve reduzir o North Star.**

## Regra operacional
Cada avanço significativo seguirá:

`AUDITAR → DECIDIR → IMPLEMENTAR → TESTAR → ATUALIZAR PROJECT_MEMORY → COMMIT → PUSH → VERIFICAR CI → HANDOFF`

## Direção final
A NEXORA deverá evoluir de infraestrutura de agentes para uma inteligência operacional capaz de:

`ENTENDER → CRIAR → TESTAR → APRENDER → EVOLUIR → CRIAR VALOR → GERAR RECURSOS → AMPLIAR SUA PRÓPRIA CAPACIDADE`

com uma experiência de usuário **tecnológica, futurista, inovadora e extremamente simples de operar**.