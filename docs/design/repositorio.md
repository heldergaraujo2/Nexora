# Design Proposto — Estrutura do Repositorio da NEXORA

> **Proposta,nao implementacao.** Este documento descreve a estrutura final sugerida(a ser construida na Fase te 1,Fundacao,apos aprovacao explicita). Nenhum codigo de producao foi criado nesta fase( conforme comando da Fase te 0.5.,

## 1. Visao Geral do Repositorio

```
nexora/
|— src/nexora/                 ( codigo de producao:modulos internos(
|   |— __init__.py
|   |— __main__.py             ( ponto de entrada CLI: python -m nexora (
|   |— cli.py                   ( definicao da CLI primaria,subcomandos( ver ADR-003 (
|   |— config/
|   |   |— __init__.py
|   |   |— loaders.py            ( leitura TOML/YAML+env,validacao via pydantic (
|   |   |— schema.py
|   |   |— permissions.py        ( carregamento das politicas de autorizacao( ADR-009 (
|   |— core/
|   |   |— __init__.py
|   |   |— agente
|   |   |   |— __init__.py
|   |   |   |— ciclo.py          ( loop objetivo->plano->execucao->verificacao->memoria (
|   |   |   |— estado.py
|   |   |— plano/
|   |   |   |— __init__.py
|   |   |   |— dag.py            ( DAG de subtarefas,validacao aciclica (
|   |   |   |— executor.py
|   |   |— objetivo.py            ( parser/normalizacao de objetivo( ver contrato objetivo ( 
|   |— providers/
|   |   |— __init__.py
|   |   |— base.py              ( interface Provider( generate,stream,tools,capabilities,erros(( ADR-006 (
|   |   |— registry.py          ( registro de providers por nome/env (
|   |   |— fake.py              ( FakeProvider para testes deterministacos (
|   |   |— groq.py             ( provider Groq( implementado na Fase te 2 (
|   |   |— openrouter.py        ( opcional,futuro (
|   |— tools/
|   |   |— __init__.py
|   |   |— registry.py         ( registry de tools versionado,risco,permissoes( ver contrato tool (
|   |   |— arquivo.py          ( ler/escrever/editar arquivos (
|   |   |— terminal.py         ( executar comandos via Sandbox( ADR-007 (
|   |   |— git.py              ( status,diff,commit( opcional(
|   |   |— rede.py             ( HTTP fetch( com allowlist( 
|   |— runtime/
|   |   |— __init__.py
|   |   |— sandbox.py        ( subprocess isolado( usuario/environment/timeout/captura de saida( ADR-007 (
|   |   |— process_manager.py   ( lifecycle de processos,reinicio (
|   |   |— eventos.py          ( bus de eventos interna,append-only( ADR-005 (
|   |   |— memória.py         ( leitura/escrita de memória JSON versionada( ADR-004 (
|   |   |— logs.py            ( logging estruturado JSON rotativo( ADR-011 (
|   |   |— verificacao.py     ( criterios de sucesso,como-verificar (
|   |   |— credenciais.py     ( credential broker:env sanitizado,sem segredos no repo (
|   |— __about__.py            ( versao,metadados (
|— tests/
|   |— conftest.py
|   |— fixtures/           ( FakeProvider,workspace temporario,event store tmp (
|   |— unit/                 ( testes por unidade (
|   |— integration/           ( ciclo completo agente+provider+fake (
|   |— cli/                  ( testes da CLI via subprocesso (
|— docs/
|   |— adr/                 ( ADRs( ja existente,ver ADR-001..011 (
|   |— contracts/           ( schemas JSON( ja existente,8 contratos (
|   |— design/              ( este documento + decisoes de design (
|— PROJECT_MEMORY/           ( memoria persistente do projeto( ja existente (
|— scripts/                   ( utilitarios de dev( export/import,migracoes,lint (
|— pyproject.toml           ( metadados,dependencias,entrada CLI (
|— nexora.toml              ( config declarativa do runtime+politicas( ADR-009 (
|— nexora.example.toml       ( exemplo versionado sem segredos (
|— .env.example               ( variaveis de ambiente exemplo( sem valores (
|— AGENTS.md                 ( memoria/instrucoes do agente neste repo (
|— README.md                 ( ja existente (
|— .gitignore                 ( ja existente (
```

## 2. Nomes e Namespaces dos Modulos( conforme 04_ARCHITECTURE_REQUIREMENTS.md (

| Modulo | Responsabilidade | Contrato(s) consumido(s) |
|--------|---------------------|------------------------------|
| `core` | Ciclo do agente;orquestracao interna( agente unico no MVP,ADR-010 ( | objetivo,plano,evento |
| `config` | Carregamento declarativo TOML/YAML+env+politicas | aprovacao( para gates (,tool( permissoes(|
| `providers` | Camada model-agnostica de IA( generate,stream,tools,caps,erros( |provider |
| `tools` | Ferramentas registradas,versionadas,com risco/permissoes |tool,aprovacao |
| `runtime` | Sandbox,process manager,eventos,memoria,logs,verificacao,credenciais |evento,memoria,verificacao |
| `cli` | Interface primaria( `python -m nexora` ( |objetivo( como input(,plano( como output( |

## 3. Fluxo de Modulos( como o ciclo do agente atravessa os contratos (

```
[CLI]  ( input: objetivo( 
   v
[core.ciclo]  ( recebe objetivo,gerencia estado (
   |--> [plano.dag]       ( monta/valida DAG de tarefas( plano( (
   |--> [providers]       ( escolhe provider( generate/stream(,modelo( (
   |       |--> [tools.registry]  ( resolve ferramentas permitidas( tool( (
   |       |       |--> [runtime.sandbox]  ( executa comandos/arquivos de forma isolada( (
   |       |       |--> [runtime.verificacao] ( criterios de sucesso( (
   |       |       v
   |       +--> [runtime.eventos]  ( registra tudo:acoes,erros,custos( evento( (
   |       +--> [runtime.logs]      ( logs operacionais estruturados( ADR-011 ( (
   |       +--> [runtime.memoria]   ( persiste aprendizados/decisoes( memoria( (
   |       +--> [runtime.credenciais]( ambiente sanitizado,sem segredos no repo( (
   |       +--> [runtime.aprovacao] ( gate humano quando acao sensivel( aprovacao( (
   v
[verificacao]  ( sucesso?criterios( 
   |--> se sim:[runtime.memoria] registra,evento,fim (
   |--> se nao:[core.ciclo] replaneja( nova iteracao(( com custo/limite( (
   v
[saida]  ( relatorio em JSON( para CLI/auditoria( (
```

## 4. Principios de Design da Estrutura

1. **Dependencias ao centro:** `core` nao conhece providers/tools concretos—apenas interfaces/contratos( model-agnostico((
2. **Contratos por schema primeiro:** todos os contratos( objetivo,plano,provider,evento,tool,delegacao,memoria,aprovacao( ja estao em `docs/contracts/`;o codigo ancora neles( por validacao pydantic/jsonschema((
3. **Extensibilidade:** novo provider = novo arquivo em `providers/` + registro( sem tocar o nucleo( novo tool = registry(;novo backend de memoria/eventos = trocar implementacao preservando interface((
4. **Seguranca por padrao:** sandbox com rede off,env sanitizado,limites;acoes sensiveis exigem aprovacao( ver ADR-007 e contrato aprovacao((
5. **Observabilidade nativa:** tudo gera evento( eventos(+ log( logs(— auditoria e custo rastreaveis((
6. **Testabilidade:** FakeProvider e fixtures( testes deterministacos;CLI testavel via subprocesso(;sem servico/portas no MVP( ADR-003((

## 5. Arquivos-Base Previstos( primeira entrega da Fase te 1 (

| Arquivo | Proposito |
|--------|----------|
| `pyproject.toml` | Metadados,pacote,entrada CLI( `python -m nexora` (( |
| `src/nexora/__init__.py` | Pacote vazio/versao |
| `src/nexora/__main__.py` | Call do cli.main( ( |
| `src/nexora/cli.py` | CLI minima( `--help`,`version`,estrutura de subcomandos( (
| `src/nexora/config/` | Carregamento de config TOML/YAML+env ( 
| `src/nexora/runtime/eventos.py` | Event store append-only inicial( (
| `src/nexora/runtime/logs.py` | Logging JSON rotativo( (
| `tests/conftest.py` + `tests/fixtures/` | Base de testes( FakeProvider,workspace tmp ( (
| `AGENTS.md` | Instrucoes do agente neste repo( (

> A **ordem exata e o escopo** de cada arquivo serao definidos pelo `NEXT_COMMAND.md` da Fase te 1 — a aprovacao do coordenador/criador e obrigatoria antes de qualquer codigo( conforme 14_AGENT_PROTOCOL.md((