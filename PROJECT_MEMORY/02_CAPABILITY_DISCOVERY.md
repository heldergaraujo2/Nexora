# NEXORA  Capability Discovery

> Fase prévia ao roadmap. Nenhum código de produção foi criado. Este documento registra a pesquisa de capacidades de agentes modernos, referências, evidências, limitações e propostas para a NEXORA.

## Convenções de evidência

- **OBSERVADO** = comportamento/capacidade efetivamente documentado ou demonstrável em fonte pública( ver seção Referências);
- **INFERIDO** = conclusão razoável baseada em comportamento observado, mas não diretamente comprovada;

- **PROPOSTA** = decisão arquitetural que estamos propondo para a NEXORA( não é fato, é design).

Nada neste documento deve ser lido como "fato" quando marcado como inferência ou proposta.

---

# A. Agent Core

## A1. Interpretação de objetivos em linguagem natural

- **Descrição:** converter um objetivo em linguagem natural em representação estruturada e processável( intenção, escopo, restrições, critérios de sucesso).
- **Por que existe:** é a porta de entrada da plataforma; sem interpretação robusta, o restante do pipeline( planejamento, execução, verificação) opera sobre base frágil.

- **Referências:** Arena.ai Agent Mode  aceita objetivos complexos e multi-etapas em um único prompt( OBSERVADO via blog oficial); OpenHands SDK  interpreta tarefas de engenharia de software( OBSERVADO via docs/arxiv).
- **Evidência observável:** Arena.ai descreve "put in one prompt to execute a multi-stage workflow"; OpenHands resolve tarefas SWE-bench a partir de descrições de issues( OBSERVADO).
- **Limitações conhecidas:** ambiguidade, metas conflitantes, critérios de sucesso não declarados; interpretação é stateless nas referências não persiste aprendizado sobre como o usuário define objetivos( INFERIDO).
- **Classificação NEXORA:** ADAPTAR  necessita representação própria de objetivo com critérios de sucesso e escopo verificáveis, além de memória de preferências do criador.

- **Dependências:** linguagem de dados de objetivo( schema); camada de Providers para interpretação; contexto/memória quando disponível.

- **Risco:** médio  interpretação pobre propaga erro para todo o pipeline.

- **Prioridade:** CRÍTICA.

- **Implicação arquitetural:** módulo `Objective Interpreter` com contrato de saída tipado( objetivo estruturado); validação de escopo e critérios de sucesso; rastreabilidade da interpretação( para auditoria e correção).

## A2. Raciocínio( reasoning)

- **Descrição:** capacidade do modelo de raciocinar sobre objetivo, contexto e alternativas antes de agir( cadeia de pensamento, raciocínio multi-etapas, ponderação de trade-offs).
- **Por que existe:** é a base da tomada de decisão;a qualidade do raciocínio determina a qualidade do plano e das ações.

- **Referências:** todos os agentes modernos dependem disso( Claude Code/Claude Agent SDK, Devin, Arena.ai); Devin cita "advances in long-term reasoning and planning"( OBSERVADO).
- **Evidência observável:** resultados de benchmarks( SWE-bench para Devin e OpenHands); modo agente da Arena para workflows multi-etapas( OBSERVADO).

- **Limitações:** raciocínio é propriedade emergente do modelo, não do harness; não pode ser "garantido" pelo framework( INFERIDO); depende fortemente do provider escolhido.

- **Classificação NEXORA:** REPLICAR  na forma de contrato de raciocínio:o harness deve expor raciocínio estruturado e auditável, sem acoplar a um modelo específico.

- **Dependências:** camada de Providers com suporte a reasoning/tool-calling; representação de thought/raciocínio rastreável.

- **Risco:** médio  sem visibilidade do raciocínio, auditoria e verificação de decisões ficam prejudicadas.

- **Prioridade:** CRÍTICA.

- **Implicação arquitetural:** registro de "thought/reasoning" como evento de primeira classe no ciclo do agente( observável, auditável, armazenável em memória episódica).

##A3. Ciclo agente( Agent Loop)

- **Descrição:** o loop fundamental do agente: Contexto → Raciocínio → Ação( tool call) → Observação → iteração até concluir ou verificar.

- **Por que existe:** é o mecanismo que transforma modelo em agente  sem loop, há apenas chat unidirecional.

- **Referências:** Anthropic "Harness"( Context → Thought → Action → Observation)( OBSERVADO via workshop oficial); OpenHands SDK "Action-Observation pattern"( OBSERVADO via docs); Arena.ai agent mode executa workflows multi-step em uma ida( OBSERVADO).
- **Evidência observável:** documentação oficial do Claude Agent SDK e do OpenHands Tool System descrevem explicitamente o padrão Action/Observation; Devin opera em ciclos de planejar-executar-testar( OBSERVADO).
- **Limitações:** loop simples pode sofrer de loops infinitos e deriva de contexto sem limites de iteração, verificação e escape( INFERIDO).
- **Classificação NEXORA:** REPLICAR  como núcleo do runtime, porém com controles adicionais( ver "execução controlada").
- **Dependências:** runtime de execução, registro de ferramentas, observabilidade, limites de iteração/escopo/custo.

- **Risco:** alto se sem controles  loop sem saída, custo explosivo, ações não verificadas.

- **Prioridade:** CRÍTICA.

- **Implicação arquitetural:** componente `Agent Runtime` com estado de sessão, contadores de iteração, orçamento de passos/custo/tempo, hooks de verificação e interrupção( ver Autonomy).

##A4. Gerenciamento de contexto( Context Management)

- **Descrição:** manter, organizar e comprimir o contexto relevante( histórico de sessão, observações, memória recuperada) dentro dos limites da janela do modelo.

- **Por que existe:** janelas de contexto são finitas; sem gerenciamento, o agente perde informação relevante ou estoura o limite.

- **Referências:** OpenHands SDK inclui"automatic context compression"( OBSERVADO via docs oficial e arxiv); Anthropic discute context engineering e memória( INFERIDO a partir do workshop oficial); Claude Code gerencia contexto extenso com sub-agentes e skills( INFERIDO).
- **Evidência observável:** docs do OpenHands SDK listam "Automatic context compression" como feature( OBSERVADO); sumarização e compressão são práticas comuns documentadas( INFERIDO).
- **Limitações:** compressão pode perder detalhes importantes; decisão de "o que esquecer" é crítica e propensa a erro sem políticas explícitas( INFERIDO).
- **Classificação NEXORA:** ADAPTAR  necessita estratégia própria de contexto( curto-prazo por sessão, sumarização, recuperação seletiva de memória), alinhada à arquitetura de memória da NEXORA.

- **Dependências:** memória de curto prazo, políticas de sumarização/compressão, camada de Providers( limites de contexto por modelo).
- **Risco:** médio  má compressão degrada qualidade; janela estourada quebra a tarefa.

- **Prioridade:** ALTA.

- **Implicação arquitetural:** módulo de gerenciamento de contexto desacoplado do loop; políticas configuráveis de compressão/sumariação; profiler de contexto por provider.

##A5. Tomada de decisão

- **Descrição:** mecanismo pelo qual o agente escolhe a próxima ação( qual ferramenta, qual parâmetro, quando parar, quando pedir ajuda), dado o estado atual e o plano.

- **Por que existe:** sem tomada de decisão explícita, o agente apenas segue roteiro fixo;a autonomia depende dessa capacidade.

- **Referências:** todos os agentes( OpenHands, Claude Agent SDK, Devin, Arena.ai) decidem ações via modelo com tool-calling( OBSERVADO via documentação de tool use); roteamento de modelo(" LLM Router ") para decidir qual modelo trata cada requisição( OBSERVADO em arquiteturas de roteamento documentadas).
- **Evidência observável:** padrão de tool calling( Anthropic, OpenAI, Groq) documentado; LLM routers decidem por tarefa/modelo( OBSERVADO).
- **Limitações:** decisões podem ser inconsistentes entre passos sem política global( orçamento, preferências)( INFERIDO).
- **Classificação NEXORA:** ADAPTAR  decisão deve ser tomada não só pelo modelo, mas por um "decidir" controlado: política de escopo, orçamento, permissões e roteamento por tarefa.

- **Dependências:** model router/camada de Providers; registro de ferramentas; políticas de autorização; estado do plano.

- **Risco:** médio  decisões fora de política geram ações não autorizadas ou custos altos.

- **Prioridade:** CRÍTICA.

- **Implicação arquitetural:** separar "decisão do modelo" de "autorização da plataforma"( control plane separado do execution plane  ver Security); decisões registradas como eventos para auditoria.

##A6. Estados( State Management)

- **Descrição:** representar e persistir o estado do agente( contexto, plano parcial, resultados de ferramentas, posição no plano, orçamento consumido) ao longo da execução de uma tarefa e entre tarefas.

- **Por que existe:** sem estado, o agente não consegue retomar após falha, nem coordenar múltiplas etapas, nem auditar o que foi feito.

- **Referências:** OpenHands SDK é "event-sourced"  estado reconstruível a partir de eventos( OBSERVADO via arxiv/docs); Claude Agent SDK gerencia session state( query vs sessões)( OBSERVADO via docs); Devin opera em sessões com workspace persistente e sandbox( OBSERVADO).
- **Evidência observável:** terminologia "event-sourced state management" no OpenHands;"session state" e sub-agents no Claude Agent SDK( OBSERVADO).
- **Limitações:** estado inconsistente ou não versionado impede rollback/reversão( INFERIDO).
- **Classificação NEXORA:** ADAPTAR  event-sourcing é boa base; adicionar checkpoints/reversão e visão de estado por objetivo/tarefa, conforme visão de segurança.

- **Dependências:** armazenamento de eventos/estado, modelos de dados de tarefa/objetivo, memória.

- **Risco:** médio  perda de estado interrompe tarefas longas; estado sem auditoria enfraquece governance.

- **Prioridade:** ALTA.

- **Implicação arquitetural:** armazenamento de eventos como fonte de verdade( event store), checkpoints de estado, reconstrução de estado( replay), visão de estado por sessão/objetivo.

##A7. Execução iterativa

- **Descrição:** executar múltiplos passos de forma iterativa, incorporando resultados intermediários e ajustando o comportamento a cada iteração.

- **Por que existe:** tarefas complexas não são resolvidas em um único passo;a iteração é o que permite corrigir rumo com base em observações reais.

- **Referências:** mesmo padrão do Agent Loop( todas as referências); Arena.ai executa"multi-step workflow in one go"( OBSERVADO).
- **Evidência observável:** exemplos de agentes construindo sites ou rodando pesquisas profundas em múltiplos passos( OBSERVADO via Arena.ai blog); Devin implementa, testa e itera( OBSERVADO).
- **Limitações:** iteração sem limites de orçamento ou critério de parada é risco de custo e loop( INFERIDO); verificação intermediária é rara nas referências( OBSERVADO  nenhuma descreve verificação estrutural entre passos nas fontes coletadas; ver Planning para exceções em robótica/DAG).
- **Classificação NEXORA:** REPLICAR  com adição de limites de iteração e verificação entre etapas( melhoria proposta como SUPERAR em "verificação estrutural entre passos").
- **Dependências:** agent runtime, tool registry, observabilidade, orçamentos( ver Autonomy).

- **Risco:** médio  sem limites, custo/fuga/loop.

- **Prioridade:** CRÍTICA.

- **Implicação arquitetural:** iteração como parte do ciclo controlado do runtime, com contadores, orçamentos e parada por verificação/escopo.

##A8. Recuperação de falhas( Error Recovery / Resilience)

- **Descrição:** detectar falhas( tool error, timeout, resultado inesperado, plano inviável) e recuperar( retry, replan, escalonar, abortar com relatório).

- **Por que existe:** em execução real, falhas são inevitáveis;a diferença entre agente útil e frágil é a capacidade de se recuperar.

- **Referências:** Devin "fix mistakes" e aprende com erros( OBSERVADO via blog oficial); OpenHands robustez em benchmarks com retries e análise de erros( INFERIDO a partir de docs de tools/workspace); LLM routers têm fallback de provedores( OBSERVADO).
- **Evidência observável:** Devin descreve explicitamente"learn over time,and fix mistakes"; tool systems expõem erros estruturados como observações( OBSERVADO  OpenHands/docs Anthropic).
- **Limitações:** recuperação cega( retry sem diagnóstico) desperdiça custo; sem classificação de falha( transitória vs permanente, local vs global),a recuperação pode ser pior que a parada( INFERIDO a partir de literatura de DAG replanning).
- **Classificação NEXORA:** SUPERAR  recuperação baseada em classificação de falha e replanejamento local/global, não apenas retry linear; integrada ao planejamento e verificação.

- **Dependências:** planejamento( replan), tool registry, estados/checkpoints, verificação, observabilidade de erros.

- **Risco:** alto  sem recuperação, tarefas longas morrem em falhas triviais; com recuperação cega, custo cresce sem progresso.

- **Prioridade:** ALTA.

- **Implicação arquitetural:** componente de tratamento de falhas com taxonomia de falhas, políticas de retry/timeout, hooks de replanejamento e circuit breakers por provider/ferramenta.

---

# B. Coding Agent

##B1. Leitura e compreensão de projetos

- **Descrição:** capacidade de explorar um repositório( estrutura, arquivos, histórico, build), entender código existente e localizar pontos relevantes para a tarefa.
- **Por que existe:** sem leitura eficaz, o agente não consegue editar com segurança nem respeitar convenções existentes.

- **Referências:** OpenHands SDK( workspace/file tools) e Claude Agent SDK( text editor tool) demonstram leitura e edição de arquivos( OBSERVADO); Devin opera end-to-end em repositórios( OBSERVADO).
- **Evidência observável:** documentação de "text editor tool" e "file tools" nas plataformas; Devin descreve "plan and execute complex engineering tasks"( OBSERVADO).
- **Limitações:** leitura ingênua( arquivo por arquivo) é cara; sem índice de projeto, o agente se perde em repos grandes  INFERIDO.

- **Classificação NEXORA:** ADAPTAR  deve manter índice/grafo do projeto e memória de decisões por repositório( project memory).

- **Dependências:** ferramentas de filesystem(escopo de leitura), memória de projeto, gerenciamento de contexto.

- **Risco:** baixo  leitura é segura em modo somente-leitura; risco de vazamento de dados sensíveis se escopo não for restrito( ver Security).

- **Prioridade:** ALTA.

- **Implicação arquitetural:** ferramentas de filesystem com escopo por projeto; camada de indexação/exploração de repositório; permissões de leitura explícitas.

