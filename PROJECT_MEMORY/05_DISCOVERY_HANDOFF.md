# NEXORA — Discovery Handoff

> Ponto de continuidade da Fase de Capability Discovery. O próximo agente/engenheiro deve começar por este documento。

 Nenhum código de produção foi criado. Nada foi commitado.



## 1. Estado atual

- **Repositório:** `/workspace/project` — greenfield, git inicializado( branch `master` ), **zero commits**, **sem remoto**;
- **Conteúdo criado nesta fase( SOMENTE documentação ):`PROJECT_MEMORY/` com 6 arquivos:
  - `00_IDENTITY.md`
  - `01_NORTH_STAR.md`
  - `02_CAPABILITY_DISCOVERY.md`( pesquisa completa≈1.250 linhas,13 seções A–L,M+referências )
  - `03_CAPABILITY_MATRIX.md`( matriz consolidada,49+ capacidades )
  - `04_ARCHITECTURE_REQUIREMENTS.md`( requisitos arquiteturais transformados )
  - `05_DISCOVERY_HANDOFF.md`( este documento )
- **Nenhum arquivo de código,configuração,teste ou src/ foi criado**。
- **Nenhuma dependência instalada;nenhum commit realizado**。





## 2. O que foi descoberto( síntese )

### Capacidades fundamentais( REPLICAR — base obrigatória )

| Capacidade | Nota |
|---|---|
| Ciclo agente( Contexto→Thought→Ação→Observação→iteração ) | Núcleo do runtime,com limites de iteração/custo/verificação |
| Raciocínio estruturado e auditável( thought como evento ) | Requisito de observabilidade e memória |
| Abstração de provider( interface tipada,model-agnostic ) | **Princípio arquitetural central da NEXORA** |
| Estado event-sourced + checkpoints | Base de auditoria,retomada e rollback |
| Memória de curto prazo( sessão,com rotação ) | Substrato de raciocínio coerente |
| Tool registry versionado com anotação de risco/permissão | Porta única de extensão de ferramentas |
| Autorização por ação( default-deny,menor privilégio ) | Fundação da execução controlada |
| Sandbox e isolamento por execução | Contenção física de dano |
| Credential broker( tokens curtos,escopados,zero segredos no contexto/logs ) | Previne vazamento irreversível |
| Audit trail imutável e indexado | Governança e investigação |
| Gates de aprovação humana( ações sensíveis ) | Última linha de alinhamento ao criador |
| Taint de conteúdo externo( prompt injection ) | Defesa em profundidade( permissões+sandbox+approval ) |

### Capacidades a adaptar( ADAPTAR — maioria do sistema )

| Capacidade | Como adaptar para a NEXORA |
|---|---|
| Interpretação de objetivos | Objetivo estruturado( escopo,critérios de sucesso,autonomia,orçamento ) + rastreabilidade |
| Gerenciamento de contexto | Política própria de compressão/sumarização por provider,alinhada à memória |
| Tomada de decisão | Decisão do modelo separada da autorização da plataforma( control/execution plane ) |
| Terminal | Sandbox estrito,default-deny de rede,quotas,auditoria |
| Filesystem | Escopo por projeto,default-deny fora do workspace |
| Git | Gates por operação( commit automático possível;push/merge com aprovação ) |
| Memória de longo prazo | 3 tipos( semântica,episódica,procedural )+ versionamento,provenance,governança( escrita e poda ) |
| Planejamento | Plano como DAG validável,com scheduler e gates de verificação entre etapas |
| Providário/roteamento | Política declarativa por tarefa,eventos de decisão,fallback com classificação de erro |
| Orquestração multi-agente | Contrato de delegação tipado,verificação de entregável,comunicação por eventos |
| Pesquisa | Pipeline com citação obrigatória e verificação de fontes |
| Ciclo de autonomia( observação,monitoramento ) | Escopo,deduplicação,limiares,orçamento |

### Capacidades a superar( SUPERAR — diferenciação )

