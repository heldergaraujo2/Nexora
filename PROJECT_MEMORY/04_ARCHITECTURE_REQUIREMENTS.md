# NEXORA — Architecture Requirements

> Transformação das capacidades descobertas( ver 02_CAPABILITY_DISCOVERY.md e 03_CAPABILITY_MATRIX.md ) em requisitos arquiteturais.**NÃO** desenha implementação detalhada ainda. Define apenas **o que** a arquitetura futura deverá ser capaz de suportar.



## Princípios norteadores ( requisitos transversais )

1. **Modelo-agnóstico obrigatório** — a inteligência não fica presa a um único modelo/fornecedor: toda capacidade que consome IA deve passar pela camada de Providers( nunca chamar um provider diretamente de um módulo de negócio )。
2. **Separação control plane / execution plane** — decisões( o que o modelo escolhe ) e autorização( o que a plataforma permite ) são camadas distintas;nada é executado sem passar por autorização,mesmo se o modelo "decidir"。
3. **Default-deny** — por padrão,nada é permitido( leitura,escrita,rede,execução,delegação );tudo o que for permitido é explicitamente concedido por política。
4. **Tudo é evento** — ações,decisões,autorizações,roteamento,custos,erros e observações são eventos de primeira classe( auditáveis,replays,alimentam memória e governança )。
5. **Memória como cidadã de primeira classe** — memória não é um extra;é parte do núcleo( contratos de schema por tipo,versionamento,provenance ) desde o início。
6. **Verificação em todo lugar** — todo passo de valor( edição,execução,pesquisa,delegação,capacidade nova ) tem etapa de verificação associada;
7. **Extensibilidade por registro** — providers,ferramentas,agentes,prompts,estratégias e capacidades são artefatos registrados e versionados( adicionar novo não reescreve o núcleo );**8. **Custo é governança** — custo é rastreado por unidade de trabalho( tarefa,sessão,objetivo,agente ) e tem orçamentos/alertas;autonomia sem custo rastreado não existe;**9. **Autonomia com freios** — níveis de autonomia por objetivo,com gates de aprovação humana para ações sensíveis e kill switches por escopo;**10. **Progressão por evidência** — mudanças( prompts,ferramentas,estratégias,capacidades ) promovidas por estágios( candidate→validated→production ),com testes e rollback;**11. **Alinhamento à North Star** — toda capacidade deve poder rastrear-se à North Star( criar valor continuamente );decisões de expansão( domínios,investimentos ) exigem alinhamento com o criador e aprovação( quando estrutural )。

**12. **Conteúdo externo é não confiável** — tudo que vem de fora( web,arquivos,ferramentas de terceiros ) é tainted( marcado por proveniência ),com defesa em profundidade( permissões+sandbox+approval )。



---

## Módulos necessários

### Core Runtime

| Requisito | Origem(capacidades) | Notas |
|---|---|---|---|
| Ciclo agente com estado de sessão e limites de iteração/custo/tempo | A3,A7,J6 | Loop controlado,com parada elegante |
| Estado event-sourced,reconstruível(replay),com checkpoints por etapa | A6,K5,J6 | Fonte de verdade = event store |
| Raciocínio/thought como evento rastreável | A2 | Auditável e alimenta memória episódica |
| Gerenciamento de contexto( compressão/sumarização configurável por provider ) | A4,E1 | Desacoplado do loop |
| Classificação de falhas + retry/replan/abort( circuit breakers ) | A8,F4 | Recuperação guiada, não cega |
| Execução em lote(long-running) com retomada idempotente | J6 | Checkpoint por etapa |

### Objective & Planning

| Requisito | Origem | Notas |
|---|---|---|---|
| `Objective Interpreter`:linguagem natural → objetivo estruturado( intenção,escopo,restrições,critérios de sucesso,autonomia nível,orçamento ) | A1,J3 | Primeiro artefato do pipeline;rastreável |
| `Plano` como artefato versionável(DAG de subtarefas com dependências) | F1,F2 | Validação de grafo( acíclico,dependências realizáveis,paralelismo seguro ) |
| Scheduler com filas por dependência,concorrência limitada,contabilidade de orçamento | F3,J4 | Por tarefa/sessão/objetivo |
| Motor de replanejamento local/global guiado por classificação de falha | F4,A8 | Verificação entre etapas + aprovação antes de ações destrutivas |
| Modo autonomia( objetivos persistentes,ciclo planejar→executar→observar→replanejar ) | J1,D4 | Com política de parada/retomada e monitoramento |