##B2. Criação e edição de arquivos

- **Descrição:** criar, modificar e remover arquivos com precisão( edição por trecho/string, não reescrita total).
- **Por que existe:** é a operação básica de qualquer agent de codificação; edição imprecisa destrói trabalho.

- **Referências:** Anthropic "str_replace_based_edit_tool" e OpenHands file editor( OBSERVADO via docs); Claude Code edita código com precisão( INFERIDO; OBSERVADO parcialmente via documentação de ferramentas).

- **Evidência observável:** nomes e descrições de ferramentas de edição documentadas nas plataformas( OBSERVADO).
- **Limitações:** edições podem violar sintaxe ou semântica sem verificação pós-edição; sem diff/review, erros se acumulam  INFERIDO.

- **Classificação NEXORA:** REPLICAR  com adição de verificação sintática e diff-review entre edições( integrar com verificação estrutural  SUPERAR).

- **Dependências:** ferramentas de file/editor, checkpoints/diff, verificação( lint, testes), permissões de escrita.

- **Risco:** médio  escrita sem permissão pode corromper ou exfiltrar; sem sandbox, edição perigosa em produção( ver Security).

- **Prioridade:** CRÍTICA.

- **Implicação arquitetural:** ferramenta de edição com geração de diff, undo/checkpoint, validação pós-edição; escrita condicionada a políticas de permissão( allowlist de paths).

##B3. Terminal e execução de comandos

- **Descrição:** executar comandos em shell( build, teste, instalação, execução) dentro de ambiente controlado.

- **Por que existe:** agente de codificação precisa verificar comportamento real, não apenas raciocinar sobre código.

- **Referências:** Devin opera com shell em sandbox( OBSERVADO via blog/fast.io); OpenHands Bash tool e Anthropic bash tool( OBSERVADO via docs); Arena.ai expõe "sandbox/bash environment"( OBSERVADO).
- **Evidência observável:** ferramenta bash/shell documentada nas três plataformas( OBSERVADO); Devin roda em "sandboxed compute environment with its own shell"( OBSERVADO).
- **Limitações:** comandos arbitrários são risco de segurança; sem limites de recursos( tempo, memória, rede, disco), execução pode fugir ao controle  INFERIDO( consenso em práticas de sandbox).

- **Classificação NEXORA:** ADAPTAR  terminal deve ser estritamente sandboxado, com limites de recursos, network e permissões por ação( execução controlada  ver Security/Governance).

- **Dependências:** runtime de sandbox/container, política de permissões, limite de recursos, observabilidade de saída/erro.

- **Risco:** alto  execução de código arbitrário é o maior vetor de dano da plataforma.

- **Prioridade:** CRÍTICA.

- **Implicação arquitetural:** execução via sandbox( container/bubblewrap/isolamento), com default-deny de rede/acesso, quotas de CPU/RAM/tempo/disco, captura de saída/exit-code, auditoria de comandos.

##B4. Testes e verificação de código

- **Descrição:** executar suítes de teste existentes e criar novos testes para verificar mudanças antes de declarar conclusão.

- **Por que existe:** é a principal forma objetiva de verificação para código; sem testes, "funciona" vira opinião do modelo.

- **Referências:** Devin "build and test"( OBSERVADO); OpenHands roda testes e validação em benchmarks como SWE-bench( OBSERVADO); Claude Code integra execução de testes( INFERIDO a partir de docs; OBSERVADO parcialmente).
- **Evidência observável:** pipelines de agentes de codificação executam testes e iteram até passar( OBSERVADO  Devin blog; docs OpenHands).
- **Limitações:** testes podem ser insuficientes, flaky ou lentos; cobertura enganosa sem oráculo de qualidade  INFERIDO.

- **Classificação NEXORA:** SEORAR  verificação de código deve ir além de testes existentes: análise de cobertura, mutação/regressão, verificação de contrato e integração com o mecanismo de verificação do runtime( ver Agent Core).

- **Dependências:** terminal/sandbox, ferramentas de teste por linguagem, relatório de cobertura, serviço de verificação.

- **Risco:** médio  verificação superficial gera falsa confiança; testes mal isolados poluem o ambiente.

- **Prioridade:** ALTA.

- **Implicação arquitetural:** serviço de verificação reutilizável( testes, lint, build, análise estática), com relatórios estruturados e gates de qualidade configuráveis.

##B5. Debugging e análise de erros

- **Descrição:** diagnosticar falhas( ler stack traces, logs, estados), formular hipóteses e iterar até a causa raiz.

- **Por que existe:** falhas são inevitáveis em código; a diferença entre um agent útil e um frágil é a qualidade do diagnóstico.

- **Referências:** Devin "fix mistakes"( OBSERVADO); Claude Code e OpenHands expõem erros estruturados como observações( OBSERVADO); boas práticas de sandbox incluem logs e diagnóstico( OBSERVADO em guias de segurança).

- **Evidência observável:** ferramentas de bash retornam exit codes e stderr; agentes iteram com base no erro( OBSERVADO  docs OpenHands/Anthropic).
- **Limitações:** diagnóstico cego( tentativa e erro) é caro; sem contexto estruturado de falha, o agente da voltas  INFERIDO( reforçado por literatura de replanning).

- **Classificação NEXORA:** ADAPTARdebugging deve ser guiado por classificação de falha e contexto estruturado( integrado ao Error Recovery do Agent Core).

- **Dependências:** terminal, observabilidade( logs, tracing), memória episódica( erros passados), ferramentas de inspeção( debuggers).

- **Risco:** médio  tentativa-e-erro sem limites consome orçamento; acesso a logs sensíveis requer sanitização( ver Security).

- **Prioridade:** ALTA.

- **Implicação arquitetural:** captura estruturada de erros( tipo, stack, exit code, contexto), memória de falhas por projeto, políticas de tentativas com limite.

##B6. Refatoração

- **Descrição:** reestruturar código preservando comportamento( mover, extrair, renomear, simplificar), com verificação de que nada quebrou.

- **Por que existe:** parte substancial do trabalho real de engenharia; sem refatoração segura, o agente apenas empilha código.

- **Referências:** agentes de codificação executam refatoração em tarefas reais( INFERIDO a partir de capacidades de edição+testes; Devin/OpenHands resolvem tarefas que envolvem mudanças estruturais  OBSERVADO via benchmarks).

- **Evidência observável:** benchmarks de engenharia( SWE-bench) exigem mudanças estruturais em código real( OBSERVADO).
- **Limitações:** refatoração sem testes de guarda quebra comportamento silenciosamente; sem diff-review, mudanças invasivas passam despercebidas  INFERIDO.

 - **Classificação NEXORA:** ADAPTAR  refatoração deve ser sempre acompanhada de verificação( testes, lint, diff) e checkpoints para reversão( ver Security/Checkpoints).

 - **Dependências:** edição, testes/verificação, diff/checkpoints, memória de projeto.

 - **Risco:** médio  refatoração sem verificação é risco silencioso de regressão.

 - **Prioridade:** ALTA.

 - **Implicação arquitetural:** padrão "editar → verificar → commit/checkpoint" obrigatório para mudanças estruturais; gate de verificação configurável.

##B7. Build e integração

- **Descrição:** executar builds, resolver erros de compilação e integrações de dependências( instalar pacotes, gerenciar versões).

- **Por que existe:** código não compilado não é código útil; gerenciamento de dependências é parte essencial de qualquer projeto real.

 - **Referências:** Devin e OpenHands executam builds e instalações em sandbox( OBSERVADO  docs e fast.io); npm/pip/uv como ferramentas de terminal( OBSERVADO).

 - **Evidência observável:** agentes instalam dependências e rodam builds em execução real( OBSERVADO  Devin blog; OpenHands workflows).

 - **Limitações:** instalação de dependências arbitrárias é vetor de supply-chain attack( ver Security  reprodutibilidade e allowlists); builds longos consomem orçamento INFERIDO.

 - **Classificação NEXORA:** ADAPTAR  builds devem ser reproduzíveis e isolados( lockfiles, ambientes efêmeros), com política de instalação controlada.

 - **Dependências:** terminal/sandbox, gerenciador de pacotes, política de dependências( allowlist/verificação).

 - **Risco:** alto  dependências maliciosas ou builds poluidos são risco de segurança real.

 - **Prioridade:** ALTA

 - **Implicação arquitetural:** ambientes de build efêmeros e reproduzíveis; política de instalação de pacotes( por padrão bloqueada ou em allowlist); registro de dependências instaladas para auditoria.

##B8. Git e controle de versão

- **Descrição:** usar git para criar branches, commits, diff/review, revert e PRs, com convenções por projeto.

- **Por que existe:** é a espinha dorsal da colaboração em código; todo agent de codificação precisa operar o ciclo git com segurança.

 - **Referências:** OpenHands e Claude Code integram git( commit, push, PR)( OBSERVADO  docs; práticas documentadas); Devin "opens the pull request"( OBSERVADO  Devin Security Swarm blog).

 - **Evidência observável:** automação de commits/PRs documentada em múltiplas plataformas( OBSERVADO).

 - **Limitações:** push/merge automáticos são risco de governança; sem política de revisão humana, mudanças ruins entram na base de código INFERIDO( reforçado por guias de segurança: "agent commits are automatic, pushes require a human").

 - **Classificação NEXORA:** ADAPTAR  política de git controlada: commits automáticos possíveis, push/merge exigem aprovação conforme política( ver Security/Governance).

 - **Dependências:** ferramenta git, política de permissões por operação, checkpoints/reversão, identidade do agente.

 - **Risco:** médio-alto  push sem revisão é risco de governança e segurança.

 - **Prioridade:** ALTA

 - **Implicação arquitetural:** integração git com gates por operação( commit / push / merge / PR), rastreabilidade de autoria do agente, hooks de revisão/approval.

---

# C. Computer Use / Runtime

##C1. Browser

- **Descrição:** controlar um navegador para navegar, extrair conteúdo, interagir com formulários e validar aplicações web.

- **Por que existe:** parte crescente do trabalho( e das aplicações modernas) acontece no browser; e é o principal meio de teste de front-end e interação com serviços web.

- **Referências:** Devin inclui "headless browser" para testar apps web( OBSERVADO via fast.io); Anthropic Computer Use interage com qualquer software, incluindo browser( OBSERVADO via docs); Arena.ai oferece web search e coding assistance( OBSERVADO; browser explícito não confirmado  INFERIDO).

- **Evidência observável:** "headless browser" documentado no Devin; "computer use" documentado na Anthropic( OBSERVADO).
- **Limitações:** automação de browser é frágil( seletores, captchas, anti-bot); interação visual é cara computacionalmente INFERIDO.

- **Classificação NEXORA:** ADAPTAR  browser como ferramenta com escopo( leitura/extração mais simples que automação plena) e política de acesso por site/allowslist.

- **Dependências:** runtime de browser( headless/real), política de rede, extração de conteúdo( HTML→texto), memória de sessão web.

 - **Risco:** médio  browser pode vazar dados, fazer ações não desejadas( compras, envios) ou ser vetor de prompt injection INFERIDO( prática comum em segurança de agentes).

 - **Prioridade:** ALTA( para o uso de pesquisa e teste web)

 - **Implicação arquitetural:** ferramenta de browser com modo somente-leitura por padrão, allowlist de domínios, captura de screenshots/HTML, gates para ações destrutivas( formulários, envio)

##C2. Filesystem

- **Descrição:** operar sobre o sistema de arquivos( ler, criar, editar, organizar) dentro de um escopo definido por tarefa/projeto

- **Por que existe:** toda atividade de agente( codificação, pesquisa, automação) apoia-se em persistência de arquivos

- **Referências:** OpenHands workspace/file tools e Anthropic text editor tool operam sobre arquivos( OBSERVADO); sandboxes de agentes definem escopo de filesystem( OBSERVADO  Devin/fast.io)

 - **Evidência observável:** ferramentas de arquivo documentadas nas plataformas; sandboxes isolam diretórios de trabalho( OBSERVADO)

 - **Limitações:** acesso irrestrito ao filesystem é risco de vazamento/dano; sem escopo, exfiltração de dados sensíveis( INFERIDO  reforçado por guias de segurança: "block all reads outside the workspace unless approved")

 - **Classificação NEXORA:** ADAPTAR  filesystem com escopo por projeto e default-deny fora do workspace( permitido por allowlist)

 - **Dependências:** política de permissões, sandbox, memória de projeto( estrutura), auditoria de acesso

 - **Risco:** médio-alto  acesso fora de escopo pode vazar segredos ou danificar dados

 - **Prioridade:** CRÍTICA

 - **Implicação arquitetural:** camada de acesso a arquivos com escopo obrigatório( workspace raiz), allow/deny por path, auditoria de leituras/escritas.

##C3. Processos e recursos do sistema

- **Descrição:** gerenciar processos( iniciar, monitorar, encerrar), recursos( CPU, RAM, disco, rede) e limites de execução

- **Por que existe:** sem controle de processos, execuções longas ou fugas de recurso dominam a máquina e a conta

 - **Referências:** sandboxes profissionais limitam recursos e processos( OBSERVADO  guias de sandbox NVIDIA/TowardsAI); agentes matam servidores/deamons que iniciaram( INFERIDO a partir de capacidades de terminal)

 - **Evidência observável:** guias de sandbox prescrevem quotas e lifecycle management( OBSERVADO); prática de encerrar processos em agentes( INFERIDO)
 - **Limitações:** sem lifecycle management, processos órfãos acumulam-se; sem quotas, um comando pode exaurir recursos INFERIDO

 - **Classificação NEXORA:** ADAPTAR  o runtime deve gerenciar o ciclo de vida de processos por tarefa e impor quotas( CPU/RAM/tempo/disco/rede)

 - **Dependências:** sandbox, observabilidade de recursos, contadores de execução

 - **Risco:** médio  fuga de recursos ou processos órfãos degradam a plataforma

 - **Prioridade:** ALTA

 - **Implicação arquitetural:** runtime com gerenciamento de processos por sessão/tarefa( kill em cleanup), quotas de recursos, monitoramento de uso( integrado a observabilidade e a Autonomy)

##C4. Observação do ambiente