| Capacidade | Justificativa( por que superar ) |
|---|---|
| Recuperação de falhas | Classificação de falha+replanejamento local/global em vez de retry cego( baseado em literatura de DAG replanning ) |
| Verificação de código( B4 ) | Além de testes existentes:cobertura,regressão,contrato,verificação estrutural entre etapas( raro nas referências ) |
| Verificação de fontes( D2 ) | Etapa explícita e auditável com provenance e graus de confiança( ausente nas referências de produto ) |
| Memória de decisões/lições( E4 ) | Decision log + lessons learned estruturados,com validade e recuperação ativa( não apenas "aprende com erros" ) |
| Verificação e replanejamento( F4 ) | Gates entre etapas + replanejamento guiado( supera iteração linear das referências ) |
| Rastreamento de custo( H7 ) | Custo abrangente( LLM+ferramentas+infra ) por unidade de trabalho,com orçamentos e alertas |
| Experimentação( I2 ) | Plataforma integrada com promoção por estágios e rollback automático |
| Criação de ferramentas( I4 ) | Pipeline com gates de segurança/testes( não apenas extensão manual ) |
| Limites de autonomia( J3 ) | Níveis por objetivo+aprovação por categoria( supera controle por conversa da Arena ) |
| Aprendizado em-loop( J5 ) | Consolidação com validade,revisão e poda( evita envenenamento do conhecimento ) |
| Operação segura( K7 ) | Circuit breakers+alertas+kill switch por escopo( segurança operacional ativa ) |

### Capacidades a criar( CRIAR — próprias da NEXORA )

| Capacidade | Por que é exclusiva |
|---|---|
| Pesquisa contínua e atualização do conhecimento( D4 ) | Nenhuma referência principal oferece monitoramento contínuo com consolidação versionada |
| Autonomia por objetivos persistentes( J1 ) | Operação contínua dirigida por objetivos( North Star ),não por prompts |
| Identificação de oportunidades( L1 ) | Motor da North Star( "identificar oportunidades" ) — ausente em agentes de propósito geral |
| Análise de mercado e concorrência( L2 ) | Serviço estruturado alimentado por pesquisa contínua |
| Produto/preço/distribuição( L3 ) | Engines de captura de valor( legal e sustentável,com aprovação humana ) |
| Analytics de valor( L4 ) | Receita,custo,margem,ROI por produto/canal |
| Portfólio e reinvestimento( L5 ) | Alocação de recursos e reinvestimento autorizado( transformar valor em capacidade ) |
| Auto-expansão( M1–M4 ) | Auto-diagnóstico de lacunas + pesquisa + implementação com gates humanos( controlada ) |

**Balanço geral das classificações( contagem a partir da matriz ):** a maioria das capacidades fundamentais cai em **REPLICAR/ADAPTAR**( o "esqueleto" da plataforma é bem conhecido );o diferencial da NEXORA está em **SUPERAR**( recuperação,verificação,custo,experimentação,autonomia ) e sobretudo **CRIAR**( dimensão econômica e auto-expansão — únicas no roadmap )。



---

## 3. Capacidades críticas( obrigatórias no MVP )

As seguintes capacidades formam o **núcleo mínimo viável**( pós-Fase 0 ) e **devem existir desde a primeira entrega executável:**

1. **Abstração de provider + fallback + custo rastreado**( H1,H5,H7 — princípio arquitetural );
2. **Ciclo agente com interpretação de objetivo e plano simples**( A1,A3,F1 );
3. **Execução controlada**:autorização por ação+sandbox+segredos+auditoria( K1,K2,K3,K4 );
4. **Gates de aprovação humana**( K6,J3 );
5. **Memória de curto prazo + mínima longo prazo**( E1,E2 );
6. **Ferramentas iniciais**:filesystem escopado+terminal sandboxado+editação+git com gates( B2,B3,C2,B8 );
7. **Verificação mínima entre etapas + recuperação básica de falha**( A8,F4 — mesmo que simples );
8. **Configuração/segredos via ambiente**( nenhum hardcode — K3 );

**Fora do MVP( pós-Fase C ):** multi-agente,computer use pleno,pesquisa contínua,auto-expansão,economic engine( prioridades MÉDIA ).



---

## 4. Lacunas identificadas( entre visão e referências )

| # | Lacuna | Impacto | Fechada por |
|---|---|---|---|
| 1 | Nenhuma referência cobre a dimensão econômica( oportunidades,produto,preço,distribuição,reinvestimento ) | North Star exige;é o maior diferencial | Capacidades L( CRIAR ) |
| 2 | Nenhuma referência destaca pesquisa contínua/monitoramento de conhecimento | Aprender continuamente sobre o mundo exige | D4+J2( CRIAR/ADAPTAR ) |
| 3 | Verificação estrutural entre passos é rara em produtos | Sem ela,erros se propagam | A8/F4/B4( SUPERAR ) |
| 4 | Recuperação de falhas é tratada superficialmente( "fix mistakes" ) | Tarefas longas morrem em falhas triviais | A8( SUPERAR ) |
| 5 | Rastreamento de custo é raro e limitado a LLM | Autonomia sem custo é insustentável | H7( SUPERAR ) |
| 6 | Auto-expansão/auto-modificação não é tratada com gates em produtos | Risco crítico de governança | M3( ADAPTAR com gates humanos obrigatórios ) |
| 7 | Segredos são frequentemente expostos no contexto/logs | Vazamento irreversível | K3( REPLICAR — broker+sanitização ) |
| 8 | Controle fino de permissões/autonomia( por ação,categoria ) é subdesenvolvido | Execução controlada é requisito explícito da visão | K1/J3( SUPERAR/REPLICAR ) |