### Providers & Routing

| Requisito | Origem | Notas |
|---|---|---|---|
| Interface `Provider` tipada( generate/stream/tools/capabilities/errors ) + implementações por provider + registry | H1 | Adicionar provider não toca o núcleo |
| Model registry com metadados( capacidades,custo,latência,contexto,qualidade medida ) | H2,H6 | Alimenta roteamento e cost tracking |
| Política de roteamento declarativa e plugável( por tarefa,tipo de etapa,orçamento,privacidade ) | H2,H3,H6 | Eventos de decisão de roteamento |
| Fallback com classificação de erro,cooldown e circuit breakers por provider/modelo | H5 | Visibilidade do fallback |
| Suporte a modelos locais como providers de primeira classe | H4 | Mesmo contrato,metadados próprios |
| Ledger de custos( LLM+ferramentas+infra ) por unidade de trabalho + orçamentos/alertas | H7,J4 | Custo como dado de governança |

### Tools & Execução

| Requisito | Origem | Notas |
|---|---|---|---|
| Tool registry versionado( schema tipado,anotação de risco/permissão por ferramenta,documentação ) | B*,C*,I4,K1 | Descoberta,autorização,auditoria |
| Filesystem com escopo obrigatório por projeto( default-deny fora do workspace ) | C2,B1,B2 | Allow/deny por path+auditoria de acesso |
| Terminal/sandbox com isolamento( rede,arquivos,processos ),quotas e lifecycle | C3,B3,K2 | Kill/destruir ao fim,tudo auditado |
| Browser com modo somente-leitura por padrão,allowlist de domínios,gates para ações destrutivas | C1 | Sanitização de conteúdo antes de entrar no contexto |
| Git integrado com gates por operação( commit,automação possível;push/merge,aprovação ) | B8,K6 | Identidade de autoria do agente |
| Edição com diff+checkpoint+validação pós-edição( lint,sintaxe,testes ) | B2,B4,B6 | Padrão editar→verificar→commit |

### Memory & Knowledge

| Requisito | Origem | Notas |
|---|---|---|---|
| Curto prazo:estado de sessão com rotação e sumarização | E1,A4 | Rápido,limitado,com política de rotação |
| Longo prazo:semântica+episódica+procedural,com versionamento,provenance e governança( escrita e poda ) | E2 | Recuperação por similaridade+metadados+política de relevância |
| Memória de projeto por repositório,com consolidação periódica | E3 | AGENTS.md-like,versionada,com processo de revisão |
| Decision log + lessons learned( com validade carimbada,fonte,revisão ) | E4,J5 | Recuperação ativa em decisões similares |

### Research

| Requisito | Origem | Notas |
|---|---|---|---|
| Pipeline de pesquisa( search→fetch→extract→rank→verify→synthesize ) | D1-D3 | Citação estruturada obrigatória |
| Verificação de fontes( graus de confiança,provenance por fato ) | D2 | Antes de persistir conhecimento |
| Monitoramento contínuo de fontes autorizadas com atualização versionada do conhecimento | D4,J2 | Deduplicação,limiares de relevância,orçamento |

### Multi-Agent

| Requisito | Origem | Notas |
|---|---|---|---|
| Agent registry versionado( especialidade,capacidade,permissões,custo,estado ) | G2,K1 | Descoberta e delegação declarativas |
| Orchestrator com atribuição de tarefas,contrato de delegação tipado e verificação do entregável | G1,G3,G6 | Antes de aceitar resultado |
| Comunicação por eventos tipados( protocolo interno );adoção seletiva de MCP/A2A | G4 | Sem acoplar núcleo a padrão específico |
| Revisão cruzada por criticidade + arbitragem configurável( regra,modelo,humano ) | G5 | Escalonamento humano em alto impacto |

### Security / Governance

