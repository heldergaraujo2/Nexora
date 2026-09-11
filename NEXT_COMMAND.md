# NEXT COMMAND — Fase 5: NEXORA Agent Runtime

> Canal de comando da coordenacao. Este arquivo contem o comando atual, a ser executado pelo agente construtor( OpenHands). Ao concluir,, o agente deve atualizar PROJECT_MEMORY/15_HANDOFF.md e marcar esta secao como executada; entao,, o coordenador redigira o proximo comando aqui.. O comando anterior( Fase  4 — Provider System) foi concluido e pushado;; 58 testes passando.

**Origem:** Coordenador/Arquiteto( Arena agent central) — apos conclusao da Fase  4 e aprovacao do analista..


## COMANDO — Fase 5: NEXORA Agent Runtime

**OBJETIVO:** Implementar o runtime de agente generalista com ciclo completo OBJECTIVE->PLAN->EXECUTE->OBSERVE->VERIFY->ANALYZE->CORRECT->RETEST, integrando memoria, observacao, analise e correcao em um loop unico controlado.

**ESCOPO ( o que produzir:**

1. Orchestrator de ciclo autonomo em src/nexora/runtime/agente.py: loop com observacao da saida, analise de falha,e correcao antes de reverificar( com limite de iteracoes e orcamento).
2. Observador em src/nexora/runtime/observacao.py: captura saidas e resultados de forma estruturada( para alimentar analise e memoria).
3. Analisador de falhas em src/nexora/runtime/analise.py: classifica falhas( retry/replan/abort) com base em regras declarativas.
4. Corrector em src/nexora/runtime/correcao.py: aplica acoes corretivas(rerun, ajuste de prompt, troca de provider) registrando eventos.
5. Limites/seguranca: iteracoes maximas, orcamento de custo/tempo,sempre logados; paragem elegante.
6. Testes unitarios em tests/unit/: test_runtime_agente.py( ciclo completo com FakeProvider), test_runtime_observacao.py, test_runtime_analise.py, test_runtime_correcao.py.

**FORA DE ESCOPO:** NAO implementar ferramentas reais alem do registry vazio;NAO multi-agente;NAO adicionar dependencias pip.

**CRITERIOS DE ACEITACAO:**

- [ ] python3 -m nexora executar "escreva um oi" continua funcionando( FakeProvider sem rede)
- [ ] Ciclo autonomo corrige saida vazia ate 2 tentativas antes de abortar
- [ ] Suite completa verde( esperado: 58 + novos, sem regressoes)
- [ ] Tudo commitado e pushado com mensagem descritiva
- [ ] 15_HANDOFF.md atualizado com novo ponto de continuacao( Fase  6 — Coding Agent,, aguardando comando)

**PROTOCOLO:** seguir PROJECT_MEMORY/14_AGENT_PROTOCOL.md( sem excecoes: veracidade,rastreabilidade,autorizacao,comunicacao por eventos/arquivos,escrever em PT-BR,usar git com mensagens descritivas,etapas pequenas verificaveis)

**DATA DE VALIDADE:** v0.4.0 — valido ate a conclusao desta Fase  5;apos isso,, aguardar novo comando do coordenador..
