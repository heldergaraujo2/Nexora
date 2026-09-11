# NEXT COMMAND — Fase 7: Research Engine

> Canal de comando da coordenacao. Este arquivo contem o comando atual, a ser executado pelo agente construtor ( OpenHands). Ao concluir,, o agente deve atualizar PROJECT_MEMORY/15_HANDOFF.md e marcar esta secao como executada;; entao,, o coordenador redigira o proximo comando aqui. O comando anterior( Fase  6 — Coding Agent) foi concluido e pushado;; 74 testes passando.

**Origem:** Coordenador/Arquiteto( Arena agent central, apos conclusao da Fase  6 e continuidade do roadmap.

## COMANDO — Fase 7: Research Engine

**OBJETIVO:** Implementar o Research Engine da NEXORA( motor de pesquisa e sintese de informacao, integrado ao runtime e ao Coding Agent(, capaz de receber uma pergunta/topico, planejar consultas, executar buscas via ferramentas( mocked/registry), sintetizar uma resposta verificada e registrar tudo no EventStore.

**ESCOPO (o que produzir(:**

1. `src/nexora/agentes/pesquisa.py` — ResearchAgent( wrap do AgenteRuntime com prompt de pesquisa, uso do RegistryFerramentas para buscas( fake/mock em testes), sintese da resposta e verificacao de presenca de fontes/citacoes.
2. `src/nexora/agentes/__init__.py` — export ResearchAgent.
3. Integracao com Provider System( usa FakeProvider/Groq via CLI.
4. CLI( `nexora agente pesquisar "<pergunta>"`( no cli.py, com `--provider` e `--fontes N`.
5. Testes unitarios em tests/unit/test_agentes_pesquisa.py( planejamento de consultas, execucao de busca via registry, sintese com citacoes, limite de tentativas.
6. Documentacao e memoria( atualizar 08_CURRENT_STATE,,12_TESTS.md,,13_CHANGELOG.md,,15_HANDOFF.md e NEXT_COMMAND.md( trocar para Fase  8 — Experience Engine.

**FORA DE ESCOPO:** NAO implementar ferramentas/plugins reais( alem do registry vazio);NAO multi-agente;;NAO adicionar dependencias pip.

**CRITERIOS DE ACEITACAO:**

- [ ] `python3 -m nexora agente pesquisar "o que e a nexora"` executou( com FakeProvider, sem rede.
- [ ] ResearchAgent planeja consultas e executa buscas via RegistryFerramentas( fake/mock.
- [ ] Resposta sintetizada contem citacoes/fontes presentes no resultado.
- [ ] Suite completa verde( esperado:  74 + novos,, sem regressoes.
- [ ] Tudo commitado e pushado com mensagem descritiva.
- [ ] 15_HANDOFF.md atualizado com novo ponto de continuacao( Fase  8 — Experience Engine,, aguardando comando.

**PROTOCOLO:** seguir PROJECT_MEMORY/14_AGENT_PROTOCOL.md( sem excecoes: veracidade,,rastreabilidade,,autorizacao,,comunicacao por eventos/arquivos,,escrever em PT-BR,,usar git com mensagens descritivas,,etapas pequenas verificaveis.

**DATA DE VALIDADE:** v0.6.0 — valido ate a conclusao desta Fase  7;apos isso,, aguardar novo comando do coordenador.