| Requisito | Origem | Notas |
|---|---|---|---|
| Autorização por ação( política declarativa,default-deny,menor privilégio,revisão periódica ) | K1 | Policy decision point separado da execução |
| Sandbox e isolamento por execução( rede,arquivos,processos,quotas,lifecycle ) | K2,C3,B3 | Defesa em profundidade |
| Credential broker( tokens curtos,escopados,injeção seletiva,zero segredos no contexto/logs ) | K3 | Sanitização em toda captura de observação/log |
| Audit trail imutável e indexado( quem,o quê,quando,por quê,resultado ) | K4 | Retenção por política;consultável |
| Checkpoints/rollback por componente com integridade de dados | K5,J6 | Testar restauração periodicamente |
| Gates de aprovação humana para ações sensíveis( com contexto,risco,alternativas ) | K6,J3 | Timeouts,registro de decisões,negação/abortamento |
| Circuit breakers,alertas de anomalia,kill switch por escopo( agente,tarefa,global ) | K7,H5 | Shutdown gracioso com checkpoint+retomada |
| Taint de conteúdo externo( proveniência ) + defesa em profundidade | K8,D2 | Monitoramento de padrões de injeção |

### Evolution / Self-expansion

| Requisito | Origem | Notas |
|---|---|---|---|
| Runner de avaliação com métricas unificadas( conclusão,qualidade,custo,passos ) e histórico | I1 | Para comparar regressões |
| Plataforma de experimentação( isolada,com promoção por estágios e rollback automático ) | I2 | Candidate→validated→production |
| Registries versionados de prompts,estratégias,ferramentas e agentes | I3,I4,G2,M4 | Tudo tratado como artefato versionável |
| Pipeline de auto-expansão( detectar lacuna→pesquisar→projetar→implementar em sandbox→testar→promover com gates humanos ) | M1-M4 | Ativação sempre com revisão humana( exceto mudanças triviais delegadas ) |
| Releases versionados + canary + rollback por componente | I5,K5 | Gates humanos para mudanças estruturais |

### Economic / Opportunity Intelligence

| Requisito | Origem | Notas |
|---|---|---|---|
| Motor de oportunidades com scorecard( alinhamento,viabilidade,ROI,risco,urência ) e portfólio em memória | L1,L5 | Gates de aprovação para perseguir novas oportunidades |
| Templates de análise de mercado( concorrência,preço,posicionamento ) com citação e revisão periódica | L2,D2 | Reanálise por monitoramento |
| Engines de produto/preço/distribuição com dados de mercado+custo e aprovação humana em decisões legais/contratuais | L3,K6 | Registro de decisões comerciais |
| Analytics de valor( receita,custo,margem,ROI ) reutilizando experimentação e cost tracking | L4,I2,H7 | Relatórios integrados à governança |
| Política de reinvestimento( alocação por evidência,aprovação para grandes alocações ) | L5,J4,K6 | Alinhamento à North Star obrigatório |

---

## Interfaces críticas( a definir em design detalhado,futuro )

| Interface | Entre | Propósito |
|---|---|---|---|
| `Objetivo` ( schema ) | Usuário/Orquestrador → Objective Interpreter | Entrada padronizada do que fazer,com escopo e critérios |
| `Plano/DAG` | Planning → Scheduler → Execução | Contrato entre etapas( o que é entregue a cada nó ) |
| `Chamada de Provider` | Runtime → Camada Providers | Contrato model-agnóstico( chat,stream,tools,erros,custo ) |
| `Evento`  (schema unificado) | Todos os módulos → Event Store | Ação,decisão,autorização,custo,observação,erro |
| `Tool` 	 (schema) | Tool Registry → Runtime | Nome,descrição,schema de entrada,risco,permissão,ação |
| `Delegação` (task packet) | Orchestrator → Agente | Objetivo,contexto,critérios,orçamento,limites |
| `Memória` (tipos/recuperação) | Runtime/Memória → Contexto | Curto/longo prazo,recuperação com provenance |
| `Aprovação` (pedido/contexto) | Runtime → Interface Humana | Ação sensível:o quê,risco,alternativas,decisão |
| `Capacidade` (ciclo de vida) | Self-expansion → Registries | Proposed→candidate→validated→production→retired |

---

## Boundaries( limites entre módulos )

