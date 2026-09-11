# NEXT COMMAND — Fase 11: Economic Engine

> Canal de comando da coordenacao. Este arquivo contem o comando atual, a ser executado pelo agente construtor( OpenHands.. Ao concluir, o agente deve atualizar PROJECT_MEMORY/15_HANDOFF.md e marcar esta secao como executada;; entao, o coordenador redigira o proximo comando aqui.. O comando anterior( Fase 10 — Evolution Engine) foi concluido e pushado;; 94 testes passando..



**Origem:** Coordenador/Arquiteto( Arena agent central, apos conclusao da Fase  10 e continuidade do roadmap..


## COMANDO — Fase 11: Economic Engine


**OBJETIVO:** Implementar o Economic Engine da NEXORA( mecanismo para medir custo/consumo de cada execucao/experimento por provider, conforme roadmap..


**ESCOPO (o que produzir(:**

1. `src/nexora/economia/`( modulo com registro de custos de execucoes/experimentos( custo por provider, tokens, estimativa monetaria quando disponivel(..
2. Integracao com Providers( Fase 2/4): capturar metadados de uso/custo na execucao via provider( quando disponiveis.:
3. Integracao com Execucao/Experimentacao( Fases  3/9): registrar custo por objetivo executado e por experimento rodado(..
4. CLI( `nexora economia`( no cli.py, para registrar custos e resumir por provider(..
5. Testes unitarios( em tests/unit/test_economia.py(..
6. Documentacao e memoria( atualizar 08_CURRENT_STATE,12_TESTS.md,13_CHANGELOG.md,15_HANDOFF.md e NEXT_COMMAND.md( trocar para Fase  12.



**FORA DE ESCOPO:** NAO implementar multi-agente;;NAO adicionar dependencias pip alem das ja existentes;;NAO alterar contratos existentes sem necessidade..


**CRITERIOS DE ACEITACAO:**

- [ ] `python3 -m pytest tests/ -q` verde com novos testes( esperado: 94 + novos, sem regressoes..
- [ ] CLI `nexora economia` funciona( com FakeProvider, sem rede..
- [ ] Custos sao registrados e resumos derivam deterministicamente( por provider(..
- [ ] Tudo commitado e pushado com mensagem descritiva..
- [ ] 15_HANDOFF.md atualizado com novo ponto de continuacao( Fase 12, aguardando comando..


**PROTOCOLO:** seguir PROJECT_MEMORY/14_AGENT_PROTOCOL.md( sem excecoes: veracidade,rastreabilidade,autorizacao,comunicacao por eventos/arquivos,escrever em PT-BR,usar git com mensagens descritivas,etapas pequenas verificaveis..


**DATA DE VALIDADE:** v0.10.0 — valido ate a conclusao desta Fase  11;apos isso, aguardar novo comando do coordenador..