- **Descrição:** capturar observações do ambiente( saída de comandos, screenshots, HTML, estado de arquivos, logs) para realimentar o agente

 - **Por que existe:** é o "sentido" do agente; sem observação rica, o agente age no escuro

 - **Referências:** console/screenshot no Anthropic Computer Use( OBSERVADO); terminal output e file content no OpenHands( OBSERVADO); screenshots/HTML no Devin browser( OBSERVADO)

 - **Evidência observável:** tool outputs( textos, imagens, metadados) documentados nas plataformas( OBSERVADO)

 - **Limitações:** observação textual perde contexto visual; observação visual é cara e imprecisa( OCR, resolução) INFERIDO

 - **Classificação NEXORA:** ADAPTAR  observações devem ser estruturadas( tipo, formato, metadados) e armazenáveis( para memória e auditoria)

 - **Dependências:** ferramentas( terminal, browser, filesystem), schema de observação, armazenamento de eventos

 - **Risco:** baixo  observação em si é segura; risco de capturar dados sensíveis em logs( sanitização  ver Security)

 - **Prioridade:** ALTA

 - **Implicação arquitetural:** schema unificado de observações( evento de primeira classe), sanitização de segredos em saídas, persistência para replay/auditoria

---

# D. Research

##D1. Busca e coleta de informação

- **Descrição:** pesquisar na web e em fontes internas, coletar conteúdo relevante( páginas, documentos, APIs ) de forma estruturada e citável.

- **Por que existe:** é a base do trabalho de pesquisa e da alimentação de conhecimento da NEXORA( North Star: aprender sobre o mundo ).
- **Referências:** Arena.ai Agent Mode inclui web search( OBSERVADO ); agentes de pesquisa modernos e frameworks como OpenHands com browser/web tools( OBSERVADO ); Devin usa browser para consultar docs( OBSERVADO ).
- **Evidência observável:** web search documentado na Arena.ai; ferramentas de web/browser no OpenHands( OBSERVADO ).
- **Limitações:** busca crua retorna ruído e fontes não confiáveis; sem pipeline de extração e verificação, a pesquisa fica superficial( INFERIDO ).
- **Classificação NEXORA:** ADAPTAR  busca deve alimentar um pipeline( coleta → ranking → verificação → síntese ) com citação obrigatória de fontes.

- **Dependências:** ferramenta de web/browser, política de rede, extração de conteúdo, armazenamento( memória semântica ).
- **Risco:** médio  fontes não confiáveis ou prompt injection via conteúdo web( ver Security ).
- **Prioridade:** ALTA.

- **Implicação arquitetural:** pipeline de pesquisa( search → fetch → extract → rank → verify → synthesize ), citação estruturada, sanitização de conteúdo externo( tratar como não confiável ).

##D2. Fontes e verificação de informação

- **Descrição:** rastrear, avaliar e verificar fontes( credibilidade, consistência, atualidade, corroboração ) antes de aceitar informação como fato.

- **Por que existe:** informação falsa ou desatualizada propaga erro em decisões e produtos( risco direto à North Star ).
- **Referências:** práticas de fact-checking e citação em pesquisa( OBSERVADO em literatura geral de agentes de pesquisa); não é capacidade destacada nas referências principais  INFERIDO que é responsabilidade do pipeline ).
- **Evidência observável:** ausência de mecanismo de verificação de fontes destacado nas referências de produto( INFERIDO  lacuna observada ).
- **Classificação NEXORA:** SUPERAR  a NEXORA deve implementar verificação de fontes como etapa explícita e auditável do pipeline( citação, confiabilidade, consistência entre fontes ).
- **Dependências:** pipeline de pesquisa, memória semântica, política de confiança de domínios( allowlist/denylist e reputação ).
- **Risco:** médio  aceitar fontes ruins contamina conhecimento persistente(a longo prazo é pior que erro pontual ).
- **Prioridade:** ALTA.

- **Implicação arquitetural:** componente de verificação de fontes com graus de confiança, rastreabilidade de origem por fato armazenado( provenance ), revisão antes de persistir conhecimento.

##D3. Síntese e comparação

- **Descrição:** combinar múltiplas fontes em uma resposta coerente, comparar alternativas( modelos, produtos, abordagens ) com critérios explícitos.

- **Por que existe:** é o que transforma coleta em entendimento utilizável;e é base de análise de mercado e oportunidades( North Star ).
- **Referências:** pesquisa e planejamento são categorias de uso da Arena.ai( OBSERVADO  11% research, 11% planning );agentes de análise comparativa( INFERIDO a partir de casos de uso documentados ).
- **Evidência observável:** categorias "Research & Planning" listadas no blog da Arena.ai( OBSERVADO ).
- **Limitações:** síntese sem critérios vira opinião não rastreável;comparação sem métricas claras é arbitrária( INFERIDO ).
- **Classificação NEXORA:** ADAPTAR  síntese com estrutura exigida( tese, evidência, limitações, fontes ) e comparação com critérios explícitos( preço, performance, trade-offs ).
- **Dependências:** pipeline de pesquisa, verificação, memória semântica, template de saída.

- **Risco:** baixo-médio  má síntese gera decisões ruins;sem citação,não é auditável.

- **Prioridade:** ALTA.

- **Implicação arquitetural:** formatos de saída estruturados para síntese e comparação( schema de relatório ), integração com citação/provenance.

##D4. Pesquisa contínua e atualização de conhecimento

- **Descrição:** monitorar fontes( feeds, changelogs, mercados ) ao longo do tempo e atualizar o conhecimento persistente da NEXORA

- **Por que existe:** o mundo muda;conhecimento desatualizado degrada a North Star( identificar oportunidades atuais ).
- **Referências:** nenhuma das referências principais destaca pesquisa contínua( OBSERVADO  lacuna );automações de monitoramento existem no ecossistema( INFERIDO a partir de práticas de agentes de monitoramento ).
- **Evidência observável:** ausência de pesquisa contínua nas referências de produto coletadas( OBSERVADO  lacuna ).
- **Classificação NEXORA:** CRIAR  monitoramento contínuo de fontes autorizadas, com consolidação periódica no conhecimento persistente e gatilhos de atualização/notificação
- **Dependências:** memória semântica e de decisões, pipeline de pesquisa, scheduler( ver Autonomy ), política de escopo de monitoramento
- **Risco:** médio  custo contínuo de monitoramento e risco de viés de fontes;sobrescrever conhecimento é arriscado( versionamento ).
- **Prioridade:** MÉDIA( pós-MVP )
- **Implicação arquitetural:** sistema de monitoramento com agenda configurável, detecção de mudanças, atualização versionada do conhecimento( sem destruir conhecimento anterior ).

---

# E. Memory

##E1. Memória de curto prazo( working/short-term )

- **Descrição:** manter o contexto ativo da tarefa atual( histórico de passos, observações recentes, plano em andamento ) com acesso rápido e rotação controlada
- **Por que existe:** é o substrato do raciocínio e da execução coerente dentro de uma sessão
- **Referências:** short-term memory é padrão em arquiteturas de agente( OBSERVADO  literatura de memória de agentes );Claude Code e OpenHands mantêm histórico de conversa/sessão( OBSERVADO ).
- **Evidência observável:** termos working memory e session context na literatura de memória de agentes( OBSERVADO ).
- **Limitações:** janela finita; sem compressão, estoura ou custa caro( ver Context Management ).
- **Classificação NEXORA:** REPLICAR  memória de curto prazo como estado de sessão do runtime
- **Dependências:** gerenciamento de contexto, armazenamento de eventos, política de rotação/compressão
- **Risco:** baixo  risco é de qualidade( perda de contexto ), não de segurança
- **Prioridade:** CRÍTICA
- **Implicação arquitetural:** estado de sessão com rotação configurável( janela de eventos ), integração com sumarização e recuperação

##E2. Memória de longo prazo( semantic / episodic / procedural )

- **Descrição:** persistir conhecimento entre sessões, dividido em:semântica( fatos, conceitos, preferências ), episódica( eventos, decisões, falhas, sucessos ) e procedural( estratégias, procedimentos, habilidades )
- **Por que existe:** é o que transforma um agente stateless em um sistema que aprende com a experiência( North Star: aprender continuamente )
- **Referências:** literatura de memória de agentes identifica episodic, semantic, procedural como os três tipos de longo prazo( OBSERVADO  survey arXiv 2602.06052 );implementações usam vector DBs e knowledge graphs( OBSERVADO  memória em agentes modernos )
- **Evidência observável:** taxonomia episodic/semantic/procedural é consenso na literatura( OBSERVADO );arquiteturas hot/warm/cold tiering são padrão( OBSERVADO )
- **Limitações:** armazenar tudo é ruído;recuperação por similaridade pura é insuficiente( requer governance, versioning, provenance )( OBSERVADO  apontado por fontes de memória )
- **Classificação NEXORA:** ADAPTAR  memória de longo prazo com os três tipos, governança e versionamento, e recuperação combinando similaridade+metadados+política de relevância
- **Dependências:** armazenamento( vetorial/estruturado ), serviço de recuperação, política de escrita( o que merece persistir ), verificação de conhecimento( provenance ))
- **Risco:** médio-alto  conhecimento incorreto persistente se propaga e envenena o futuro( mais perigoso que erro efêmero ))
- **Prioridade:** ALTA( desde cedo, mesmo que simples;full vetorial depois ))
- **Implicação arquitetural:** serviço de memória com schemas por tipo, versionamento, provenance de fontes, política de consolidação e poda( forget ), e sanitização de dados sensíveis

##E3. Memória de projeto( project memory )

