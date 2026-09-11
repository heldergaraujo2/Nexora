# NEXT COMMAND — Fase 10: Evolution Engine

> Canal de comando da coordenacao. Este arquivo contem o comando atual, a ser executado pelo agente construtor( OpenHands.. Ao concluir, o agente deve atualizar PROJECT_MEMORY/15_HANDOFF.md e marcar esta secao como executada;; entao, o coordenador redigira o proximo comando aqui. O comando anterior( Fase 9 — Experimentation Engine) foi concluido e pushado;; 89 testes passando.

**Origem:** Coordenador/Arquiteto( Arena agent central, apos conclusao da Fase 9 e continuidade do roadmap.

## COMANDO — Fase 10: Evolution Engine

**OBJETIVO:** Implementar o Evolution Engine da NEXORA( mecanismo para evoluir experiencias/estrategias com base em resultados acumulados, conforme roadmap.

**ESCOPO (o que produzir(:

1. `src/nexora/evolucao/`( modulo com registro de aprendizados e recomendacao de melhor variante/abordagem(.
2. Integracao com o Experimentation Engine( Fase 9): consumir resultados de experimentos para gerar aprendizados(.
3. CLI( `nexora evoluir`( no cli.py, para registrar aprendizados e recomendar evolucao(.
4. Testes unitarios( em tests/unit/test_evolucao.py(.
5. Documentacao e memoria( atualizar 08_CURRENT_STATE,12_TESTS.md,13_CHANGELOG.md,15_HANDOFF.md e NEXT_COMMAND.md( trocar para Fase 11.

**FORA DE ESCOPO:** NAO implementar multi-agente;;NAO adicionar dependencias pip alem das ja existentes;;NAO alterar contratos existentes sem necessidade.

**CRITERIOS DE ACEITACAO:**

- [ ] `python3 -m pytest tests/ -q` verde com novos testes( esperado: 89 + novos, sem regressoes.
- [ ] CLI `nexora evoluir` funciona( com FakeProvider, sem rede.
- [ ] Aprendizados sao registrados e recomendacoes derivam de resultados deterministicamente(.
- [ ] Tudo commitado e pushado com mensagem descritiva.
- [ ] 15_HANDOFF.md atualizado com novo ponto de continuacao( Fase 11, aguardando comando.

**PROTOCOLO:** seguir PROJECT_MEMORY/14_AGENT_PROTOCOL.md( sem excecoes: veracidade,rastreabilidade,autorizacao,comunicacao por eventos/arquivos,escrever em PT-BR,usar git com mensagens descritivas,etapas pequenas verificaveis.

**DATA DE VALIDADE:** v0.9.0 — valido ate a conclusao desta Fase 10;apos isso, aguardar novo comando do coordenador.

