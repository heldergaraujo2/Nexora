# NEXORA — Capability Matrix

> Matriz consolidada da Capability Discovery( ver 02_CAPABILITY_DISCOVERY.md para detalhes, evidências e fontes ).Classificações:REPLICAR / ADAPTAR / SUPERAR / CRIAR.Prioridade:CRÍTICA > ALTA > MÉDIA-ALTA > MÉDIA.



## Legenda de evidência

- **OBSERVADO** = documentado/demonstrável em fonte pública( ver Referências no 02 );
- **INFERIDO** = conclusão razoável de comportamento observado;
- **PROPOSTA** = decisão arquitetural da NEXORA( não fato ).



## Matriz consolidada

| Capacidade | Referência | Evidência | Classificação NEXORA | Prioridade | Dependências principais | Implicação arquitetural |
|---|---|---|---|---|---|---|
| A1 Interpretação de objetivos | Arena.ai, OpenHands | OBSERVADO | ADAPTAR | CRÍTICA | schema de objetivo, Providers | Objective Interpreter tipado com escopo+critérios+rastreabilidade |
| A2 Raciocínio | Todos (Claude, Devin, Arena, OpenHands) | OBSERVADO | REPLICAR | CRÍTICA | Providers com reasoning, schema de thought | Thought como evento de primeira classe, auditável |
| A3 Ciclo agente | Anthropic Harness, OpenHands | OBSERVADO | REPLICAR | CRÍTICA | runtime, tools, observabilidade | Agent Runtime com limites de iteração/custo/verificação |
| A4 Gerenciamento de contexto | OpenHands (compression), Claude | OBSERVADO + INFERIDO | ADAPTAR | ALTA | memória curto prazo, política de sumarização | Context manager desacoplado, configurável por provider |
| A5 Tomada de decisão | Tool calling (todos), LLM routers | OBSERVADO | ADAPTAR | CRÍTICA | router, permissões, estado do plano | Decisão do modelo separada da autorização (control/execution plane) |
| A6 Estados | OpenHands (event-sourced), Claude (session), Devin (workspace) | OBSERVADO | ADAPTAR | ALTA | event store, schemas | Event sourcing + checkpoints + visão por objetivo |
| A7 Execução iterativa | Arena.ai, Devin | OBSERVADO | REPLICAR | CRÍTICA | runtime, orçamentos | Iteração controlada com verificação entre etapas |
| A8 Recuperação de falhas | Devin, DAG replanning literature | OBSERVADO + INFERIDO | SUPERAR | ALTA | replan, verificação, observabilidade | Falha classificada + replanejamento local/global + circuit breakers |
| B1 Leitura de projetos | OpenHands, Claude, Devin | OBSERVADO | ADAPTAR | ALTA | filesystem escopado, memória de projeto | Indexação/exploração de repositório com escopo |
| B2 Criação/edição de arquivos | Anthropic (str_replace), OpenHands | OBSERVADO | REPLICAR | CRÍTICA | editor, diff, verificação, permissões | Edição com diff+checkpoint+validação pós-edição |
| B3 Terminal e execução | Devin, OpenHands, Arena.ai (bash) | OBSERVADO | ADAPTAR | CRÍTICA | sandbox, permissões, quotas | Terminal sandboxado default-deny com auditoria |
| B4 Testes e verificação | Devin, OpenHands | OBSERVADO | SUPERAR | ALTA | terminal, framework de testes | Verificação além de testes: cobertura+regressão+contrato |
| B5 Debugging | Devin, erros estruturados (OpenHands/Claude) | OBSERVADO + INFERIDO | ADAPTAR | ALTA | terminal, observabilidade, memória episódica | Erros estruturados + lições por projeto |
| B6 Refatoração | Benchmarks (SWE-bench) | OBSERVADO + INFERIDO | ADAPTAR | ALTA | edição, testes, diff, checkpoints | Padrão editar→verificar→commit obrigatório |
| B7 Build e integração | Devin, OpenHands, npm/pip/uv | OBSERVADO | ADAPTAR | ALTA | terminal, política de dependências | Builds efêmeros/reproduzíveis + allowlist de pacotes |
| B8 Git e controle de versão | OpenHands, Claude, Devin (commit/PR) | OBSERVADO | ADAPTAR | ALTA | git, política por operação (gate commit/push/merge) | Integração git com gates e identidade de autoria |
| C1 Browser | Devin (headless), Anthropic (computer use) | OBSERVADO | ADAPTAR | ALTA | runtime browser, rede, extração | Browser somente-leitura por padrão + allowlist de domínios |
| C2 Filesystem | OpenHands, Anthropic, sandboxes | OBSERVADO | ADAPTAR | CRÍTICA | permissões, sandbox, memória projeto | Escopo por projeto + default-deny fora do workspace |
| C3 Processos e recursos | Guias de sandbox | OBSERVADO + INFERIDO | ADAPTAR | ALTA | sandbox, observabilidade | Lifecycle de processos + quotas de recursos |
| C4 Observação do ambiente | Anthropic, OpenHands, Devin | OBSERVADO | ADAPTAR | ALTA | tools, schema de observação, sanitização | Observação como evento estruturado + sanitização de segredos |
| D1 Busca e coleta | Arena.ai (web search), OpenHands | OBSERVADO | ADAPTAR | ALTA | web, rede, extração, memória | Pipeline search→fetch→extract→rank→verify→synthesize |
| D2 Fontes e verificação | Fact-checking(geral) | INFERIDO | SUPERAR | ALTA | pesquisa, memória, confiança de domínios | Verificação de fontes com provenance e graus de confiança |
| D3 Síntese e comparação | Arena.ai (research/planning categories) | OBSERVADO | ADAPTAR | ALTA | pesquisa, verificação, templates | Relatórios estruturados com citação e critérios explícitos |
| D4 Pesquisa contínua | (nenhuma nas refs principais) | OBSERVADO (lacuna) | CRIAR | MÉDIA | monitoramento, memória, scheduler | Monitoramento contínuo com atualização versionada do conhecimento |
| E1 Memória curto prazo | Literature de memória | OBSERVADO | REPLICAR | CRÍTICA | contexto, event store | Estado de sessão com rotação configurável |
| E2 Memória longo prazo | Survey arXiv, vector DBs | OBSERVADO | ADAPTAR | ALTA | armazenamento, recuperação, governança | 3 tipos (semantic/episodic/procedural) + versionamento + provenance |
| E3 Memória de projeto | AGENTS.md, CLAUDE.md | OBSERVADO | ADAPTAR | ALTA | memória, filesystem | Bloco por repositório com revisão/consolidação periódica |
| E4 Decisões/falhas/sucessos | Devin, literature de memória episódica | OBSERVADO | SUPERAR | ALTA | memória episódica, observabilidade | Decision log + lessons learned com validade e recuperação ativa |
| F1 Decomposição | Arena.ai, OpenHands, Devin | OBSERVADO | ADAPTAR | CRÍTICA | interpretador, schema de plano | Plano versionável com critérios por subtarefa |
| F2 DAG e dependências | Literature (DAG-Plan, scheduler-theoretic) | OBSERVADO | ADAPTAR | ALTA | schema DAG, validação, scheduler | DAG validável com estado por nó e caminho crítico |
| F3 Scheduler | Literature de orquestração/scheduling | OBSERVADO | ADAPTAR | ALTA | plano, runtime, orçamento | Motor de agendamento por dependências + concorrência limitada |
| F4 Verificação e replanejamento | Planning literature (replanning on failure), MDPI | OBSERVADO | SUPERAR | CRÍTICA | verificação, falhas, memória | Gates de verificação entre etapas + replanejamento local/global |
| G1 Orquestração | Literature (orchestration), Microsoft MARI | OBSERVADO | ADAPTAR | ALTA | registry, comunicação, permissões | Orchestrator com filas, atribuição e gates de delegação |
| G2 Registro de agentes | Microsoft MARI | OBSERVADO | REPLICAR | ALTA | schema de agente, permissões | Agent registry versionado com capacidade/permissão/custo |
| G3 Especialização e delegação | Literature, OpenHands (sub-agents) | OBSERVADO | ADAPTAR | ALTA | orchestrator, comunicação, verificação | Contrato de delegação tipado + verificação do entregável |
| G4 Comunicação | A2A, MCP (literature) | OBSERVADO | ADAPTAR | ALTA | event store, schemas | Mensagens tipadas + adoção seletiva de protocolos abertos |
| G5 Revisão cruzada e conflitos | Literature (conflict resolution), Devin Swarm | OBSERVADO | ADAPTAR | MÉDIA-ALTA | comunicação, verificação, escalonamento | Hooks de revisão por criticidade + arbitragem configurável |
| G6 Consolidação de resultados | Literature (aggregation), Devin Swarm (map-reduce) | OBSERVADO | ADAPTAR | ALTA | comunicação, verificação, política | Validação de consistência + critérios de aceitação |
| H1 Abstração de provider | OpenHands, roteamento de modelos | OBSERVADO | REPLICAR | CRÍTICA | schema de chamada, registry | Interface Provider tipada + negociação de capacidades |
| H2 Múltiplos modelos e troca | Model routing literature | OBSERVADO | ADAPTAR | CRÍTICA | abstraction, registry, política | Troca por política explícita + eventos de roteamento |
| H3 Combinação de modelos | Capability matrix (routing literature) | OBSERVADO + INFERIDO | ADAPTAR | ALTA | abstraction, plano, verificação | Papéis de modelo por etapa + contrato de passagem |
| H4 Modelos locais e online | Ollama/vLLM, LiteLLM, OpenRouter | OBSERVADO | ADAPTAR | MÉDIA | abstraction, registry, benchmark | Providers locais como primeira classe + benchmark interno |
| H5 Fallback e resiliência | LiteLLM (cooldown), OpenRouter | OBSERVADO | ADAPTAR | CRÍTICA | abstraction, observabilidade, política | Fallback com classificação de erro + cooldown/circuit breakers |
| H6 Seleção por tarefa | Zylos (capability matrix), Braintrust (routing por qualidade) | OBSERVADO | ADAPTAR | ALTA | registry, avaliação, política | Roteamento por política declarativa realimentada por dados |
| H7 Rastreamento de custo | OpenRouter, Braintrust | OBSERVADO | SUPERAR | CRÍTICA | abstraction, runtime, ledger | Ledger de custos por unidade de trabalho + orçamentos/alertas |
| I1 Avaliação e benchmarking | Arena.ai (leaderboard), OpenHands (SWE-bench) | OBSERVADO | ADAPTAR | MÉDIA-ALTA | runner, métricas, memória | Runner de avaliação com métricas unificadas e histórico |
| I2 Experimentação | A/B testing(geral) | OBSERVADO | SUPERAR | MÉDIA | benchmarking, observabilidade, política | Experimentos isolados com promoção (candidate→validated→production) e rollback |
| I3 Melhoria de prompts/estratégias | Prática de engenharia de prompt | OBSERVADO | ADAPTAR | MÉDIA | benchmarking, experimentação, memória | Prompts/estratégias versionados, promovidos por dados |
| I4 Criação de ferramentas | OpenHands, Claude Code (skills) | OBSERVADO | SUPERAR | MÉDIA | tool registry, sandbox, review | Pipeline de criação de tools com gates de segurança/testes |
| I5 Evolução controlada e rollback | CI/CD(prática de engenharia) | OBSERVADO | ADAPTAR | MÉDIA-ALTA | benchmarking, release, aprovação | Releases versionados + canary/rollback + gates humanos estruturais |
| J1 Objetivos e planejamento contínuo | Automações scheduladas (ecossistema) | OBSERVADO (parcial) + INFERIDO | CRIAR | ALTA | planejamento, memória, orçamento | Modo autônomo com ciclo planejar→executar→observar→replanejar + parada elegante |
| J2 Observação e monitoramento | GitHub repo monitor, Slack monitor | OBSERVADO | ADAPTAR | MÉDIA | pesquisa, memória, scheduler | Monitoramento com escopo, deduplicação e limiares |
| J3 Limites de autonomia | Guias de segurança (approval gates) | OBSERVADO | SUPERAR | CRÍTICA | permissões, notificação, registro | Níveis de autonomia por objetivo + gates de aprovação |
| J4 Alocação de recursos e priorização | Orquestração/scheduling literature | OBSERVADO + INFERIDO | ADAPTAR | MÉDIA-ALTA | cost tracking, scheduler, objetivos | Quotas por objetivo + priorização com pesos + revisão |
| J5 Aprendizagem em-loop | Devin, memória episódica | OBSERVADO | SUPERAR | MÉDIA-ALTA | memória, verificação, reflexão | Ciclo de reflexão periódico + lições com validade |
| J6 Loops de longo prazo | Devin (sessões persistentes), OpenHands cloud | OBSERVADO | ADAPTAR | MÉDIA-ALTA | estado, checkpoints, scheduler | Execução em lote com checkpoints + retomada idempotente |
| K1 Autorização e permissões | Guias NVIDIA, Huntress, TowardsAI | OBSERVADO | REPLICAR | CRÍTICA | política, tool registry, auditoria | Authorization per action + default-deny + políticas como código |
| K2 Sandbox e isolamento | Devin, NVIDIA, TowardsAI | OBSERVADO | REPLICAR | CRÍTICA | runtime, rede, processos | Execução isolada com allow/deny + quotas + lifecycle |
| K3 Segredos e dados sensíveis | NVIDIA (secret injection), TowardsAI (broker), AYAutomate (sanitização) | OBSERVADO | REPLICAR | CRÍTICA | cofre, broker, sanitização | Credential broker com tokens curtos + zero segredos no contexto/logs |
| K4 Audit trail | Huntress, event-sourcing | OBSERVADO | REPLICAR | CRÍTICA | event store, observabilidade, retenção | Trilha imutável indexada de ações/decisões/autorizações |
| K5 Checkpoints e rollback | Prática de engenharia (checkpoint/rollback) | OBSERVADO | ADAPTAR | ALTA | estado, versionamento, retenção | Checkpoints por etapa + undo por edição + rollback por componente |
| K6 Ações sensíveis e aprovação | NVIDIA, TowardsAI, AYAutomate | OBSERVADO | REPLICAR | CRÍTICA | autorização, taxonomia, interface | Gates de aprovação humana com contexto + timeouts + registro |
| K7 Operação segura | LiteLLM (cooldown), práticas de resiliência | OBSERVADO + INFERIDO | SUPERAR | MÉDIA-ALTA | observabilidade, custo, checkpoints | Circuit breakers + alertas + kill switch por escopo com shutdown gracioso |
| K8 Prompt injection | NVIDIA (network isolation), TowardsAI, AYAutomate | OBSERVADO | REPLICAR | CRÍTICA | permissões, sandbox, provenance | Taint de conteúdo externo + defesa em profundidade + monitoramento |
| L1 Identificação de oportunidades |(nenhuma nas refs——lacuna) | OBSERVADO (lacuna) | CRIAR | MÉDIA | pesquisa, memória, governança | Motor de oportunidades com scorecard + portfólio + gates de aprovação |
| L2 Análise de mercado | Business intelligence(campos) | OBSERVADO (domínio) + PROPOSTA | CRIAR | MÉDIA | pesquisa, síntese, monitoramento | Templates de análise com citação + revisão periódica por domínio |
| L3 Produto/preço/distribuição | Roadmap NEXORA; campos de negócio | OBSERVADO (domínio) + PROPOSTA | CRIAR | MÉDIA | mercado, custos, aprovação | Engines especializadas + aprovação humana em decisões legais/contratuais |
| L4 Analytics de valor | Growth analytics(campos) | OBSERVADO (domínio) + PROPOSTA | CRIAR | MÉDIA | cost tracking, experimentação, coleta | Métricas de negócio + pipeline de analytics integrado |
| L5 Portfólio e reinvestimento | Portfolio management(campos);Roadmap | OBSERVADO (domínio) + PROPOSTA | CRIAR | MÉDIA-ALTA | oportunidades, custos, analytics, governança | Portfólio estruturado + política de alocação + aprovação p/ grandes alocações |
| M1 Identificação de lacunas | Auto-evolução(emergente) | INFERIDO | CRIAR | MÉDIA | benchmarking, verificação, memória | Capacity-gap pipeline com tickets e fila de revisão humana |
| M2 Pesquisa/avaliação de soluções | Composição de D + I2 | PROPOSTA | ADAPTAR | MÉDIA | pesquisa, experimentação, governança | Scorecard build/buy/adapt + review de segurança |
| M3 Implementação com gates | Pipeline de desenvolvimento | OBSERVADO (prática) + PROPOSTA | ADAPTAR | MÉDIA-ALTA | dev tools, testes, governança | Auto-expansão em sandbox + gates humanos de ativação + rollback |
| M4 Validação e incorporação | Registries de skills/tools | OBSERVADO | ADAPTAR | MÉDIA | benchmarking, experimentação, registries | Ciclo de vida de capacidade + registro central + promoção por estágios |