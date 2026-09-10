# NEXT COMMAND — Fase 3: Orquestracao de Agente

> **Canal de comando da coordenacao.** Este arquivo contem o comando atual, a ser executado pelo agente construtor( OpenHands). Ao concluir,, o agente deve atualizar PROJECT_MEMORY/15_HANDOFF.md e marcar esta secao como executada; entao,, o coordenador redigira o proximo comando aqui.. O comando anterior( Fase  2 — Providers & Conectoresaconcluido e pushado; 43 testes passando..

**Origem:** Coordenador/Arquiteto( Arena agent central) — apos conclusao da Fase  2 e aprovacao do analista..



## COMANDO — Fase 3: Orquestracao de Agente

**OBJETIVO:** Implementar o loop de orquestracao do agente que recebe um objetivo em linguagem natural, planeja tarefas, executa com um Provider de IA( roteado por configuracao), verifica a saida e registra o historico( memoria/eventos), integrando os modulos da Fase  1( core) e Fase  2( providers) em um fluxo unico..

**CONTEXTO OBRIGATORIO — leia nesta ordem:**

1. PROJECT_MEMORY/15_HANDOFF.md( ponto de continuidade)
2. PROJECT_MEMORY/08_CURRENT_STATE.md( estado e estrutura}
3. PROJECT_MEMORY/09_DECISIONS.md( decisoes e ADRs referenciados}
4. docs/adr/ADR-006-*.md( contrato de provider}
5. docs/contracts/objetivo.schema.json e plano.schema.json( contratos de objetivo/plano}
6. src/nexora/core/ciclo.py( executor/ciclo existente—— base da orquestracao}
7. PROJECT_MEMORY/14_AGENT_PROTOCOL.md( protocolo obrigatorio}

**ESCOPO (o que produzir:**

1. **Orquestrador** em src/nexora/orquestracao/orquestrador.py:
   - Classe Orquestrador que recebe objetivo(texto) e executa o ciclo completo: Objetivo→Plano→Executor( provider roteado)→Verificador→Resultado( com historico/eventos)}
   - Usar módulos existentes( core/ciclo, core/objetivo, core/plano, runtime/verificacao, runtime/eventos, runtime/memoria) sem reescreve-los..]
   - Provider escolhido via RegistryProviders por nome/alias( config;NOTE: registrar fabricas "fake" e "groq" por padrao.}
   - Se o provider nao estiver disponivel/saudavel,, levantar erro tipado claro e registrar no historico.}

2. **Roteamento de Provider** em src/nexora/orquestracao/roteador.py:
   - Mapa objetivo→provider recomendado( regras simples e declarativas:ex, objetivo "groq"/"ia"→groq;"teste"/"fake"→fake;default→config NEXORA_PROVIDER_PADRAO ou "fake")
   - Registrar/obter alias no RegistryProviders( case-insensitive}

3. **CLI atualizada** em src/nexora/cli.py:
   - Comando `nexora executar "<objetivo>"` que usa Orquestrador e imprime resultado( text) ao usuario, com erros claros.}

4. **Persistencia minima** em src/nexora/runtime/memoria.py( se ainda nao houver): adicionar metodos para salvar/carregar episodios em JSON( append-only, arquivo em NEXORA_MEMORIA_ARQUIVO ou .nexora/memoria.jsonl).}

5. **Testes unitarios** em tests/unit/:
   - test_orquestrador.py: ciclo completo com FakeProvider( objetivo→plano→execucao→verificacao→resultado}
   - test_roteador.py: selecao de provider por alias/objetivo/default/manipulacao de registro( sem rede}
   - test_cli_executar.py: comando CLI com objetivo simples( monkeypatch no Orquestrador) e sem provider real
   - Manter TODOS os 43 testes existentes verdes.}

**FORA DE ESCOPO( nao fazer nesta fase:**

- NAO implementar ferramentas reais( tools) alem do registry vazio existente;}
- NAO implementar agentes paralelos/multi-agente( P10:nao no MVP)}
- NAO adicionar dependencias pip}
- NAO tocar em providers/Fase  2 salvo necesitarlos pontuais( sem reescrever ProviderGroq/FakeProvider/registry}]

**CRITERIOS DE ACEITACAO( tudo verificavel:}

- [ ] `python3 -m nexora executar "escreva um oi"` funciona com FakeProvider sem rede( e com ProviderGroq quando NEXORA_PROVIDER_PADRAO=groq e chave presente)}
- [ ] Ciclo completo registra historico/memoria/eventos( e resultado verificavel.}
- [ ] RegistryProviders exporta fabricas padrao( fake,groq)};roteador seleciona por objetivo/alias/default}
- [ ] Suite completa `python3 -m pytest tests/ -q` — todos verdes( esperado:43 + novos, sem regressoes}
- [ ] Tudo commitado e pushado com mensagem descritiva( ex: `feat(fase-3): orquestracao de agente com roteamento de providers,CLI executar e memoria JSON`}
- [ ] 15_HANDOFF.md atualizado com novo ponto de continuacao( Fase  4 — Ferramentas e Execucao( outils), aguardando comando}

**PROTOCOLO:** seguir PROJECT_MEMORY/14_AGENT_PROTOCOL.md( sem excecoes: veracidade,rastreabilidade,autorizacao,comunicacao por eventos/arquivos,escrever em PT-BR,usar git com mensagens descritivas,etapas pequenas verificaveis) e atualizar 08_CURRENT_STATE,09_DECISIONS,11_TASKS,12_TESTS,13_CHANGELOG e 15_HANDOFF ao concluir..]

**DATA DE VALIDADE:** v0.2.0 — valido ate a conclusao desta Fase  3;}apos isso,, aguardar novo comando do coordenador..

**HANDOFF PARA O ANALISTA — apos executar este comando,, o construtor deve:**

1. Enviar o resultado da Fase  3( resumo,testes verdes,e commit hash}
2. E COBRAR o proximo comando do analista/coordenador,, indicando que a Fase  4 — Ferramentas e Execucao( tools) aguarda aprovacao explicita..]]