- **Descrição:** manter contexto específico por repositório/projeto( estrutura, convenções, decisões, estado, comandos úteis ) persistente entre as tarefas
- **Por que existe:** tarefas de codificação repetem descobertas;sem memória de projeto,toda tarefa recomeça do zero( desperdício e erro )
- **Referências:** AGENTS.md e arquivos de contexto em repositórios são padrão do OpenHands( OBSERVADO  prática documentada );Claude Code usa CLAUDE.md/skills de projeto( OBSERVADO )
- **Evidência observável:** arquivos de memória de repositório( AGENTS.md, CLAUDE.md ) são documentos vivos documentados pelas plataformas( OBSERVADO )
- **Limitações:** arquivos estáticos desatualizam;sem atualização disciplinada, tornam-se ruído( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  memória de projeto versionada, mantida por política de atualização( revisitar e consolidar ) e alimentada por memória episódica de decisões
- **Dependências:** memória de longo prazo, ferramentas de arquivo, política de atualização de memória
- **Risco:** baixo-médio  memória de projeto desatualizada induz decisões erradas
- **Prioridade:** ALTA
- **Implicação arquitetural:** bloco de memória de projeto por repositório com processo de revisão/consolidação( ex:após cada tarefa concluída ), rastreabilidade de quando foi atualizado

##E4. Memória de decisões, falhas e sucessos( experience memory )

- **Descrição:** registrar decisões tomadas( e por quê ), falhas( e causa ), sucessos( e o que funcionou ) para influenciar decisões futuras
- **Por que existe:** aprender com a experiência requer registrar não só resultados, mas o contexto e o raciocínio que levaram a eles
- **Referências:** Devin "learn over time,and fix mistakes"( OBSERVADO  superfície documentada );memória episódica captura eventos e outcomes( OBSERVADO  literatura de memória )
- **Evidência observável:** Devin afirma aprender ao longo do tempo( OBSERVADO );taxonomia de memória episódica inclui outcomes( OBSERVADO )
- **Limitações:** sem registro estruturado de decisão,o aprendizado é vago;sem revisão periódica,falhas se repetem( INFERIDO )
- **Classificação NEXORA:** SUPERAR a NEXORA deve implementar registro estruturado de decisões e lições( decision log + lessons learned ), com recuperação ativa quando decisões similares surgirem
- **Dependências:** memória episódica, observabilidade( registrar eventos de decisão ), política de revisão/reflexão periódica
- **Risco:** médio  lições erradas ou desatualizadas enviesam decisões futuras;é preciso carimbar validade( quando aprendida, quando revisada )
- **Prioridade:** ALTA( pós-MVP )
- **Implicação arquitetural:** decision log e lições como tipos de memória versionados, com gatilhos de recuperação( quando uma decisão similar está sendo tomada ), e ciclo de reflexão( retrospectiva )

---

# F. Planning

##F1. Decomposição de objetivos em subtarefas

- **Descrição:** transformar um objetivo estruturado em uma lista de subtarefas executáveis, com granularidade adequada e critérios de conclusão por tarefa
- **Por que existe:** é o que transforma intenção em trabalho;sem decomposição, o agente apenas responde, não executa multi-etapas
- **Referências:** Arena.ai multi-step workflow( OBSERVADO );task planning and decomposition no OpenHands SDK( OBSERVADO );Devin plan and execute complex engineering tasks( OBSERVADO )
- **Evidência observável:** docs do OpenHands listam task planning/decomposition como feature( OBSERVADO )
- **Limitações:** decomposição ingênua( linear,sem dependências ) falha em tarefas do mundo real;granularidade errada( grande demais ou pequena demais ) degrada a execução( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  decomposição com critérios de conclusão por subtarefa e dependências explícitas( integrada a F2/F3 )
- **Dependências:** interpretador de objetivos, schema de plano, providers( para planejar ), memória de estratégias( procedural )
- **Risco:** médio  plano ruim propaga erro para toda a execução
- **Prioridade:** CRÍTICA

- **Implicação arquitetural:** artefato `Plano` com nós( subtarefas ), arestas( dependências ), metadados( critérios, dono, estado ), versionável e auditável

##F2. Grafo de tarefas( DAG ) e dependências

- **Descrição:** representar o plano como grafo acíclico dirigido( DAG ), com dependências explícitas entre subtarefas e identificação de partes paralelizáveis
- **Por que existe:** tarefas reais têm pré-requisitos e passos independentes;DAG permite paralelismo correto e ordenação segura

- **Referências:** DAG-based task planning é padrão em orquestração de tarefas de LLM e robótica( OBSERVADO  literatura:DAG-Plan, scheduler-theoretic frameworks );task graph planning: explicit dependencies( OBSERVADO  fontes de planejamento )
- **Evidência observável:** literatura documenta ganhos de eficiência e correção com DAG em relação a planos lineares( OBSERVADO )
- **Limitações:** LLM erra ao gerar DAGs( dependências implícitas perdidas, paralelismo falso  OBSERVADO em literatura de planejamento );validação do grafo é necessária

- **Classificação NEXORA:** ADAPTAR  DAG com validação de dependências( checagem de impossibilidade, ciclos ) e metadados para scheduler

- **Dependências:** schema de plano( DAG ), validação de grafo, scheduler, monitoramento de estado por nó
- **Risco:** médio  DAG inválido gera execução incorreta ou paralelismo perigoso
- **Prioridade:** ALTA
- **Implicação arquitetural:** representação de plano como DAG validável( acíclico,dependências realizáveis ), com estado por nó( pending/ready/running/done/failed ) e visão de caminho crítico

##F3. Scheduler e execução do plano

- **Descrição:** agendar e executar subtarefas respeitando dependências( o que pode rodar agora ), paralelismo seguro e limites de concorrência
- **Por que existe:** sem scheduler, dependências são violadas ou tudo roda serializado( perde paralelismo );e paralelismo sem limite é risco de custo/recursos
- **Referências:** modelos de orquestração multi-agente descrevem orchestration layer planejando e executando( OBSERVADO  literatura de multi-agent orchestration );task DAG scheduling com métricas de critical path( OBSERVADO  literatura )
- **Evidência observável:** frameworks de orquestração com scheduler e filas de execução( OBSERVADO );papers formalizam agendamento de tarefas de agente( OBSERVADO )
- **Limitações:** scheduler ingênuo não lida com falhas( ver F4);concorrência infinita estoura orçamento( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  scheduler com prioridades,concorrência limitada por política( custo/recursos ), e awareness de orçamento global
- **Dependências:** plano( DAG ), runtime de execução, políticas de orçamento, observabilidade, tratamento de falhas
- **Risco:** médio  scheduler sem limites dispara custo;sem monitoramento,falhas encavalem

- **Prioridade:** ALTA
- **Implicação arquitetural:** motor de agendamento com filas por dependência,semáforo de concorrência,contabilidade de orçamento por tarefa/sessão,integração com observabilidade

##F4. Verificação e replanejamento( recovery )

- **Descrição:** verificar resultados de subtarefas( critérios de conclusão, testes, inspeção ) e, em falha, replanejar localmente( refazer aquela parte ) ou globalmente( revisar o plano )
- **Por que existe:** planos falham na prática;verificação entre etapas é o que impede que um erro se propague silenciosamente
- **Referências:** add replanning on failure é recomendação explícita em técnicas de planejamento( OBSERVADO  fontes de planning );literatura de agendamento descreve LLM-driven recovery module com replanejamento local( OBSERVADO  MDPI paper )
- **Evidência observável:** documentação de agent planning recomenda replanning on failure como prática de produção( OBSERVADO );papers mostram ganhos com replanejamento local vs reinício( OBSERVADO )
- **Limitações:** replanejamento sem classificação de falha desperdiça esforço;verificação ausente torna replanejamento cego( INFERIDO  alinhado a A8 )
- **Classificação NEXORA:** SUPERAR  verificação entre etapas + replanejamento local/global guiado por classificação de falha( integrado ao Error Recovery ), com gates antes de ações destrutivas
- **Dependências:** serviço de verificação( testes, checagem estrutural ), tratamento de falhas, memória de decisões( aprender com replanejamentos ), monitoramento de progresso
- **Risco:** alto  sem verificação,o plano conclui com resultado errado;sem replanejamento,tarefas morrem à toa
- **Prioridade:** CRÍTICA

- **Implicação arquitetural:** gates de verificação entre subtarefas( configuráveis por tipo ), motor de replanejamento local/global, registro de decisões de replanejamento( para memória e auditoria )

---

# G. Multi-Agent

##G1. Orquestração( orchestrator )

- **Descrição:** coordenar múltiplos agentes especializados rumo a um objetivo comum, decidindo quem age, quando e com que contexto( orchestration layer )( planejamento, execução, quality control )
- **Por que existe:** a visão da NEXORA inclui agentes especializados trabalhando juntos;tarefas complexas se dividem naturalmente entre especialistas
- **Referências:** multi-agent orchestration é padrão documentado( OBSERVADO  literatura: orchestrated multi-agent systems, Microsoft MARA, Google ADK ); OpenHands CLI suporta sub-agents e micro-agentes( OBSERVADO  docs SDK )
- **Evidência observável:** frameworks de orquestração( orchestrator, classifier de intents, registry, agent lifecycle ) descritos em arquiteturas de referência( OBSERVADO  Microsoft MARI)
- **Limitações:** sobrecarga de comunicação e coordenação( communication overhead );agentes com objetivos conflitantes exigem mecanismos de resolução( OBSERVADO  literatura de multi-agent orchestration )
- **Classificação NEXORA:** ADAPTAR  orquestração com registro de agentes, roteamento por intenção/capacidade e política global de contexto/orçamento/autorização(`análise`))
- **Dependências:** agent registry, comunicação entre agentes, política de delegação, observabilidade, verificação de resultados( aggregation )
- **Risco:** médio  orquestração sem governança gera custos descontrolados e resultados inconsistentes;agentes com permissões amplas são risco de segurança( ver Security )
- **Prioridade:** ALTA( pós-MVP;para o MVP inicial,um agente único orquestrado internamente basta )
- **Implicação arquitetural:** componente orchestrator no runtime, com fila de tarefas e atribuição a agentes registrados, gates de autorização por delegação e consolidação de resultados( ver G6 )

 >>>>>

##G2. Registro de agentes( agent registry )

- **Descrição:** catálogo de agentes disponíveis com metadados( especialidade, capacidades, permissões, custo, estado, versão ) e descoberta por capacidade
- **Por que existe:** sem registro, delegação é ad-hoc e insegura;com registro,a orquestração se torna declarativa e auditável
- **Referências:** agent registry e agent discovery são componentes de arquiteturas de referência multi-agente( OBSERVADO  Microsoft MARI: registry for agent discovery and lifecycle management )
- **Evidência observável:** o registry é listado como componente central do orchestration layer( OBSERVADO )
- **Limitações:** registro estático desatualiza;sem versionamento de capacidades, agentes quebrados permanecem elegíveis( INFERIDO )
- **Classificação NEXORA:** REPLICAR  como componente estrutural do runtime( registry declarativo, versionado, com permissões e custos )
- **Dependências:** schema de agente, política de permissões, observabilidade( estado/versão )
- **Risco:** médio  registro sem permissões explícitas permite delegação insegura
- **Prioridade:** ALTA( acompanha multi-agent )
- **Implicação arquitetural:** agent registry versionado com capacidade/permissão/custo por entrada, API de descoberta, auditoria de uso( quem delegou a quem )

 >>>>>

##G3. Especialização e delegação

- **Descrição:** criar/utilizar agentes especializados( coding, research, análise, etc. ) e delegar subtarefas a eles com contexto e critérios claros
- **Por que existe:** especialistas produzem melhor resultado por tarefa que um generalista tentando tudo( foco, memória e ferramentas específicas )
- **Referências:** "specialized agents" são a base do multi-agent orchestration( OBSERVADO  literatura; cada agente possui role/capability );OpenHands micro-agentes e sub-agents( OBSERVADO  docs )
- **Evidência observável:** agentes especializados por papel,são descritos como blocos fundamentais de sistemas orquestrados( OBSERVADO )
- **Limitações:** delegação sem contexto suficiente gera retrabalho;especialização excessiva fragmenta o conhecimento( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  delegação com contrato explícito( objetivo, contexto, critérios de sucesso, limites, orçamento ) e verificação de resultado antes de aceitar
- **Dependências:** orchestrator, agent registry, comunicação, verificação, memória compartilhada( ou handoff de contexto )
- **Risco:** médio  agente delegado sem limites pode agir fora de escopo( reforça necessidade de permissões por agente )
- **Prioridade:** ALTA( pós-MVP )
- **Implicação arquitetural:** contrato de delegação tipado( task packet ), permissões por agente( ver Security ), handoff de contexto explícito, verificação do entregável antes da consolidação.


##G4. Comunicação entre agentes

- **Descrição:** troca de mensagens, contexto e resultados entre agentes( e entre agentes e orquestrador ), com protocolo comum e semântica clara

- **Por que existe:** sem protocolo de comunicação, integração vira acoplamento frágil e incompreensível
- **Referências:** A2A( agent-to-agent ) e MCP são protocolos emergentes para comunicação inter-agentes e ferramentas( OBSERVADO  literatura de orchestration: standardized protocols such as MCP and A2A );semântica de mensagens em sistemas orquestrados( OBSERVADO )
- **Evidência observável:** protocolos A2A e MCP citados como padrões em orquestração multi-agente( OBSERVADO )
- **Limitações:** comunicação excessiva é custo;mensagens sem schema evoluem mal; protocolos externos maduros ainda jovens( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  comunicação interna com schema de mensagens tipado( eventos estruturados ), e adoção de protocolos abertos( MCP para ferramentas) quando benéfico, sem acoplar o núcleo a um padrão específico
- **Dependências:** event store/estado, schema de mensagens, verificação( mensagens validadas )
- **Risco:** médio  comunicação sem schema vira bagunça;mensagens não auditadas enfraquecem governança
- **Prioridade:** ALTA( pós-MVP )
- **Implicação arquitetural:** camada de comunicação baseada em eventos tipados( reutilizando o event store do estado ), schemas JSON por tipo de mensagem, auditoria de trocas


##G5. Revisão cruzada e resolução de conflitos

- **Descrição:** agentes revisarem o trabalho uns dos outros( cross-review ) e mecanismos para resolver conflitos( divergência de resultados, objetivos concorrentes, disputa de recursos )
- **Por que existe:** revisão cruzada captura erros que o autor não vê;conflitos sem resolução travam o sistema degradam a qualidade
- **Referências:** conflict resolution é listada como requisito de multi-agent orchestration( OBSERVADO  literatura );Devín Security Swarm usa paralelismo de agentes para encontrar falhas( OBSERVADO  map-reduce architecture )
- **Evidência observável:** conflict resolution mechanisms citados como essenciais em orquestração( OBSERVADO );casos reais de revisão paralela( Devin Security Swarm  OBSERVADO )
- **Limitações:** revisão cruzada multiplica custo;conflito sem arbitragem clara( quem decide? ) gera empate INFERIDO
- **Classificação NEXORA:** ADAPTAR  revisão cruzada seletiva( por criticidade ),com política de arbitragem( auto-resolução por regra, escalonamento humano em conflitos de alto impacto )
- **Dependências:** comunicação,verificação de resultados,política de escalonamento,observabilidade
- **Risco:** médio  arbitragem sem política clara gera decisão arbitrária ou paralisia
- **Prioridade:** MÉDIA-ALTA( pós-MVP )
- **Implicação arquitetural:** hooks de revisão por criticidade de tarefa, mecanismo de resolução configurável( regra/modelo/humano ), registro de conflitos e resoluções( memória )


##G6. Consolidação de resultados( result aggregation )

- **Descrição:** combinar resultados de múltiplos agentes/subtarefas em um entregável coerente, detectando inconsistências e aplicando critérios de aceitação
- **Por que existe:** o valor do multi-agente aparece na consolidação;resultados soltos não são um produto

- **Referências:** result aggregation e agent verification são citados como componentes do orchestration layer( OBSERVADO  literatura de orchestration );map-reduce( agregação de achados ) é o padrão do Devin Security Swarm( OBSERVADO )
- **Evidência observável:** arquiteturas orquestradas incluem quality control e agregação( OBSERVADO )
- **Limitações:** agregação sem critérios de aceitação acumula lixo;inconsistências entre agentes sem detecção geram entregáveis contraditórios( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  consolidação com validação de consistência( checagem cruzada, schema de entregável ) e critérios de aceitação explícitos
- **Dependências:** comunicação,verificação,memória de curto prazo( contexto do entregável ),policy de aceitação
- **Risco:** médio  entregável inconsistente é pior que ausência de entrega( dano reputacional e retrabalho )
- **Prioridade:** ALTA( pós-MVP )
- **Implicação arquitetural:** etapa de consolidação no ciclo do orquestrador, com validação de schema e consistência, e gates de aceitação( aceitar/rejeitar/escalonar )


---

# H. Providers

##H1. Abstração de provider( interface comum )

- **Descrição:** camada que padroniza a interação com diferentes serviços de IA( chat, streaming, tool-calling, visão, erros ), expondo uma única interface ao núcleo
- **Por que existe:** é o princípio arquitetural central da NEXORA( inteligência não presa a um fornecedor );permite adicionar providers sem reescrever o núcleo
- **Referências:** princípio model-agnostic é central no OpenHands( OBSERVADO  docs: model-agnostic architecture );provider abstraction é recomendada em roteamento de modelos( OBSERVADO  MindStudio: abstract provider-specific API details )
- **Evidência observável:** "model-agnostic" é termo usado explicitamente pelo OpenHands( OBSERVADO );práticas de roteamento usam abstração de provider( OBSERVADO )
- **Limitações:** abstração excessiva achata capacidades específicas( ex: reasoning, tool-calling avançado ) INFERIDO;padronizar demais esconde diferenças úteis dos modelos
- **Classificação NEXORA:** REPLICAR  como porta( interface ) de primeira classe, com schema comum mas capacidade de expor capacidades específicas( capability negotiation )
- **Dependências:** schema de chamada/resposta, detecção de capacidades, política de roteamento, tracking de custo
- **Risco:** alto se mal desenhada  acopla o núcleo a um provider específico na prática( violando o princípio )
- **Prioridade:** CRÍTICA( é a fundação do princípio arquitetural )
- **Implicação arquitetural:** interface `Provider` com contrato tipado( generate/stream/tools/capabilities/errors ), implementações por provider, registro de providers( sem tocar o núcleo ), negociação de capacidades( o que este modelo sabe fazer? )


##H2. Múltiplos modelos e troca dinâmica

- **Descrição:** operar com múltiplos modelos( de um ou vários providers ) e permitir troca por tarefa, por etapa do plano( planejador usa modelo forte; executor usa modelo rápido ), ou por política( custo, latência, qualidade )
- **Por que existe:** nenhum modelo é ótimo para tudo;troca dinâmica otimiza custo/qualidade e reduz dependência de um fornecedor

- **Referências:** model routing é camada de decisão entre "the agent needs to call an LLM" e "this specific API endpoint gets called"( OBSERVADO  literatura de roteamento );roters como OpenRouter e Braintrust oferecem seleção por preço/latência/qualidade( OBSERVADO )
- **Evidência observável:** fallback chains ordernadas, live model switching, capacity-aware routing documentados( OBSERVADO  literatura de roteamento )
- **Limitações:** troca excessiva pode gerar comportamento inconsistente( resultados de modelos diferentes divergem );roteamento por heurística simples pode escolher mal( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  troca por política explícita( por tipo de tarefa, orçamento, resultados medidos ), com consistência controlada( contexto compartilhado, políticas de seleção rastreáveis )
- **Dependências:** abstraction de provider, model registry, política de roteamento, tracking de custo/qualidade, fallback
- **Risco:** médio  roteamento ruim degrada qualidade ou estoura custo;sem rastreabilidade,vira caixa-preta( ver K Auditoria )
- **Prioridade:** CRÍTICA( princípio central da NEXORA )
- **Implicação arquitetural:** model registry com metadados( capacidades, custo, latência, contexto ),policy de roteamento plugável( estática por tarefa, dinâmica por orçamento/qualidade ),decisões de roteamento registradas como eventos


##H3. Combinação de modelos( multi-model workflows )

- **Descrição:** usar modelos diferentes em sequência ou em paralelo no mesmo fluxo( ex:gerador propõe, verificador valida, planejador planeja, executor executa com modelo mais barato )
- **Por que existe:** permite orquestrar forças de modelos distintos( qualidade no que importa, velocidade/custo no resto )
- **Referências:** pipelines multi-modelo são prática em agentes avançados( INFERIDO a partir da literatura de roteamento e de arquiteturas que separam planejador/executor/verificador );"routing by task type against model capabilities"( OBSERVADO  Zylos, Model Capability Matrix )
- **Evidência observável:** capability matrix( mapear tipos de tarefa contra capacidades de modelos ) é recomendação explícita( OBSERVADO )
- **Limitações:** coordenação entre modelos exige passagem de contexto estruturada;sem contrato,formatos incompatíveis quebram o fluxo( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  composição de modelos por papel( planner, executor, reviewer ),com passagem de contexto contratual e validação entre etapas
- **Dependências:** abstraction, model registry, planejamento( plano como contrato entre etapas ),verificação,ormamento
- **Risco:** médio  combinação sem contrato gera resultados inconsistentes;custo se multiplica sem governança
- **Prioridade:** ALTA( posterior ao MVP )
- **Implicação arquitetural:** papéis de modelo configuráveis por tipo de etapa do plano,contrato de passagem( o que uma etapa entrega à próxima ),verificação entre modelos( reviewer )


##H4. Modelos locais e online( on-prem )

- **Descrição:** suportar tanto providers online( Groq, OpenAI, Anthropic) quanto modelos locais( Ollama, vLLM, etc. ),com mesma interface
- **Por que existe:** modelos locais oferecem privacidade,custo fixo e disponibilidade offline; a NEXORA deve poder escolher entre eles por tarefa/política

- **Referências:** ecosistema de modelos locais via Ollama/vLLM é amplamente documentado( OBSERVADO  prática comum );roteadores suportam providers e modelos próprios( OBSERVADO  OpenRouter, LiteLLM )
- **Evidência observável:** ferramentas como LiteLLM roteiam entre providers online e locais com interface unificada( OBSERVADO )
- **Limitações:** modelos locais têm qualidade variável e exigem hardware;desempenho inconsistente sem benchmark próprio( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  modelos locais como providers de primeira classe( mesma porta, metadados de capacidade/custo/qualidade ),com política de escolha por tarefa( privacidade,custo,qualidade )
- **Dependências:** abstraction, model registry, benchmark interno( qualidade medida in-house ),política de roteamento
- **Risco:** baixo-médio  qualidade de modelo local não medida gera expectativa errada( benchmark resolve )
- **Prioridade:** MÉDIA( pós-provider online )
- **Implicação arquitetural:** implementações de provider local( via adaptadores padrão ),benchmark interno por modelo,metadados de capacidade/qualidade/custo por entrada do registry,política de roteamento considerando modelo local para dados sensíveis( ver Security/K )


##H5. Fallback e resiliência de provider

- **Descrição:** em falha( timeout, rate-limit, erro 5xx, indisponibilidade ),redirecionar automaticamente para outro provider/modelo segundo política( fallback chains, cooldowns, circuit breakers )
- **Por que existe:** providers falham na prática;fallback é o que mantém a plataforma operacional e sem intervenção manual


- **Referências:** fallback chains e cooldown são padrão em roteamento de modelos( OBSERVADO  LiteLLM: allowed_fails + cooldown mechanism );OpenRouter oferece fallback automático( OBSERVADO )
- **Evidência observável:** mecanismos de fallback documentados em roteadores comerciais e open-source( OBSERVADO )
- **Limitações:** fallback sem classificação de erro( permanente vs transitório ) mascara problema; fallback para modelo muito inferior degrada resultado silenciosamente( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  fallback com política explícita( classificação de erro, cooldown por modelo, circuito por provider ),visibilidade( o fallback aconteceu e por quê )) e custo/qualidade rastreados
- **Dependências:** abstraction, model registry, observabilidade( latência,erros, custo ),política de resiliência
- **Risco:** alto se mal feito  falha de provider derruba a plataforma inteira; fallback cego degrada qualidade sem aviso
- **Prioridade:** CRÍTICA( primeira entrega: pelo menos 2 providers ou fake provider )
- **Implicação arquitetural:** política de fallback por modelo/provider( ordem,cooldown,circuito ),erros tipados( rate-limit, timeout, auth ),registro de eventos de fallback( auditoria e melhoria de política )


##H6. Seleção de provider por tarefa( routing por capacidade )

- **Descrição:** escolher qual provider/modelo atende cada tarefa( ou etapa ) com base em capacidade( precisa tool-calling? visão? janela grande? ),custo,latência e qualidade medida
- **Por que existe:** muda o custo e a qualidade real da plataforma;é parte do princípio de não ficar preso a um modelo


- **Referências:** Model Capability Matrix mapeia tipos de tarefa contra capacidades de modelo( OBSERVADO  Zylos );routing decisions conectadas a measured answer quality( OBSERVADO  Braintrust )
- **Evidência observável:** recomendação explícita de criar capability matrix antes de construir router( OBSERVADO )
- **Limitações:** qualidade medida exige infraestrutura de avaliação( ver I Evolution );rotas estáticas desatualizam com novos modelos( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  roteamento por política declarável( capacidade necessária + restrições de custo/privacidade + qualidade medida ),com dados de avaliação realimentando a política
- **Dependências:** model registry( metadados ),benchmark/avaliação,ormamento,política de privacidade( ver K )
- **Risco:** médio  roteamento por capacidade sem dados reais escolhe mal;política opaca é inauditável
- **Prioridade:** ALTA( evolui com o tempo;versão 1 pode ser estática por tipo de tarefa )
- **Implicação arquitetural:** atributos de capacidade por modelo no registry,sistema de avaliação( ver I ),política de roteamento como código declarativo( auditável, testável ),eventos de decisão de roteamento( para melhoria contínua )


##H7. Rastreamento de custo( cost tracking )

- **Descrição:** medir e atribuir custo( por chamada, modelo, tarefa, sessão, agente, objetivo ) e expor orçamentos e alertas
- **Por que existe:** sem custo rastreado,não dá para governar autonomia,priorizar tarefas nem avaliar ROI( North Star: transformar valor em recursos  custo é central )
- **Referências:** roteadores expõem preço por modelo e custo por requisição( OBSERVADO  OpenRouter,Braintrust );boas práticas de agentes incluem monitoramento de custo( INFERIDO  implícito em orçamento de agentes;reforçado por governança de agentes )
- **Evidência observável:** métricas de custo por requisição/modelo documentadas em roteadores( OBSERVADO )
- **Limitações:** custo de tool/execução( não só LLM ) também precisa ser rastreado( CPU,sandbox, APIs externas ) INFERIDO
- **Classificação NEXORA:** SUPERAR  cost accounting abrangente( LLM + ferramentas + infraestrutura ),por agente/tarefa/objetivo,com orçamentos e alertas( integrado a Autonomy e ao Economic Engine )
- **Dependências:** abstraction( metadados de custo por chamada ),tool runtime( custo por execução ),contabilidade( ledger ),políticas de orçamento
- **Risco:** alto  sem cost tracking,autonomia estoura custo sem freio( ameaça a sustentabilidade da North Star )
- **Prioridade:** CRÍTICA( desde a primeira entrega: custo por tarefa mínimo )
- **Implicação arquitetural:** ledger de custos( eventos de custo por unidade de trabalho ),agregação por tarefa/sessão/objetivo,orçamentos com alertas e interrupção( ver Autonomy/K ),relatórios de custo( Economic Engine )


---

# I. Evolution

##I1. Avaliação e benchmarking

- **Descrição:** medir sistematicamente o desempenho dos agentes( e dos modelos/providers ) em tarefas representativas, com métricas claras( conclusão, qualidade, custo, passos, latência ) e datasets de referência
- **Por que existe:** sem medição,não há como saber se mudanças melhoram ou pioram o sistema;é a base do aprendizado e da evolução controlada( North Star: ampliar capacidade )


- **Referências:** Arena.ai opera leaderboards de agentes baseados em sinais reais de uso( OBSERVADO  blog methodology );benchmarks de engenharia( SWE-bench, SWT-bench ) são usados para avaliar agentes de código( OBSERVADO  OpenHands docs )
- **Evidência observável:** leaderboard dinâmico e metodologia de avaliação documentados na Arena.ai( OBSERVADO );benchmarks públicos citados pelo OpenHands( OBSERVADO )
- **Limitações:** benchmarks podem não refletir tarefas reais e específicas da NEXORA;avaliação manual é cara e não escala( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  benchmark interno com datasets próprios( tarefas reais da NEXORA, pós-MVP ) + referência a benchmarks públicos;métricas unificadas( conclusão, qualidade, custo, passos )
- **Dependências:** runner de avaliação,sandbox,coleta de métricas,memória( armazenar resultados )
- **Risco:** médio  métricas mal definidas levam a otimizar a coisa errada( Goodhart );benchmark desatualizado engana(( INFERIDO )
- **Prioridade:** MÉDIA-ALTA( inicial:métricas de MVP;full benchmarking após Fase 1 )
- **Implicação arquitetural:** runner de avaliação( executa tarefas de teste e coleta métricas ),definição de métricas por tipo de tarefa,armazenamento de resultados( para comparar regressões ),integração com Evolution(I2I5)


##I2. Experimentação( experiments )

- **Descrição:** executar variações controladas( prompts, modelos, ferramentas, políticas, estratégias ) lado a lado( A/B ) e decidir por dados qual configurar fica melhor
- **Por que existe:** a evolução deve ser guiada por evidência, não por opinião;experimentação controlada evita regressões e acelera melhoria

- **Referências:** prática de A/B testing e experimentação é padrão em produtos de IA( OBSERVADO  prática comum;implícita em leaderboards e avaliação );auto-evolução de agentes é tema emergente( INFERIDO  literatura de agentes auto-melhorantes )
- **Evidência observável:** cultura de experimentação com medição é amplamente documentada em produtos de IA( OBSERVADO )
- **Limitações:** experimentação sem isolamento correto contamina resultados;custo de experimentação precisa ser governado( INFERIDO )
- **Classificação NEXORA:** SUPERAR  plataforma de experimentação integrada( comparar configs e reter o melhor com rollback automático ),com custo de experimento rastreado e gates de promoção( candidate → validated → production )
- **Dependências:** benchmarking, observabilidade, memória de decisões, política de promoção/rollback
- **Risco:** médio  experimentos mal controlados degradam produção( usa-se sham gate )
- **Prioridade:** MÉDIA( pós-MVP )
- **Implicação arquitetural:** runner de experimentos com isolamento por experimento,registro de configuração( experimento=config completa versionada ),comparação por métricas,política de promoção com reversão automática


##I3. Melhoria de prompts, contexto e estratégias

- **Descrição:** iterar sobre prompts, templates de contexto e estratégias de agente( como planejar, quando verificar, como recuperar ) com base em resultados medidos, e persistir as versões que funcionam
- **Por que existe:** prompts e estratégias são o "software" do agente;melhorá-los é evolir sem reescrever código
- **Referências:** melhoria contínua de prompts é prática comum em sistemas de agentes( OBSERVADO  prática de engenharia de prompt;iteração sobre estratégias documentada em методиках de agente )( INFERIDO em parte )
- **Evidência observável:** versionamento e iteração de prompts são prática difundida( OBSERVADO )
- **Limitações:** prompts otimizados para um benchmark podem overfit( perder generalização ) INFERIDO
- **Classificação NEXORA:** ADAPTAR  prompts/contexto/estratégias como artefatos versionados( tratados como código ),melhorados via experimentação e promovidos com gate( same pipeline de I2 ))
- **Dependências:** benchmarking, experimentação, memória de estratégias( procedural ),registro de versões
- **Risco:** baixo-médio  overfit em benchmark e perda de robustez sem validação diversa
- **Prioridade:** MÉDIA( pós-MVP )
- **Implicação arquitetural:** registry de prompts/estratégias versionado,integração com runner de experimentos,validação em datasets diversos antes de promoção


##I4. Melhoria de ferramentas e criação de novas ferramentas

- **Descrição:** identificar lacunas nas ferramentas existentes,projetar/criar novas ferramentas( ou melhorar as existentes ),testá-las e registrá-las para uso do agente
- **Por que existe:** ferramentas são o vocabulário de ação do agente;mais e melhores ferramentas = mais capacidades( auto-expansão da North Star )
- **Referências:** agentes modernos têm tool registries extensíveis e criação de skills/tools documentada( OBSERVADO  OpenHands skills/tools, Claude Code skills );tool creation por agentes é área emergente( INFERIDO  auto-evolução )
- **Evidência observável:** sistemas de skills e ferramentas extensíveis documentados nas plataformas( OBSERVADO  docs de skills/tools )
- **Limitações:** ferramentas novas precisam de testes,segurança( review de código ) e documentação;ferramenta ruim ativa é risco( INFERIDO )
- **Classificação NEXORA:** SUPERAR  pipeline de criação de ferramentas com revisão de segurança obrigatória,testes e registro versionado( ver M Self-expansion )
- **Dependências:** tool registry, sandbox para testes,verificação,política de revisão de código/segurança,memória
- **Risco:** médio-alto  ferramenta maliciosa/defeituosa ativada é vetor de ataque( exigir review antes de ativar )
- **Prioridade:** MÉDIA( pós-MVP;forte candidato a CRIAR/Self-expansion )
- **Implicação arquitetural:** tool factory( helper para criar ferramentas seguindo schema ),gates de revisão( código+segurança ) antes de registro,testes por ferramenta,versionamento


##I5. Evolução arquitetural controlada e rollback

- **Descrição:** evoluir o próprio sistema( componentes, política, configurações ) de forma controlada,com versionamento,testes de regressão e rollback seguro quando algo regride
- **Por que existe:** evolução sem controle destrói um sistema funcional;a regressão é o preço de mudanças não testadas( e o que impede inovação segura )
- **Referências:** boas práticas de CI/CD com testes de regressão e rollback são padrão em engenharia( OBSERVADO  prática de engenharia );auto-evolução de agentes é tema emergente e arriscado( INFERIDO )
- **Evidência observável:** sistemas de produção sérios usam canary/release/rollback( OBSERVADO  prática comum )
- **Limitações:** rollback sem estado compatível não funciona( mudanças de schema exigem migração/rollback de dados ) INFERERIDO

- **Classificação NEXORA:** ADAPTAR  evolução como releases versionados( configs, prompts, ferramentas, estratégias ),com testes de regressão automáticos,canary e rollback,governada por gates humanos para mudanças estruturais( ver regra: grandes alterações exigem aprovação )
- **Dependências:** benchmarking(I1),experimentação(I2),CI/tests,armazenamento versionado,política de aprovação
- **Risco:** alto  auto-evolução sem gates é perigosa( agentes reescrevendo a si mesmos sem controle )=exigir aprovação humana para mudanças de arquitetura
- **Prioridade:** MÉDIA-ALTA( governança desde cedo;automação plena depois )
- **Implicação arquitetural:** pipeline de release versionado para todos os artefatos do agente,testes de regressão obrigatórios,capacidade de rollback por componente( e por estado/dados ),gates humanos para mudanças estruturais( ver Self-expansion/M )


---

# J. Autonomy

##J1. Objetivos e planejamento contínuo

- **Descrição:** operar sobre objetivos de longo prazo,planejando continuamente( revisando e estendendo o plano à medida que o mundo muda ),em vez de apenas responder a prompts pontuais
- **Por que existe:** autonomia real é dirigida por objetivos persistentes,não por cada prompt individual( North Star: operação contínua )
- **Referências:** pesquisa contínua e agentes de monitoramento são padrão emergente de automação( INFERIDO  a partir de automações de monitoramento e cron jobs );roadmap da NEXORA prevê e Long-Term Autonomy( e contínua operação PROPOSTA basada no roadmap do usuário )
- **Evidência observável:** automações scheduladas e monitoramento são comuns no ecossistema OpenHands( OBSERVADO  GitHub Actions, crons de automação )
- **Limitações:** objetivos contínuos sem orçamento claro podem rodar para sempre( custo );sem parada elegante,a operação contínua vira sangria( INFERIDO )
- **Classificação NEXORA:** CRIAR  o modo autônomo da NEXORA( objetivos persistentes,replanejamento periódico,iteração em lote ) com orçamento e política de parada/retomada explícita( ver J5/J6/K )
- **Dependências:** planejamento,memória de longo prazo,observabilidade,scheduler,política de orçamento/interrupção
- **Risco:** alto  autonomia sem freio é o maior risco de custo e de ação indesejada( ver K )
- **Prioridade:** ALTA( para evolução;o MVP pode ser dirigido a tarefas )
- **Implicação arquitetural:** modo autonomia com ciclo planejar→executar→observar→replanejar em lote( não em tempo real ),política de interrupção,checkpoints por ciclo,limites de orçamento por objetivo


##J2. Observação e monitoramento( watch )

- **Descrição:** monitorar fontes e estados( web, mercados, repositórios, sistemas, resultados de tarefas ) ao longo do tempo,detectando mudanças relevantes e acionando ações( notificação, nova tarefa, replanejamento )
- **Por que existe:** oportunidades e problemas aparecem com o tempo;monitoramento é o que conecta o agente ao mundo real( North Star: identificar oportunidades )
- **Referências:** automações de monitoramento( poll de repositórios, canais, issues ) são comuns( OBSERVADO  ex:GitHub repo monitor, Slack channel monitor no ecossistema OpenHands );pesquisa contínua( ver D4 )
- **Evidência observável:** ferramentas de monitoramento agendado são amplamente usadas no ecossistema( OBSERVADO )
- **Limitações:** monitoramento amplo demais gera ruído e custo;detecção relevante exige filtros de qualidade( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  monitoramento por política de escopo( fontes autorizadas,frequência,limiar de relevância ),com custo rastreado e deduplicação( memória )
- **Dependências:** pesquisa(D4),memória( visto antes? ),scheduler,política de custo,notificação
- **Risco:** médio  volume de monitoramento sem filtro vira custo e ruído;monitoramento de fontes sensíveis exige autorização( ver K )
- **Prioridade:** MÉDIA( pós-MVP )
- **Implicação arquitetural:** serviço de monitoramento com agenda,deduplicação por memória,limiares de relevância,integração com notificações e com o planejador( mudança detectada → replaneja? )


##J3. Limites de autonomia e interrupção( human-on/off-loop )

- **Descrição:** definir limites explícitos de autonomia( por ação,por categoria,por orçamento,por escopo ) e pontos obrigatórios de interrupção/human approval( aprovação humana para ações de alto impacto )
- **Por que existe:** é o que torna a autonomia segura e alinhada ao criador( princípio de alinhamento da North Star;sem limites,autonomia é perigo )
- **Referências:** approval gates e human approval para ações de alto impacto são recomendação central de segurança de agentes( OBSERVADO  guias de segurança NVIDIA, TowardsAI, Huntress )
- **Evidência observável:** "Require user approval for every instance of specific actions";"Require approval for high-impact operations"( OBSERVADO  guias de segurança )
- **Limitações:** pedir aprovação demais anula a autonomia;pedir de menos assume risco; níveis de autonomia devem ser configuráveis por objetivo( INFERIDO )
- **Classificação NEXORA:** SUPERAR  níveis de autonomia por objetivo/domínio( delegado → supervisionado → aprovado-por-ação ),com política padrão default-deny para ações sensíveis( ver K )
- **Dependências:** política de permissões(K),execução controlada,sistema de notificação/approval( interface ),registro de decisões
- **Risco:** alto  autonomia excessiva sem gates é risco de dano irreversível( ver K/Security )
- **Prioridade:** CRÍTICA( desde a primeira entrega,mesmo que simples )
- **Implicação arquitetural:** níveis de autonomia por objetivo( configurados no objetivo estruturado ),gates de aprovação por categoria de ação,filas de aprovação humana com timeout e política de negação/abortamento


##J4. Alocação de recursos e priorização

- **Descrição:** decidir onde gastar recursos( orçamento de custo,tempo,concorrência ) entre objetivos,tarefas e agentes,com priorização explícita( p0/p1/p2, ROI esperado, urgência )
- **Por que existe:** recursos são finitos;priorização é o que garante que os recursos vão para o que mais importa( North Star: gerar recursos e reinvestir  eficiência é central )
- **Referências:** orçamentação e priorização são práticas de governança de agentes( INFERIDO  derivado de práticas de governança e gestão de recursos;sistemas de queue/prioridade são padrão em orquestração( OBSERVADO  filas de execução em upstream )
- **Evidência observável:** schedulers usam prioridades e dead ± lines em sistemas orquestrados( OBSERVADO  literatura de orchestration/scheduling )
- **Limitações:** priorização sem dados distorcida;sem política global,miguel objetivo dominante pode consumir tudo( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  alocação por política( orçamento por objetivo,prioridades,pesos ) com revisão periódica( e escalonamento humano para trade-offs de alto impacto )
- **Dependências:** cost tracking(H7),scheduler(F3),objetivos estruturados(J1),observabilidade
- **Risco:** médio  má priorização aloca recursos ao que não importa( desperdício de custo )
- **Prioridade:** MÉDIA-ALTA( pós-MVP )
- **Implicação arquitetural:** camada de alocação de recursos por objetivo/sessão( quotas },mecanismo de priorização( filas com peso ),revisão periódica de prioridades,escalonamento humano para conflitos de recursos de alto impacto


##J5. Aprendizagem durante a operação( learning in-the-loop )

- **Descrição:** extrair lições das execuções( sucessos,falhas,decisões ) durante a operação normal e incorporá-las a memória e a estratégias( sem exigir intervenção manual )
- **Por que existe:** é o que fecha o ciclo "aprender → melhorar → mais valor"( North Star: aprender continuamente );sem isso,a experiência se perde ao fim de cada tarefa
- **Referências:** Devin afirma "learn over time,and fix mistakes"( OBSERVADO  superfície );sistemas de memória episódica/procedural existem para isso( OBSERVADO  literatura de memória )
- **Evidência observável:** memória episódica( eventos e outcomes ) é projetada para alimentar aprendizado( OBSERVADO  literatura )
- **Limitações:** aprendizado sem revisão pode consolidar erros( viés de confirmação );lições precoces podem ser imaturas( carimbar validade e revisar ) INFERIDO
- **Classificação NEXORA:** SUPERAR  aprendizado em-loop com consolidação periódica( retrospectivas ),validade carimbada( quando válida ),revisão e poda( evitar lixo acumulado ),integrado a E4( experience memory )
- **Dependências:** memória(E4),verificação de resultados,observabilidade,revisão periódica( reflexão )
- **Risco:** médio  aprendizado não revisado envenena decisões futuras( mais perigoso que não aprender )
- **Prioridade:** MÉDIA-ALTA( pós-MVP )
- **Implicação arquitetural:** ciclo de reflexão periódico( por tarefa/sessão ),consolidação de lições com validade e fonte,revisão de lições consolidadas( poda/atualização ),gatilhos de recuperação em decisões futuras( ver E4 )


##J6. Loops de longo prazo e retomada( long-running )

- **Descrição:** operar tarefas que duram horas/dias( execução em lote, persistência de estado, retomada após interrupção(crash,manutenção (sem perder progresso )
- **Por que existe:** a visão da NEXORA( e o Estágio Long-Term Autonomy do roadmap ) exige operação contínua além de uma sessão;e o mundo real não cabe num único prompt

- **Referências:** agentes de produção rodam por horas em sessões persistentes( OBSERVADO  Devin opera em sessões com workspace persistente;OpenHands cloud runs );automações scheduladas rodam continuamente( OBSERVADO  ecossistema OpenHands )
- **Evidência observável:** workspaces persistentes e execuções remotas são padrão em agentes de código( OBSERVADO )
- **Limitações:** execução longa sem checkpoints perde tudo em crash;retomada sem estado consistente corrompe( INFERIDO  derivado de práticas de sistemas distribuídos )
- **Classificação NEXORA:** ADAPTAR  execução em lote com checkpoints periódicos( estado + plano + custo ),retomada idempotente,e observabilidade para acompanhamento remoto
- **Dependências:** estado/event store(A6),checkpoints,scheduler( cron ),observabilidade,política de interrupção/retomada

- **Risco:** médio  long-running sem persistência perde trabalho;operações contínuas sem orçamento sangram custo( ver J3/J4/K )
- **Prioridade:** MÉDIA-ALTA( pós-MVP )
- **Implicação arquitetural:** execução em lote com checkpoint por etapa,estado recuperável( replay ),retomada idempotente,policy de orçamento por lote,e heartbeat/monitoramento( ver K Auditoria )


---

# K. Security / Governance

##K1. Autorização e permissões( políticas )

- **Descrição:** controlar o que o agente pode fazer( leitura, escrita, execução, rede, delegação ) por política explícita( por agente,tarefa,objetivo,domínio ),com princípio de menor privilégio
- **Por que existe:** é a fundação da execução controlada( requisito explícito da visão da NEXORA );sem permissões,qualquer ação é possível e qualquer erro é dano
- **Referências:** least privilege é princípio central de segurança de agentes( OBSERVADO  guias de segurança NVIDIA, Huntress, TowardsAI );"AI agents should be treated as distinct non-human identities with defined owners, scoped permissions"( OBSERVADO )
- **Evidência observável:** prescrições de escopo de permissões e default-deny são amplamente documentadas( OBSERVADO )
- **Limitações:** permissões estáticas ficam desatualizadas;permissões amplas demais anulam a proteção( INFERIDO )
- **Classificação NEXORA:** REPLICAR  políticas de permissão por agente/tarefa/ferramenta,default-deny,revisão periódica de permissões( least privilege )
- **Dependências:** schema de política,tool registry( anotação de risco por ferramenta ),execução controlada,auditoria
- **Risco:** crítico  permissões frouxas são o vetor primário de dano( ações indesejadas,vazamento )
- **Prioridade:** CRÍTICA( desde a primeira entrega )
- **Implicação arquitetural:** camada de autorização avaliada a cada ação de ferramenta( policy decision point separado da execução  control plane vs execution plane ),políticas como código declarativo( auditável,testável ),anotação de risco/permissão por ferramenta


##K2. Sandbox e isolamento

- **Descrição:** executar ações( código, terminal, browser, rede ) em ambientes isolados( container, bubblewrap, permissions ) com default-deny de acesso externo e limites de recursos
- **Por que existe:** é a contenção física do dano possível;mesmo que a política falhe,o sandbox limita o estrago( defesa em profundidade )
- **Referências:** Devin roda em "sandboxed compute environment"( OBSERVADO );guia NVIDIA prescreve default-deny,allowlists e lifecycle management( OBSERVADO );guia TowardsAI: "if the model can influence the operation directly,assume the operation is untrusted"( OBSERVADO )
- **Evidência observável:** sandboxing documentado como prática obrigatória para agentes autônomos que executam código( OBSERVADO )
- **Limitações:** sandbox imperfeito( escapes ) existe;isolar demais impede trabalho legítimo( equilíbrio necessário ) INFERIDO

- **Classificação NEXORA:** REPLICAR  sandbox por execução com isolamento de rede/filesystem/processos,quotas de recurso e lifecycle management( alinhado a C3/Processos )
- **Dependências:** runtime de sandbox,política de rede,gerenciamento de processos,observabilidade
- **Risco:** crítico  sem sandbox,execução de código arbitrário expõe o host e segredos

- **Prioridade:** CRÍTICA( para qualquer execução não trivial )
- **Implicação arquitetural:** runtime de execução isolado( por tarefa/sessão ),allow/deny de rede e filesystem,quotas de CPU/RAM/disco/tempo,limpeza( kill/destruir ) ao fim,tudo auditado


##K3. Segredos e dados sensíveis

- **Descrição:** gerenciar segredos( chaves de API,tokens,credentials ) com injeção seletiva( não expor ao agente ),broker de credenciais( tokens curtos,escopados,auditáveis ),e sanitização em logs
- **Por que existe:** segredo exposto = capacidade de dano em outras contas/sistemas;e logs com segredos são uma das maiores vazamentos reais( ver boas práticas )
- **Referências:** guia NVIDIA: "Use a secret injection approach to prevent secrets from being shared with the agent";guia TowardsAI: "issue short-lived,scoped,auditable tokens through a broker"( OBSERVADO );guia AYAutomate:"Sanitize secrets from structured logs"( OBSERVADO )
- **Evidência observável:** práticas de credential broker,short-lived tokens e sanitização de logs são prescritas em guias de segurança de agentes( OBSERVADO )
- **Limitações:** injeção seletiva de segredos é complexa;sem broker,segredos de longo prazo vazam no contexto do agente( INFERIDO )
- **Classificação NEXORA:** REPLICAR  broker de credenciais com tokens curtos e escopados,injeção por tarefa,zero segredos no contexto/logs( sanitização automática )
- **Dependências:** cofre de segredos,broker/emissor de tokens,política de escopo por tarefa,sanitização de logs/observações
- **Risco:** crítico  vazamento de segredo é irreversível e compromete tudo( contas,serviços,dados )
- **Prioridade:** CRÍTICA( desde a primeira entrega: nenhum segredo hardcoded,nenhum segredo em logs )
- **Implicação arquitetural:** serviço de segredos fora do alcance do agente( control plane ),emitindo tokens curtos sob demanda,sanitização em toda captura de observação/log,auditoria de acesso a segredos


##K4. Audit trail e observabilidade de segurança

- **Descrição:** registrar tudo( ações,decisões,acessos,autorizações,negações,erros ) em trilha imutável e auditável,com quem/o quê/quando/por quê
- **Por que existe:** auditoria é o que permite investigar incidentes,responsabilizar decisões e melhorar políticas( sem registro,não há governança )
- **Referências:** audit trails são prescritas em segurança de agentes( OBSERVADO  Huntress:"defined owners,scoped permissions,and audit trails" );agente-server e sistemas de agentes registram eventos por padrão( OBSERVADO  OpenHands event-sourced; arquiteturas de orquestração incluem observability )
- **Evidência observável:** prescrição de audit trails para agentes como identidades não humanas( OBSERVADO )
- **Limitações:** auditar tudo sem índice é inutilizável;logs envenenados por segredos viram passivo( sanitização obrigatória ver K3 )
- **Classificação NEXORA:** REPLICAR  trilha de eventos imutável e indexada( quem,o quê,quando,por quê,resultado ),com sanitização de segredos e retenção por política
- **Dependências:** event store,observabilidade,sanitização,política de retenção,ferramentas de consulta
- **Risco:** médio-alto  trilha ausente ou ilegível impede investigação/recuperação( e enfraquece toda governança )
- **Prioridade:** CRÍTICA( desde a primeira entrega: eventos de ação/decisão/autorização )
- **Implicação arquitetural:** todo evento de ação/decisão/autorização/fluxo registrado em event store indexado,imutável e com retenção;consulta de trilha para auditoria;integração com memória( lições de incidentes )


##K5. Checkpoints,reversibilidade e rollback

- **Descrição:** permitir desfazer ações( edições,execuções,estado,configurações ) via checkpoints periódicos,undo/diff e rollback por componente( com integridade de dados )
- **Por que existe:** erro é inevitável;capacidade de reverter é o que transforma erro em incidente controlado em vez de catástrofe( e permite experimentação segura  ver I )
- **Referências:** checkpoints e restore são práticas de sistemas de segurança e experimentação( OBSERVADO  prática de engenharia );reversibilidade é requisito implícito de gobernanza( INFERIDO  derivado de práticas de rollout/rollback )
- **Evidência observável:** padrões de checkpoint/rollback em sistemas distribuídos e CI/CD( OBSERVADO  prática comum )
- **Limitações:** rollback sem migração de dados não funciona( versões de schema );checkpoint caro demais é inutilizável( custo de armazenamento )( INFERIDO )
- **Classificação NEXORA:** ADAPTAR  checkpoints por etapa( estado + plano + artefatos ),undo por edição( diff ),rollback por componente com integridade de dados( e política de retenção de checkpoints )
- **Dependências:** event store/estado(A6),diff/versionamento de artefatos,política de retenção,custos(H7)
- **Risco:** médio-alto  irreversibilidade transforma erro pequeno em perda grande;rollback quebrado corrompe estado( testar rollback também! )
- **Prioridade:** ALTA( checkpoints desde o MVP;rollback completo pós-MVP )
- **Implicação arquitetural:** serviço de checkpoints por etapa( snapshot ou reexecução por eventos ),undo por edição,capacidade de rollback por componente,testes periódicos de restauração( recovery drills )


##K6. Ações sensíveis e aprovação humana

- **Descrição:** categorizar ações por sensibilidade( e impacto ) e exigir aprovação humana( ou segundo política ) para ações sensíveis( finanças,exfiltração,produção,delegação externa,destruição )
- **Por que existe:** algumas ações são irreversíveis ou de alto impacto;aprovação humana é o controle final de alinhamento ao criador( North Star )
- **Referências:** approval gates para high-impact operations são prescritas( OBSERVADO  guias NVIDIA,TowardsAI,Huntress );"agent commits are automatic,pushes require a human"( OBSERVADO  AYAutomate )
- **Evidência observável:** política de exigir aprovação para operações de alto impacto é amplamente recomendada( OBSERVADO )
- **Limitações:** aprovação sem informação suficiente é caixa-preta( mostrar contexto,risco,diff );filas de aprovação lentas travam autonomia( timeouts e escalonamento ) INFERERIDO
- **Classificação NEXORA:** REPLICAR  categorias de sensibilidade por ação,filas de aprovação humanas com contexto( o quê,risco,alternativas ),timeout e política de negação/abortamento( integrado a J3 )
- **Dependências:** política de autorização(K1),classificação de ações por sensibilidade,interface de aprovação( notificação ),observabilidade
- **Risco:** crítico se ausente  ação irreversível sem aprovação é o pior cenário de governança
- **Prioridade:** CRÍTICA( desde a primeira entrega )
- **Implicação arquitetural:** taxonomia de sensibilidade por categoria de ferramenta/ação,gate de aprovação antes da execução,interface humana com contexto de decisão,timeouts e registro de decisões( aprovado/negado )


##K7. Operação segura( segurança operacional )

- **Descrição:** gerenciar riscos operacionais contínuos( rate limits,indisponibilidade de providers,anomalias de custo,comportamento inesperado de agente ) com circuit breakers,ertentes e desligamento de emergência( kill switch )
- **Por que existe:** sistemas autônomos precisam de freios operacionais além de permissões;e anomalias precisam de resposta antes de virarem incidente
- **Referências:** circuit breakers e cooldowns são padrão em resiliência( OBSERVADO  LiteLLM,práticas de sistemas );kill switch é prática de segurança de automação( INFERIDO  derivado de segurança operacional )
- **Evidência observável:** mecanismos de circuito e cooldown documentados em roteadores( OBSERVADO )
- **Limitações:** kill switch central demais interrompe tudo( escopos de desligamento );alertas sem triagem geram fadiga( limiares e escalonamento ) INFERERIDO
- **Classificação NEXORA:** SUPERAR  painel de segurança operacional( métricas de anomalia,alertas com limiares,circuit breakers por componente,kill switch por escopo( agente,tarefa,global )) e desligamento seguro( com checkpoint e retomada )
- **Dependências:** observabilidade,cost tracking,sandbox,política de alertas,checkpoints( para desligamento seguro )
- **Risco:** alto  sem freios operacionais,anomalia pequena escala para incidente grande( custo,dano )
- **Prioridade:** MÉDIA-ALTA( circuit breakers e alertas de custo desde cedo;plano de emergência pós-MVP )
- **Implicação arquitetural:** monitor de anomalias( custo,erros,latência,comportamento ),circuit breakers por provider/ferramenta/agente,kill switches por escopo com shutdown gracioso( checkpoint + retomada ),escalonamento de alertas( humano )


##K8. Promt injection e conteúdo não confiável

- **Descrição:** tratar todo conteúdo externo( web,arquivos,emails,ferramentas de terceiros ) como não confiável,com camadas de contenção( escopo de ferramentas,isolamento,permissões ) e detecção/neutralização de ataques de injeção( instruções maliciosas )
- **Por que existe:** prompt injection é o vetor de ataque mais explorável de agentes( conteúdo externo tenta sequestrar o agente );e defesa em profundidade( permissões+sandbox+approval ) é a única proteção realista
- **Referências:** guias de segurança tratam prompt injection e restrição de rede como práticas centrais( OBSERVADO  NVIDIA: network isolation,TowardsAI: prompt injection embedded in many places;AYAutomate: camadas de contenção )
- **Evidência observável:** recomendações de isolamento de rede e default-deny para limitar impacto de injeção( OBSERVADO )
- **Limitações:** detecção automática de injeção é imperfeita( defesa principal é contenção,não detecção ) INFERERIDO;E-vazamento via tool outputs precisa sanitização( ver K3 )
- **Classificação NEXORA:** REPLICAR  conteúdo externo marcado como não confiável em todo pipeline( memória,contexto,ferramentas ),com defesa em profundidade( permissões,sandbox,approval ) e monitoramento de comportamento anômalo
- **Dependências:** K1/K2/K3/K6,Marcação de provenance( de onde veio o conteúdo ),sanitização
- **Risco:** crítico  injeção bem-sucedida pode exfiltrar dados,alterar arquivos ou violar políticas( com permissões frouxas )
- **Prioridade:** CRÍTICA( considerar em todo fluxo que toca conteúdo externo )
- **Implicação arquitetural:** taint( marcação ) de conteúdo não confiável por proveniência,políticas de escopo reforçadas para ações sobre conteúdo não confiável,monitoramento de padrões de injeção( comportamento anômalo ),revisão humana para efeitos colaterais de alto impacto


---

# L. Economic / Opportunity Intelligence

##L1. Identificação de oportunidades

- **Descrição:** detectar e avaliar oportunidades de criação de valor( gaps de mercado, problemas, demandas, tendências ) a partir de observação contínua,e priorizá-las por potencial( alinhamento com o criador, viabilidade, ROI esperado )
- **Por que existe:** é o motor da North Star( "identificar oportunidades" );sem isso,a NEXORA executa tarefas mas não cria valor proativamente
- **Referências:** capacidade não presente nas referências principais de agente( OBSERVADO  lacuna );práticas de análise de mercado e oportunidade são da engenharia de negócios( OBSERVADO  campos consolidados: market research, opportunity assessment )
- **Evidência observável:** nenhuma das plataformas referenciadas( Arena, OpenHands, Claude, Devin ) expõe identificação de oportunidades como capacidade( OBSERVADO  lacuna )
- **Limitações:** identificação sem validação gera ruído( muitas "oportunidades" falsas );oportunidade sem alinhamento com o criador pode desviar a NEXORA( INFERIDO )
- **Classificação NEXORA:** CRIAR  pipeline de identificação de oportunidades( observação → sinal → validação → priorização ) com critérios explícitos( alinhamento,viabilidade,ROI,risco ) e portfólio de oportunidades( ver L5 )
- **Dependências:** pesquisa/monitoramento(D4,J2),memória semântica,análise de mercado(L2),governança( alinhamento e aprovação  K6 )
- **Risco:** médio-alto  perseguir oportunidade não validada desperdiça recursos;desalinhamento com o criador é falha de governança( exigir aprovação para novos domínios )
- **Prioridade:** MÉDIA( pós-MVP;centro do estágio Market Intelligence do roadmap )
- **Implicação arquitetural:** motor de oportunidades com scorecard padronizado( alinhamento,viabilidade,ROI,risco,urência ),registro de oportunidades em memória( portfólio ),gates de aprovação para perseguir( ver L5/Gov )

##L2. Análise de mercado e concorrência

- **Descrição:** analisar mercados,concorrentes e alternativas( quem resolve o quê,preços,posicionamento,forças/fraquezas ) para embasar decisões de produto e posicionamento
- **Por que existe:** valor só se materializa se houver demanda e diferenciação;análise de mercado é o que conecta observação a decisão de produto( North Star: criar valor )
- **Referências:** capacidades de pesquisa e síntese( D1D3 ) são a matéria-prima( OBSERVADO  ver seção D );análise de concorrência é prática consolidada de negócios( OBSERVADO  campos de business intelligence )
- **Evidência observável:** NEXORA pode combinar pesquisa+síntese para produzir análises de mercado( PROPOSTA  compor capacidades D )
- **Limitações:** mercado muda rápido;análise estática desatualiza( exigir reanálise periódica  monitoramento );dados de mercado são incompletos por natureza( INFERIDO )
- **Classificação NEXORA:** CRIAR  serviço de análise de mercado( processos estruturados de análise de concorrência,preços,posicionamento ) alimentado por pesquisa contínua,com relatórios padronizados( ver L5/Product Engine )
- **Dependências:** pesquisa(D),síntese(D3),memória semântica,monitoramento(J2),governança( escopo )
- **Risco:** médio  análise desatualizada embasa decisão errada;nalise como insight sem fonte não é auditável( citação obrigatória  D2 ))
- **Prioridade:** MÉDIA( pós-MVP )
- **Implicação arquitetural:** templates de análise de mercado( concorrência,preços,posicionamento ),integração com pesquisa/monitoramento,registro de fontes( provenance ),revisão periódica por domínio


##L3. Produtos, precificação e distribuição( Product / Pricing / Distribution )

- **Descrição:** projetar, precificar e distribuir produtos/serviços/software gerados pela NEXORA( com estratégia de canais,marketing e vendas )
- **Por que existe:** a North Star exige transformar valor em recursos( legal e sustentável );produto,preço e distribuição são o mecanismo de captura de valor

- **Referências:** áreas de product management,pricing strategy,e distribution/sales são consolidadas na engenharia de negócios( OBSERVADO  campos estabelecidos );roadmap da NEXORA lista Product Engine,Pricing,Marketing,Sales/Distribution( PROPOSTA  do roadmap do usuário )
- **Evidência observável:** são domínios bem estudados de negócio( OBSERVADO  literatura de negócios );não são capacidades de agentes de propósito geral( OBSERVADO  lacuna nas referências de agente )
- **Limitações:** é uma área nova para agentes autônomos;pricing e distribuição têm componentes legais/contratuais( exigir supervisão humana ) INFERIDO
- **Classificação NEXORA:** CRIAR  engines de produto/preço/distribuição como módulos especializados( ver Economic Engine do roadmap ),com participação humana obrigatória em decisões legais/contratuais( K6/Aprovação )
- **Dependências:** análise de mercado(L2),oportunidades(L1),experimentação(I2,governança e aprovação(K6),custos(H7,para calcular margem )
- **Risco:** médio-alto  decisões comerciais sem supervisão humana( contratos,legal ) são risco de governança;precificação errada destrói sustentabilidade( ver Roadmap/Pricing )
- **Prioridade:** MÉDIA( pós-MVP;estágio Economic Engine )
- **Implicação arquitetural:** módulos especializados de produto/preço/distribuição com dados vindos de análise de mercado e custos, aprovação humana em decisões sensíveis,registro de decisões comerciais( memória+auditoria )


##L4. Analytics e experimentação de valor

- **Descrição:** medir o desempenho de produtos/canais( receita,custo,conversão,retenção ) e executar experimentos de negócio( testar preço,canal,mensagem,produto ) guiados por dados
- **Por que existe:** captura de valor é um processo empírico;medir e experimentar é o que melhora receita/custo ao longo do tempo( North Star: gerar recursos ))
- **Referências:** prática de growth analytics e experimentação de negócio é padrão em produtos digitais( OBSERVADO  campos consolidados );a NEXORA já terá infraestrutura de experimentação(I2) e benchmarking(I1)  composição natural( PROPOSTA )
- **Evidência observável:** métodos A/B e analytics de produto são amplamente consolidados( OBSERVADO  prática comum )
- **Limitações:** métricas de negócio demoram para acumular;sinal estatístico fraco em início( amostra pequena ) INFERIDO

- **Classificação NEXORA:** CRIAR  analytics de valor( receita,custo,margem,ROI por produto/canal ) integrado a experimentação e ao cost tracking( ver Economic Engine/Analytics do roadmap )
- **Dependências:** cost tracking(H7),experimentação(I2,análise de mercado(L2,coleta de métricas de negócio( integrações com canais ),governança
- **Risco:** médio  métricas de negócio imprecisas induzem decisão errada;privacidade de dados comerciais( ver K/Governança ))
- **Prioridade:** MÉDIA( pós-MVP )
- **Implicação arquitetural:** conjunto de métricas de negócio( receita,custo,margem,ROI ),pipeline de analytics( agregação de dados de canais ),reutilização da infraestrutura de experimentação(I2) e relatórios( integrados ao Painel/Gov )


##L5. Portfólio e reinvestimento

- **Descrição:** gerenciar um portfólio de oportunidades/produtos( priorizar,alocar recursos,matar/pausar ),e reinvestir recursos gerados( conforme política aprovada ) em capacidade( mais ferramentas,memória,benchmark,novos domínios ))
- **Por que existe:** a North Star exige transformar recursos em capacidade( "ampliar continuamente sua própria capacidade" );portfólio é o mecanismo de decidir onde reinvestir

- **Referências:** gestão de portfólio e alocação de capital são práticas consolidadas de negócios( OBSERVADO  campos de portfolio management );roadmap da NEXORA lista Portfolio e Reinvestimento autorizado( PROPOSTA  do roadmap do usuário )
- **Evidência observável:** é prática de gestão de recursos e capital( OBSERVADO  literatura de negócios );não é capacidade de agentes de propósito geral( OBSERVADO  lacuna )
- **Limitações:** reinvestir sem alinhamento com o criador é desvio de governança;alocação errada desperdiça recursos( políticas de portfólio obrigatórias ) INFERIDO
- **Classificação NEXORA:** CRIAR  portfólio de oportunidades/produtos com scorecard,alocação de recursos por política aprovada,reinvestimento em capacidade guiado por evidência( ROI medido ) e aprovação humana para grandes alocações
- **Dependências:** oportunidades(L1),custo(H7),analytics(L4,experimentação(I2,governança(K6/Aprovação ))
- **Risco:** alto  reinvestimento sem governança desvia os recursos do criador( viola o alinhamento da North Star );portfólio sem critérios acumula lixo( "zumbis" )
- **Prioridade:** MÉDIA-ALTA( governança de reinvestimento desde cedo;execução plena pós-MVP ))
- **Implicação arquitetural:** portfólio como memória estruturada( oportunidades/produtos com estado,ROI,decisões ),política de alocação/priorização( ver J4 ),gates de aprovação para grandes alocações,relatórios de ROI por investimento( integrado a K4/Auditoria )


---

# M. Self-expansion

##M1. Identificação de lacunas de capacidade

- **Descrição:** detectar capacidades ausentes ou insuficientes( durante execução,avaliação ou observação ),formulando a lacuna com clareza( o que falta,por que,impacto esperado ))
- **Por que existe:** a auto-expansão começa com consciência do que falta( mapear lacuna é o primeiro passo para criar capacidade  North Star: ampliar capacidade )
- **Referências:** auto-melhoria de agentes é tema emergente( INFERIDO  literatura de auto-evolução;ex:agentes que identificam necessidades e criam ferramentas )tool creation por agentes é direção ativa em pesquisas( INFERIDO  literatura de agentes auto-melhorantes )
- **Evidência observável:** pipelines de quality control( verificação,benchmarking ) são projetados para revelar lacunas( OBSERVADO  ver I1/I4;área emergente em pesquisa )
- **Limitações:** lacuna mal formulada gera solução errada;agente não deve "se diagnosticar" sem evidência e revisão humana( INFERIDO )
- **Classificação NEXORA:** CRIAR  processo de auto-diagnóstico( fonte:falhas,benchmarks,pedidos,observação ) com formulário padronizado de lacuna( evidência,impacto,solução candidata )
- **Dependências:** benchmarking(I1),verificação,memória( falhas,decisões ),observabilidade
- **Risco:** médio  auto-diagnóstico sem validação gera mudanças dispendiosas e inúteis( gates humanos obrigatórios ))
- **Prioridade:** MÉDIA( pós-MVP;área de pesquisa e diferenciação )
- **Implicação arquitetural:** pipeline de detecção de lacunas( gatilhos:falhas recorrentes,benchmark deficitário,demanda do criador ),tickets padronizados de lacuna( capacity gap ticket ),fila de revisão humana( antes de investir )


##M2. Pesquisa e avaliação de soluções

- **Descrição:** pesquisar( internamente e externamente ) como resolver a lacuna( ferramentas existentes,padrões,literatura,projetos open-source ),avaliar alternativas( custo,esforço,adequação,risco ) e recomendar uma abordagem

- **Por que existe:** nem toda lacuna exige construir do zero;pesquisar antes de construir evita retrabalho e má escolha( e respeita a regra de não reinventar a roda )
- **Referências:** capacidades de pesquisa e comparação( D1D3 ) são a matéria-prima( OBSERVADO  ver seção D );padrão "research before build" é prática de engenharia( OBSERVADO  prática comum ))
- **Evidência observável:** a NEXORA já terá pipeline de pesquisa para reutilizar( PROPOSTA  composição de D )
- **Limitações:** pesquisar demais atrasa( timebox );solução externa precisa de avaliação de segurança( código de terceiros  ver K ) INFERIDO

- **Classificação NEXORA:** ADAPTAR( composição de D + I2 )  usar o pipeline de pesquisa/experimentação para avaliar soluções candidatas com scorecard( custo,esforço,adequação,risco,manutenção )
- **Dependências:** pesquisa(D),experimentação(I2),benchmarking(I1),governança( aprovação ))
- **Risco:** médio  adotar solução externa sem revisão de segurança é vetor de ataque( revisão obrigatória )
- **Prioridade:** MÉDIA( pós-MVP ))
- **Implicação arquitetural:** reutilizar o pipeline de pesquisa/síntese para avaliar soluções,scorecard de adoção( build vs buy vs adapt ),revisão de segurança para dependências externas( ver B7/K )


##M3. Projetar, implementar e testar nova capacidade( com gates )

- **Descrição:** projetar e implementar a nova capacidade( ferramenta,skill,agente,política,estratégia,componente ),com testes e validação antes de ativar,e revisão humana obrigatória( especialmente para código,segurança e arquitetura ))
- **Por que existe:** é a execução da auto-expansão;mas sem gates,a auto-expansão vira auto-modificação descontrolada( risco crítico de governança ))
- **Referências:** pipelines de desenvolvimento( projetar→implementar→testar→revisar→promover ) são prática padrão de engenharia( OBSERVADO  ver I2/I5 );tool creation por agentes com validação é direção de pesquisa( INFERIDO  auto-evolução ))
- **Evidência observável:** o próprio pipeline de desenvolvimento de software( testes,review,CI ) é a referência( OBSERVADO  prática de engenharia ))
- **Limitações:** auto-implementação sem revisão humana de código é risco crítico( segurança,arquitetura );gatilhos de modificação precisam ser restritos( política explícita ) INFERIDO
- **Classificação NEXORA:** ADAPTAR( gates humanos obrigatórios )  a NEXORA pode *propor* e até *implementar* mudanças em sandbox,mas *ativação* exige revisão humana( exceto mudanças triviais explicitamente delegadas ))
- **Dependências:** ferramentas de desenvolvimento( B ),testes/verificação,experimentação(I2,governança(K1/K6,memória( registro ))
- **Risco:** crítico  auto-modificação sem gates pode corromper ou sequestrar o próprio sistema( o controle mais importante de toda a plataforma ))
- **Prioridade:** MÉDIA-ALTA( definir a política de gates desde cedo;execução pós-MVP ))
- **Implicação arquitetural:** pipeline de auto-expansão com ambiente de desenvolvimento isolado( sandbox ),testes obrigatórios,gates de revisão humana para ativação,rollback de capacidade( ver I5/K5 ),registro de toda alteração( auditoria )


##M4. Validação e incorporação( registrar )

- **Descrição:** validar a nova capacidade em condições reais( em staging,incremental,com métricas ),registrá-la( versão,capacidade,custo,uso,autoria)e incorporá-la ao sistema( registry,memória,documentação ))
- **Por que existe:** capacidade não validada nem registrada não é capacidade( é experimento abandonado );registro é o que torna a expansão auditável e reutilizável

- **Referências:** padrões de promover mudanças( validated→production ) e registry de componentes são práticas de engenharia e orquestração( OBSERVADO  ver I2, registries de tools/agentes ))
- **Evidência observável:** sistemas de skills/tools/agent registries documentados( OBSERVADO  OpenHands,Claude Code skills ))
- **Limitações:** validação insuficiente ativa capacidade imatura;registro incompleto gera componente órfão( sem dono,sem métricas ) INFERIDO

