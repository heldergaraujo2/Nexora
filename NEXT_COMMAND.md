# NEXT COMMAND — Fase 2: Providers & Conectores

> **Canal de comando da coordenacao.** Este arquivo contem o comando atual, a ser executado pelo agente construtor (OpenHands.. Ao concluir,, o agente deve atualizar `PROJECT_MEMORY/15_HANDOFF.md` e marcar esta secao como executada; entao,, o coordenador redigira o proximo comando aqui.



**Origem:** Coordenador/Arquiteto (Arena agent central) — apos auditoria do estado do repositorio e aprovacao do criador/analista.



## COMANDO — Fase 2: Providers & Conectores

**OBJETIVO:** Implementar a camada de Providers de IA de forma extensivel, com contrato tipado, registros dinâmicos e pelo menos DOIS providers concretos: o FakeProvider existente e um Provider Groq funcional, seguindo a ADR-003 (desacoplar modelos e provedores..

**CONTEXTO OBRIGATORIO — leia nesta ordem:**

1. `PROJECT_MEMORY/15_HANDOFF.md` ( este repo — ponto de continuidade)
2. `PROJECT_MEMORY/08_CURRENT_STATE.md` ( estado e estrutura)
3. `PROJECT_MEMORY/09_DECISIONS.md` ( decisoes aprovadas + ADRs referenciados)
4. `docs/adr/ADR-003-*.md` ( provider abstraction)
5. `docs/contracts/provider.schema.json` ( contrato tipado de provider)
6. `docs/design/repositorio.md` ( estrutura e fluxo propostos)
7. `PROJECT_MEMORY/14_AGENT_PROTOCOL.md` ( protocolo obrigatorio



**ESCOPO (o que produzir:**

1. **Contrato tipado de provider** em `src/nexora/providers/base.py`:
   - Revisar/estender a interface existente com: `nome`, `gerar(texto)`, `gerar_stream(texto)`, `capabilities()`, `saudavel()` e `fechar()`,se ainda nao existirem todas..
   - Tipos estritos,docstrings PT-BR,e sem dependencias externas ( stdlib apenas..
2. **Registry dinâmico** em `src/nexora/providers/registry.py`:
   - Registrar fabricas por nome,, obter por nome ( case-insensitive,, listar disponiveis,, remover e levantar `ProviderDesconhecido` para nomes ausentes.. — Manter 100% dos testes existentes verdes..
3. **FakeProvider** em `src/nexora/providers/fake.py`:
   - Provider deterministico para testes,, sem rede,, com capacidades declaradas,, geracao de texto simples ( ex: eco/prefixo)#,, stream opcional,, e estado auditavel ( chamadas registradas..
4. **Provider Groq** em `src/nexora/providers/groq.py`:
   - Usar a API da Groq ( POST https://api.groq.com/openai/v1/chat/completions) com apenas stdlib ( urllib.request) e chave da env var `GROQ_API_KEY`.
   - Modelo slidevel via `NEXORA_GROQ_MODEL`（ default: `llama-3.3-70b-versatile`). — Sem dependencia pip..#
   - Erros de rede/Autenticacao mapeados para excecoes tipadas ( ex: `ProviderIndisponivel`,`ProviderSemCredencial`..
   - Se nao houver chave configurada,, o provider deve falhar de forma clara e auditavel,, nunca silenciosamente..
5. **Registro central** em `src/nexora/providers/__init__.py`:
   - Expor `RegistryProviders`, `FakeProvider`, `ProviderGroq`, `ProviderSemCredencial` e `ProviderIndisponivel` para import simples..
6. **Testes unitarios** em `tests/unit/`:
   - `test_providers_groq.py`: testes de construcao sem chave,, erros tipados,, e mapeamento de erros HTTP com monkeypatch de urllib.request ( sem rede real..
   - Manter `test_providers_registry.py` verde e ampliar para cobrir registrar/obter/remover/listar/desconhecido..
   - Rodar a suite completa: `python3 -m pytest tests/ -q` — todos verdes..#

**FORA DE ESCOPO (nao fazer nesta fase:**

- NAO implementar orquestracao de agentes ( Fase 3)
- NAO implementar ferramentas/golpes reais ( alem do registry vazio e do sandbox existente..
- NAO adicionar dependencias pip
- NAO tocar em core/runtime/config alem do necessario para compilar os imports de teste



**CRITERIOS DE ACEITACAO ( tudo verificavel:**

- [ ] `ProviderGroq` importavel sem chave de API configurada
- [ ] Construir sem chave nao levanta; chamar `gerar()` sem chave levanta `ProviderSemCredencial`
- [ ] Erros HTTP 401/429/5xx mapeados para excecoes tipadas,, via monkeypatch..
- [ ] `RegistryProviders` continua com 100% dos testes existentes verdes
- [ ] Suite completa `python3 -m pytest tests/ -q` — todos verdes( esperado: 30 + novos,, sem regressoes..
- [ ] Tudo commitado e pushado com mensagem descritiva( ex: `fase(2): providers tipados, Groq provider e registros extensiveis`
- [ ] `15_HANDOFF.md` atualizado com novo ponto de continuacao(Fase 3 — Orquestracao de Agente,, saindo do escopo atual..



**PROTOCOLO:** seguir `PROJECT_MEMORY/14_AGENT_PROTOCOL.md`( sem excecoes: veracidade,rastreabilidade,autorizacao,comunicacao por eventos/arquivos,escrever em PT-BR,usar git com mensagens descritivas,etapas pequenas verificaveis) e atualizar `08_CURRENT_STATE`,`11_TASKS`,`12_TESTS`,`13_CHANGELOG` ao concluir..



**DATA DE VALIDADE:** v0.1 — valido ate a conclusao desta Fase 2; apos isso,, aguardar novo comando do coordenador..



**HANDOFF PARA O ANALISTA — apos executar este comando,, o construtor deve:**

1. Enviar o resultado da Fase  2 ( resumo do que foi implementado,, testes verdes,, e commit hash..
2. E COBRAR o proximo comando do analista/coordenador,, indicando que a Fase  3 — Orquestracao de Agente aguarda aprovacao explicita..