- **Providers conhecem apenas o contrato do Provider** — sem lógica de agente,negócio ou política;
- **Runtime não conhece providers específicos** — só a interface;
- **Política de autorização vive fora do alcance do modelo( control plane )** — o modelo não decide suas próprias permissões;
- **Sandbox isola execução** — ferramentas nunca tocam o host diretamente( por padrão );
- **Memória é serviço separado( com seus próprios schemas e governança )** — não embutida em módulos de negócio;
- **Registrys são a única porta de extensão** — providers,ferramentas,agentes,capacidades entram por registro,não por edição do núcleo;

- **Contenção de conteúdo externo no ingresso( taint )** — web/arquivos/ferramentas de terceiros são tratados como não confiáveis antes de qualquer uso;



---

## Sistemas críticos( com requisitos de teste e recuperação )

| Sistema | Por que crítico | Testes/Recuperação exigidos |
|---|---|---|---|
| Autorização + Sandbox + Segredos | Vetores primários de dano | Testes de negação( garantir que o proibido falha);testes de isolamento;testes de vazamento de segredo( logs recebem tokens? );drills de rollback |
| Gate de aprovação humana | Última linha de alinhamento ao criador | Testes de fluxo( aprovar,negar,timeout,abortar );drills com ações irreversíveis simuladas |
| Ledger de custos + circuit breakers | Governança de autonomia | Testes de estouro de orçamento( interrupção automática );testes de failover de provider( fallback age e registra ) |
| Estado/event store + checkpoints | Retomada e auditoria de tudo | Testes de replay/reconstrução de estado;drills de recuperação de crash( retomar sem perder progresso ) |
| Ciclo de verificação entre etapas | Impede propagação de erro | Testes de gate( etapa sem verificação não avança );testes de replanejamento local/global |
| Auto-expansão( gates ) | Auto-modificação descontrolada é o maior risco de governança | Testes de permissão de ativação( nada ativa sem review);drills de rollback de capacidade |
| Monitoring/autonomia( long-running ) | Operação contínua sem freio | Testes de limite de orçamento/escopo;drills de kill switch com retomada |

---

## Componentes que devem ser desacoplados obrigatoriamente

- **Camada de Providers** do núcleo( princípio arquitetural central );‑
- **Política de autorização/permissões** da execução( control plane vs execution plane );
- **Memória** dos módulos de negócio( serviço separado com contrato );
- **Observabilidade/event store** dos módulos que produzem eventos( pub/sub ou escrita direta em camada própria );
- **Registrys**( tools,providers,agentes,capacidades ) da lógica que os consome( extensão sem reescrita );
- **Repositório de prompts/estratégias** do runtime( artefatos versionados,tratados como código )。

 **Componentes que exigem sandbox obrigatório**

- Execução de código/comandos( terminal,build,testes );
- Browser com ações( navegação e interação;modo somente-leitura por padrão );
- Instalação de dependências( bundles,packages );
- Experimentos/auto-expansão( código candidato antes de promoção );
- Qualquer processamento de conteúdo externo não confiável( sanitização+isolamento )。

 **Componentes que exigem autorização obrigatória。**

- Toda chamada de ferramenta( leitura,escrita,execução,rede,delegação );
- Toda ação sensível ou irreversível( aprovação humana por política );
- Todo acesso a memória sensível( escopo de leitura por tarefa );
- Toda delegação para agente/subagente( permissões do delegado );
- Toda instalação/ativação de capacidade nova( gates de revisão );

---

## Resumo executivo

A arquitetura da NEXORA deve girar em torno de cinco colunas:

1. **Núcleo model-agnóstico**( loop de agente com estado,verificação,falhas e contexto );
2. **Camada de Providers e roteamento**( interface tipada,registry,fallback,roteamento por política,custo rastreado );
3. **Plataforma de execução segura**( tools registradas,autorização por ação,sandbox,segredos,auditoria,checkpoints,aprovação );
4. **Memória e conhecimento**( curto/longo prazo,projeto,decisões e lições,com governança e provenance );
5. **Camadas evolutivas**( avaliação,experimentação,auto-expansão com gates,economic/opportunity intelligence com alinhamento à North Star )。

Tudo registrado como eventos;tudo extensível por registro;tudo governado por política declarativa e custo rastreado【】