- **Classificação NEXORA:** ADAPTAR  promoção por estágios( candidate→validated→production ),registro completo( capacidade,versão,autoria,custo,uso ),integração com memória e observabilidade
- **Dependências:** benchmarking(I1,experimentação(I2,registries( tools,agentes,providers ),memória,documentação
- **Risco:** médio  ativação de capacidade não validada degrada produção( gates de estágio obrigatórios ))
- **Prioridade:** MÉDIA( pós-MVP ))
- **Implicação arquitetural:** ciclo de vida de capacidade( proposed→candidate→validated→production→retired ),registro central por capacidade( versão,custo,uso,autoria,validade ),integração com memória e com relatórios( I1/K4 )


---

# Z. Referências utilizadas ( pesquisa )

> Fontes públicas consultadas durante esta Capability Discovery. A maioria das referências é documentação oficial ou literatura técnica

1. **Arena.ai  Agent Mode**( blog oficial, jun 2026 ): https://arena.ai/blog/agent-mode
2. **Arena.ai  Agent Arena methodology**( blog oficial ): https://arena.ai/blog/agent-arena-methodology
3. **Arena.ai  Agent Leaderboard**: https://arena.ai/leaderboard/agent
4. **OpenHands Software Agent SDK  Docs e arXiv**( arquitetura, tool system, context compression, model-agnostic ): https://docs.openhands.dev/sdk  https://arxiv.org/html/2511.03690v2
5. **Anthropic  Computer use tool / Claude Agent SDK**( docs ): https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool  https://www.aiagentshub.net/blog/claude-agent-sdk-guide
6. **Anthropic  Advanced tool use**( tool search ): https://www.anthropic.com/engineering/advanced-tool-use
7. **Cognition  Introducing Devin**( blog oficial ): https://cognition.com/blog/introducing-devin
8. **Cognition  Devin Security Swarm**( PR oficial ): https://www.prnewswire.com/news-releases/cognition-launches-devin-security-swarm-to-tackle-the-vulnerability-backlog-302814800.html
9. **Fast.io  Devin architecture, sandboxes**: https://fast.io/resources/devin-software-engineer
10. **Survey de memória de agentes**( episodic, semantic, procedural; hot/warm/cold tiering ): https://atlan.com/know/long-term-vs-short-term-ai-memory  https://machinelearningmastery.com/beyond-short-term-memory-the-3-types-of-long-term-memory-ai-agents-need
11. **Memória de agentes**( MongoDB, Redis, Moxo ):https://www.mongodb.com/resources/basics/artificial-intelligence/agent-memory  https://redis.io/blog/build-smarter-ai-agents-manage-short-term-and-long-term-memory-with-redis  https://www.moxo.com/blog/agentic-ai-memory
12. **Multi-agent orchestration**( arxiv, Microsoft MARI, TrueFoundry ): https://arxiv.org/html/2601.13671v1  https://microsoft.github.io/multi-agent-reference-architecture/docs/reference-architecture/Reference-Architecture.html
13. **Guia de segurança para sandboxing de agentes**( NVIDIA ): https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk
14. **Sandbox architecture para agentes de produção**( TowardsAI ): https://pub.towardsai.net/ai-agent-sandbox-architecture-how-to-let-agents-run-code-without-letting-them-run-everything-63a9293c35fb

15. **AI Agent Security Best Practices**( AYAutomate ): https://www.ayautomate.com/blog/ai-agent-security-best-practices
16. **LLM routers e model routing**( Zylos, MindStudio, Braintrust, OpenRouter, TrueFoundry; kenhuangus substack ): https://zylos.ai/research/2026-03-02-ai-agent-model-routing  https://www.mindstudio.ai/blog/set-up-ai-model-router-llm-stack-c2610  https://www.braintrust.dev/articles/best-llm-routers-2026  https://kenhuangus.substack.com/p/chapter-14-model-routing-and-provider
17. **Task planning com DAG e replanning**( arxiv, MDPI, Laxaar, EmergentMind ): https://arxiv.org/html/2604.11378v1  https://www.mdpi.com/2076-3417/16/8/3851  https://laxaar.com/blog/agent-planning-techniques-1748650000006  https://www.emergentmind.com/topics/dag-based-task-planner