---

## 5. Decisões provisórias( tomadas nesta fase,sujeitas a aprovação )

1. **Linguagem/ecossistema: NÃO decidida ainda** — Python é candidato natural( ecossistema de IA,SDK de agentes );Node/TS também viável( ecosistema de ferramentas ).**Decisão adiada para aprovação**( ver Perguntas arquiteturais ).
2. **MVP vertical sugerido**:linguagem natural → objetivo estruturado → plano simples → execução controlada de 3–5 ferramentas via provider( Groq inicial) com custo,auditoria e aprovação— NÃO implementado;a proposta segue abaixo( Próxima etapa ).
3. **Primeiro provider sugerido:** Groq( planejado pelo usuário );com um `FakeProvider` determinístico para testes e um fallback(` fake ou segundo provider ) desde cedo( H5 ）;
4. **Arquitetura de estado sugerida:** event-sourced( baseado em OpenHands e requisitos de auditoria/retomada );
5到. **Memória inicial sugerida:** curto prazo em sessão + longo prazo simples( com schema e versionamento desde o início,mesmo que backend simples — ex:JSON/estruturado );vetorial depois;
6.**. **Segurança desde o dia 1**:autorização por ação,default-deny,sandbox( mesmo que simples ),credential broker( mínimo:env+injeção seletiva ),auditoria de eventos,gates de aprovação;

7.**. **Extensibilidade por registro desde o início**:tool registry,provider registry;( agent registry depois);
8.**. **Níveis de autonomia desde cedo**:padrão conservador( supervisor/por-ação ) evoluindo com confiança;

---

## 6. Pontos ainda indefinidos( precisam decisão humana )

| # | Ponto | Opções | Impacto |
|---|---|---|---|
| P1 | Linguagem/ecossistema | Python(uv/pip,poetry) vs Node/TypeScript(tsx/pnpm) vs híbrido | Fundamental:todo o design de módulos |
| P2 | Nomeação de módulos/namespace | `src/nexora/`(Python) vs `src/`(TS) etc. | Organização do repositório |
| P3 | Interface de entrada do MVP | CLI primeiro vs API REST primeiro vs SDK | Primeiro caso de uso e teste |
| P4 | Backend inicial de memória | Arquivos JSON/estruturado vs SQLite vs vetorial desde cedo | Esforço vs capacidade |
| P5 | Backend inicial do event store | Arquivos JSON sequenciais vs SQLite vs append-only próprio | Simplicidade vs robustez |
| P6 | Groq como provider 1( e modelo específico a usar ) | Qual modelo Groq;como expor tool-calling | Capacidade real do MVP |
| P7 | Sandbox do MVP | Docker vs bubblewrap vs subprocess isolado vs remoto( gVisor etc. ) | Esforço vs isolamento |
| P8 | Ângulo do MVP( qual caso de uso primeiro ) | Codificação( multi-arquivo ) vs pesquisa+relatório vs automação( workflow ) | Direção da primeira demonstração |
| P9 | Onde vive a política( permissões,roteamento,autonomia ) | Arquivo de config declarável( YAML/TOML/Python ) vs banco vs UI | Governança e testabilidade |
| P10 | Multi-agente no MVP ou nah | Agente único orquestrado internamente vs sub-agentes | Escopo do MVP |
| P11 | Observabilidade do MVP | Logs estruturados locais vs endpoint/UI vs OpenTelemetry | Esforço vs diagnóstico |

---

## 7. Propostas de alteração do roadmap( AGUARDANDO APROVAÇÃO — não aplicar ainda )

> Nenhuma alteração foi aplicada ao ROADMAP v1. Abaixo,propostas emergentes da Discovery,para revisão humana:

1. **PROPOSTA A( Nomenclatura/alinhamento ):** os "Engines" do roadmap( Agent Runtime,Coding Agent,Research Engine,Experience Engine,Experimentation Engine,Evolution Engine,Economic Engine,Product Engine,etc. ) mapeiam bem às capacidades descobertas;**sugere-se explicitar que "Coding/Research/Experience" são **papéis de agente/ferramenta** acoplados a um núcleo único( não subsistemas independentes )** — reduz risco de duplicação arquitetural；
2. **PROPOSTA B( Segurança como transversal ):** o roadmap lista Security/Governance como um estágio;**sugere-se tratá-lo como requisito transversal desde a Fase  técnica**( não uma fase tardia ) — baseado em guias de segurança de agentes:contenção deve vir com a primeira execução;
3. **PROPOSTA C( Verificação/Evolution como habilitadores antecipados ):** experimentação e benchmarking( Evolution Engine ) são necessários cedo( mesmo que simples ) para governar escolhas de providers e prompts— não apenas após "Evolution Engine";
4.. **PROPOSTA D( Economic Engine — aprovação humana ):** decisões de pricing/distribuição/contratos devem sempre exigir participação humana( legal,contratual,alinhamento ) — sugerido como invariante,mesmo quando a plataforma for autônoma;
5.**.** **PROPOSTA E( Auto-expansão com gates ):** auto-modificação( Self-Modeling/Metacognition,Agent Creation,Tool Creation ) deve ser sempre gateada por revisão humana para ativação( exceto mudanças trivialmente delegadas ) — para evitar auto-modificação descontrolada;

---

## 8. Perguntas arquiteturais que precisam de aprovação

1. **Linguagem/ecossistema e estrutura de diretórios**( ver P1/P2 );
2. **Escopo do MVP**( qual caso de uso;quais ferramentas iniciais;quais capacidades entram ) ;
3. **Encaixe do Groq**:qual modelo de tool-calling/streaming do Groq será o primeiro provider( e se usaremos também um provider secundário/fake desde cedo );
4.. **Backends iniciais**( memória=JSON/SQLite;event store=JSON sequencial/SQLite;política=arquivo declarativo );
5. **Nível de isolamento do sandbox inicial**( subprocesso isolado vs container );
6.. **Autonomia inicial por padrão**( supervisor por-ação vs delegação limitada );
7.**.** **Aceitação das propostas A–E de alteração do roadmap**( seção 7 ;

---

## 9. Recomendação da próxima etapa( proposta — aguardando aprovação )

**Não avançar para implementação ainda.** A próxima etapa recomendada é uma **Fase de Decisão e Design( "Fase 0.5" )**, curta e sem código:

1. Fechar com o usuário/arquiteto as **decisões P1–P11**( seção 6 );
2.. Aprovar( ou ajustar ) as **propostas A–E** de alteração do roadmap( seção 7 );
3。. Produzir( em documentação,ainda sem código ) :
   - **ADR**( Architecture Decision Records ) das decisões P1–P11;
   - **Contratos iniciais por schema**( JSON Schema ) de:Objetivo,Plano/DAG,Chamada de Provider,Evento,Tool,Delegação,Memória,Aprovação( ver seção Interfaces do 04 );
   - **Estrutura de repositório proposta**( diretórios,nomes,arquivos-base,AGENTS.md,config ) — como **proposta**,não implementação;
4**. **Só então** avançar para a **Fase 1 de implementação**( fundação/esqueleto ),com aprovação explícita por etapa。



---

## 10. Ponto exato onde o próximo agente deve continuar

- **Comece por este documento**( todo );
- Depois releia `02_CAPABILITY_DISCOVERY.md`->`03_CAPABILITY_MATRIX.md`->`04_ARCHITECTURE_REQUIREMENTS.md`( nessa ordem );
- Verifique o repositório com `git status`( esperado:somente `PROJECT_MEMORY/` não commitado );
- **NÃO escreva código de produção** até que ( a )( as decisões P1–P11 foram aprovadas/respondidas e ( b )( a Fase de Implementação foi explicitamente autorizada pelo usuário/arquiteto;
- Se aprovado para continuar, comece pela "Fase 0.5 — Decisão e Design"( seção 9 ),produzindo ADRs e schemas como documentação,sem código;

---

## 11. Confirmação de conformidade

- ✅ **Nenhum código de produção foi criado**( sem src/,tests/,agents/,providers/,runtime/,tools/,executors/,interfaces,configuração operacional );
- ✅ **Nenhuma dependência instalada**;
- ✅ **Nenhum commit realizado**( `git status` mostra apenas `PROJECT_MEMORY/` pendente );
- ✅ **Nenhuma alteração ao ROADMAP v1 original**( propostas registradas apenas na seção 7 );
- ✅ **Nenhum arquivo apagado,movido ou renomeado do projeto**( apenas criação de documentação em `PROJECT_MEMORY/` );
- ✅ **Nenhuma inferência apresentada como fato**( OBSERVADO/INFERIDO/PROPOSTA distinguidos ao longo de todo o 02/03 )。

---

*Fim do Discovery Handoff.*