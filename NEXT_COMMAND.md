# NEXT COMMAND — Fase 9: Experimentation Engine

> Canal de comando da coordenacao. Este arquivo contem o comando atual, a ser executado pelo agente construtor( OpenHands). Ao concluir, o agente deve atualizar PROJECT_MEMORY/15_HANDOFF.md e marcar esta secao como executada;; entao, o coordenador redigira o proximo comando aqui. O comando anterior( Fase 8 — Experience Engine) foi concluido e pushado;; 84 testes passando.

**Origem:** Coordenador/Arquiteto( Arena agent central, apos conclusao da Fase 8 e continuidade do roadmap.

## COMANDO — Fase 9: Experimentation Engine

**OBJETIVO:** Implementar o Experimentation Engine da NEXORA( motor de experimentacao: definir, executar e comparar variantes de abordagem/prompt/provider para uma mesma tarefa, medindo resultados de forma deterministic(, conforme roadmap.

**ESCOPO (o que produzir(:

1. `src/nexora/experimentacao/`( modulo com definicao de experimento( variantes( e executor deterministico de comparacao(.
2. Integracao com providers: executar variantes via provider e registrar metricas( sucesso,tentativas,saida.
3. CLI( `nexora experimento`( no cli.py, para definir e rodar experimentos(.
4. Testes unitarios( em tests/unit/test_experimentacao.py(.
5. Documentacao e memoria( atualizar 08_CURRENT_STATE,12_TESTS.md,13_CHANGELOG.md,15_HANDOFF.md e NEXT_COMMAND.md( trocar para Fase 10.

**FORA DE ESCOPO:** NAO implementar multi-agente;;NAO adicionar dependencias pip alem das ja existentes;;NAO alterar contratos existentes sem necessidade.

**CRITERIOS DE ACEITACAO:**

- [ ] `pytest tests/ -q` verde com novos testes( esperado: 84 + novos, sem regressoes.
- [ ] CLI `nexora experimento` funciona( com FakeProvider, sem rede.
- [ ] Experimentos definidos sao executaveis e comparaveis de forma deterministica.
- [ ] Tudo commitado e pushado com mensagem descritiva.
- [ ] 15_HANDOFF.md atualizado com novo ponto de continuacao( Fase 10, aguardando comando.

**PROTOCOLO:** seguir PROJECT_MEMORY/14_AGENT_PROTOCOL.md( sem excecoes: veracidade,rastreabilidade,autorizacao,comunicacao por eventos/arquivos,escrever em PT-BR,usar git com mensagens descritivas,etapas pequenas verificaveis.

**DATA DE VALIDADE:** v0.8.0 — valido ate a conclusao desta Fase 9;apos isso, aguardar novo comando do coordenador.

