# COMANDOS FINAIS — FASE WORKSPACE COMPLETO (Entrega Final da NEXORA)

> **Canal Analista → Construtor.** Este arquivo contém o comando único e completo da **Fase Final**: construir o **Workspace Completo** que o criador pediu — a janela prática para usar a NEXORA. O comando é auto-contido: leia, execute linha por linha, rode os testes, commite e faça push. **Não pare no meio.** Se algo falhar, corrija e continue. Ao final, reporte com commit hash + resumo + evidência de teste.**

---

## CONTEXTO OBRIGATÓRIO (leia nesta ordem)

1. `PROJECT_MEMORY/15_HANDOFF.md` — ponto de continuidade ( roadmap concluído;Fases 0–16 pushadas;128 testes verdes;v1.0.0 commitado e taggeado)
2. `PROJECT_MEMORY/08_CURRENT_STATE.md` — estado e estrutura
3. `src/nexora/orquestracao/orquestrador.py` — Orquestrador real ( ciclo Objetivo→Plano→Executor(provider roteado)→Verificador→Resultado)
4. `src/nexora/orquestracao/roteador.py` — roteador por palavra-chave/alias/default
5. `src/nexora/agentes/coding.py` e `src/nexora/agentes/pesquisa.py` — Coding/Research Agent reais
6. `src/nexora/runtime/eventos.py`, `runtime/memoria.py`, `runtime/logs.py` — registros reais
7. `src/nexora/providers/registry.py` — registro de providers ( fake,groq)
8. `PROJECT_MEMORY/14_AGENT_PROTOCOL.md` — protocolo obrigatório
9. `cli.py` — família de comandos `nexora executar|agente|experiencia|evoluir|economia|seguranca|memoria|recursos|portfolio|autonomia` ( todos existentes)

---

## OBJETIVO

Criar o **Workspace Completo da NEXORA**: uma interface web simples( servida **localmente** por **`http.server` stdlib**,sem dependências pip),que permita ao usuário/criador usar a plataforma de forma prática:

- **Entrada de objetivo em linguagem natural** → executa via `Orquestrador` real( com provider fake/groq);
- Painel com os **agentes especializados** ( `agente codar`, `agente pesquisar` — chamadas reais ao código;
- **Visualização de execução/estado**( resultado,sucesso,métricas,etapas,histórico em eventos;
- **Logs**( mostrar as últimas entradas do `LogJson` e do `EventStore`;
- **Memória**( mostrar as últimas entradas do `Memoria` e do `RegistroMemorias`;
- **Documentação de uso** → `README-WORKSPACE.md`( na raiz do repo,
- **Testes** → suíte completa nova que valida o servidor,as páginas e a integração( sem rede:

---

## ENTREGAS EXATAS ( crie TODOS estes arquivos:

### 1. `workspace/nexora_http.py` — servidor HTTP (stdlib)

- Use **apenas stdlib** (`http.server`, `urllib.parse`, `json`, `pathlib`, `threading`).
- **Rotas:** (`GET/POST`,URL-encoded e JSON)
 - `GET  /` → HTML do dashboard( abaixo)
  - `GET  /api/estado` → JSON: versão,últimas entradas de `historico/eventos.jsonl`,`logs.jsonl`,`memoria.jsonl`,e contagem de módulos
  - `POST /api/objetivo` → body `{"objetivo": "...", "provider": "fake|groq|auto"}` → cria `Orquestrador` real( ver passo 4)e devolve `{sucesso,etapas,metricas,resultado,historico_tail}`; registra em `EventStore` e `Memoria`
  - `POST /api/agente/codar` → body `{"tarefa": "...", "linguagem": "python", "provider": "fake"}` → chama `CodingAgent.codar()` real e devolve `{sucesso,saida_final,tentativas}`
  - `POST /api/agente/pesquisar` → body `{"pergunta": "...", "fontes": 3, "provider": "fake"}` → chama `ResearchAgent.pesquisar()` real e devolve `{sucesso,saida_final,tentativas}`
  - `POST /api/memoria` → body `{"chave","conteudo","escopo"}` → grava via `RegistroMemorias.lembrar()` e devolve ok
  - `GET  /api/logs` → últimas `N` linhas de `logs.jsonl` filtradas por nível
  - `GET  /api/eventos` → últimas `N` eventos de `eventos.jsonl`
  - `POST /api/limpar` → limpa os arquivos de estado( com confirmação `{"confirmar": true}`)e devolve ok
- **Diretório de dados:** respeitar env `NEXORA_DADOS_DIR`( default `.nexora_workspace/` na raiz do repo,ignorado pelo `.gitignore`( adicione `/.nexora_workspace/` e `/workspace/__pycache__/` ao `.gitignore`).
- **Tratamento de erros:** toda rota responde JSON com `sucesso:false` + `erro` legível em PT-BR;nunca estoure exceção para o browser.

###  ​2. `workspace/static/index.html` — frontend único( HTML+CSS+JS embutidos)

- **Visual:** dark mode,limpo,profissional( use fontes do sistema;sem CDN externo;;sem rede;
- **Seções:**
  - Cabeçalho:"NEXORA — Workspace"( com versão e badge de "128 testes • v1.0.0"(
  - **Entrada principal:** textarea + seletor de provider( `auto`, `fake`, `groq`) + botão **"Executar objetivo"** → `POST /api/objetivo` → exibe `sucesso`( verdech/vermelho `x`),métricas,e o texto gerado/resultado;
  - **Agentes especializados:** dois cards( "Coding Agent" com textarea+linguagem, "Research Agent" com textarea+fontes)→ botões **"Gerar código"** e **"Pesquisar"** → exibem saída final em `<pre>`;
  - **Memória rápida:** input chave+conteúdo + botão "Gravar memória" + lista das últimas 5 entradas;
  - **Estados/Logs:** três abas ou painéis( "Eventos","Logs","Memória")com última atualização e refresh manual( botão "Atualizar"(
  - Rodapé: caminhos dos arquivos( `.nexora_workspace/...`)e hint de uso( "Digite um objetivo em linguagem natural → Execute → veja o histórico em Eventos/Logs/Memória")。
**
  -
- **Comportamento JS:** `fetch()` puro( sem libs);atualiza estado ao carregar;exibe erros do JSON em destaque;desabilita botão durante execução( `disabled`),
**
###  ​3. `workspace/servir_workspace.py` — script de execução

- Lê `PORT` de env( default **8000**);printa `NEXORA Workspace → http://localhost:8000/`;chama `nexora_http.executar(porta)`.
- Executável direto( `python3 workspace/servir_workspace.py`).
**
###  ​4. `workspace/integracao.py` — fábrica real ligada ao código da NEXORA

- `montar_orquestrador(provider="auto")` → `RegistryProviders`( registra `fake`,`groq`)→ `Roteador`( default env `NEXORA_PROVIDER_PADRAO` ou `fake`)→ instancia o provider( `groq` **somente se** `GROQ_API_KEY` presente,senão error claro "Sem chave GROQ_API_KEY")→ `Orquestrador`.
- `montar_coding_agent(provider="fake")` e `montar_research_agent(provider="fake",buscar=_buscar_offline)` — a `_buscar_offline` é a mesma busca fake do `cli.py`( devolve 1 fonte fixa `{"titulo":"Nexora","url":"https://nexora.dev","trecho":"plataforma de agentes de IA"}`),para o Research Agent funcionar **sem rede**.
- Todas as funções importam de `nexora.*`( caminho real do `src/`);reuse, não reescreva,o `Orquestrador`, `CodingAgent`, `ResearchAgent`, `Roteador`, `RegistryProviders`.
**
###  ​5. `workspace/README-WORKSPACE.md` — documentação de uso do workspace

- O que é;como instalar( sem deps: só Python 3.10+);como rodar( `python3 workspace/servir_workspace.py`,acesse `http://localhost:8000/`);
- Comandos equivalentes no terminal( `nexora executar`, `nexora agente codar`, `nexora agente pesquisar`, etc.);
- Onde ficam os dados( `.nexora_workspace/eventos.jsonl`,`logs.jsonl`,`memoria.jsonl`,`seguranca.jsonl`,`economia.jsonl`,etc.);
- Exemplos de uso( 3 exemplos: objetivo, gerar código, pesquisar.
- Observação de segurança( servidor local;só expor em rede com camada de auth;estado é append-only JSON;
**
###  ​6. `.gitignore` — adicionar:

```
/.nexora_workspace/
workspace/__pycache__/
__pycache__/
*.pyc
```
**
###  ​7. Testes — `tests/unit/test_workspace_http.py` e `tests/unit/test_workspace_integracao.py`

**`test_workspace_integracao.py`( sem rede:**
- `montar_orquestrador("fake")` → objetivo simples → `sucesso:true`,`etapas:1`,`metricas.ok:1`,e que o histórico registrou `objetivo`,`plano`,`resultado`( via `EventStore` em `tmp_path` com `historico` do Orquestrador);
- `CodingAgent` fake → `codar("funcao que soma 2 numeros")` → retorna texto não-vazio e `sucesso:true`( sem rede;
- `ResearchAgent` fake+`_buscar_offline` → `pesquisar("o que e agentes de IA?")` → retorna `sucesso:true` e contém `[fonte:`( sem rede;
- `RegistroMemorias`+`RegistroExperiencias`+`RegistroPolitica`+`RegistroEconomia`+`RegistroRecursos`+`RegistroPortfolio`+`RegistroAutonomia` — escrever/ler em `tmp_path` e verificar round-trip( cada um: 1 assert);
- `montar_orquestrador("groq")` **sem** `GROQ_API_KEY` → levanta erro claro( `ProviderSemCredencial` ou mensagem contendo "chave")( usando `monkeypatch.delenv("GROQ_API_KEY", raising=False)`;
**

**`test_workspace_http.py`( sem rede;usa o servidor real injetado com fábrica fake:**
- Fixture cria o servidor em thread( `threading.Thread(target=...daemon=True)`)na porta `0`( porta livre)e expõe a porta real;
- `GET  /` → `200` e contém `"NEXORA — Workspace"` e `"Executar objetivo"`;
- `GET  /api/estado` → `200` e JSON com chaves esperadas( `versao`, `pasta_dados`, pelo menos um dos painéis);e que os arquivos JSONL so existem se criados( não criar lixo;
- `POST /api/objetivo`( body `{"objetivo":"teste rapido","provider":"fake"}`)→ `200`,JSON `sucesso:true`,`etapas:1`;e que **registrou**(+1 linha em `historico/eventos.jsonl` e em `memoria.jsonl`);
- `POST /api/agente/codar`( `{"tarefa":"def f(): return 1","linguagem":"python","provider":"fake"}`)→ `200`,JSON `sucesso:true` e `saida_final` não-vazio;
- `POST /api/agente/pesquisar`( `{"pergunta":"o que e Python?","fontes":2,"provider":"fake"}`)→ `200`,JSON `sucesso:true`( e contém `[fonte:` na resposta);
- `POST /api/memoria`( `{"chave":"k1","conteudo":"v1"}`)→ `200`,JSON `ok:true`;e `GET /api/memoria`? ( se existir a rota(,senão via `/api/estado`)confirma `k1` apareceu;
- `POST /api/objetivo` com provider **inválido** → `200`,JSON `sucesso:false` com `erro` não-vazio( não deve estourar servidor;
- `POST /api/limpar` sem confirmação → `sucesso:false`;com `{"confirmar":true}` → `sucesso:true` e arquivos zerados(sem apagar o diretório;
- Ao final da suíte,rodar `python3 -m pytest tests/unit/test_workspace_integracao.py tests/unit/test_workspace_http.py -q` — **todos verdes**,e depois a suíte completa `python3 -m pytest tests/ -q` — **128 + novos TODOS verdes**.


---

## CRITÉRIOS DE ACEITAÇÃO ( VERICÁVEIS, nesta ordem:

1. [ ] `python3 workspace/servir_workspace.py` sobe na porta 8000( print "NEXORA Workspace → http://localhost:8000/"()
2. [ ] `curl http://localhost:8000/` devolve HTML com "NEXORA — Workspace" e "Executar objetivo";
3. [ ] `curl -X POST http://localhost:8000/api/objetivo -d '{"objetivo":"teste rapido","provider":"fake"}' -H "Content-Type: application/json"` → JSON `sucesso:true`,`etapas:1`;e criar `.nexora_workspace/eventos.jsonl` e `memoria.jsonl` com +1 linha cada;
4. [ ] `curl -X POST http://localhost:8000/api/agente/codar ...` → `sucesso:true` com código gerado;
5. [ ] `curl -X POST http://localhost:8000/api/agente/pesquisar ...` → `sucesso:true` com `[fonte:` na saída;
6.. [ ] Suíte nova: `python3 -m pytest tests/unit/test_workspace_integracao.py tests/unit/test_workspace_http.py -q` — **verdes**;
7.. [ ] Suíte completa: `python3 -m pytest tests/ -q` — **128 + novos,TODOS verdes**,sem regressão;
8. [ ] `.gitignore` inclui `.nexora_workspace/` e `workspace/__pycache__/`;
9. [ ] `git status` limpo( exceto os arquivos novos de entrega+e `.gitignore`;`git add -A`;commit descritivo: **`feat(workspace): janela completa da NEXORA — dashboard web local,API JSOn e integracao real com orquestrador/agentes;testes verdes`**;
10.. [ ] **PUSH** para `origin/main`;
11.. [ ] `git tag -a v1.1.0 -m "Workspace completo da NEXORA"` e `git push origin v1.1.0`;

---

## PROTOCOLO ( sem exceções:

- Siga `PROJECT_MEMORY/14_AGENT_PROTOCOL.md`( veracidade,rastreabilidade,autorização,comunicação por arquivos,PT-BR,git descritivo,etapas pequenas;
- **Teste antes de concluir** cada etapa( os comandos estão embutidos no ESCOPO de cada entrega;
- **Não adicione dependências pip**;stdlib apenas( `http.server` etc.);
- **Não reescreva o núcleo**( Orquestrador/Coding/Research/Provider):importe e use;
- **Limpe zero-width spaces** antes do commit( ex: `grep -rP '\xe2\x80\x8b|\xe2\x80\x8c|\xe2\x80\x8d' workspace/ tests/ || echo limpo`);
- Ao concluir,atualize `PROJECT_MEMORY/08_CURRENT_STATE.md`,`09_DECISIONS.md`,`11_TASKS.md`,`12_TESTS.md`,`13_CHANGELOG.md` e `15_HANDOFF.md`( registrando a Fase Final concluída,v1.1.0,e ponte de continuação = "projeto concluído;aguardar novas diretrizes do criador/coordenador"));

---

## REPORTE AO ANALISTA ( ao final:

1. Commit hash( e tag v1.1.0;
2. Resumo do que entregou( arquivos,rotas,teses;
3. Evidência do teste( saída `pytest -q` final);
4. Próximo passo( "Projeto NEXORA concluído;aguardando novas diretrizes")