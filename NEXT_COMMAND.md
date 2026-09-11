# NEXT COMMAND — Fase 6: Coding Agent

> Canal de comando da coordenacao. Este arquivo contem o comando atual,, a ser executado pelo agente construtor ( OpenHands). Ao concluir,, o agente deve atualizar PROJECT_MEMORY/15_HANDOFF.md e marcar esta secao como executada;; entao,, o coordenador redigira o proximo comando aqui. O comando anterior( Fase  5 — NEXORA Agent Runtime) foi concluido e pushado;; 69 testes passando.

**Origem:** Coordenador/Arquiteto( Arena agent central, apos conclusao da Fase  5 e aprovacao do analista.

## COMANDO — Fase 6: Coding Agent

**OBJETIVO:** Implementar o Coding Agent da NEXORA( agente especializado em geracao e edicao de codigo,, integrado ao runtime da Fase  5), com planejamento de tarefas,, execucao controlada e verificacao por testes.

**ESCOPO (o que produzir(:

1. `src/nexora/agentes/coding.py` — CodingAgent( wraps AgenteRuntime com prompt de engenharia( tarefa,, linguagem,, contexto) e verificador de codigo( testa sintaxe e heurísticas basicas).
2. `src/nexora/agentes/__init__.py` — exportes publica do pacote.
3. Integracao com Provider System( usa ProviderManager ou FakeProvider via CLI).
4. CLI( `nexora agente codar "<tarefa>"` no clipy,( ou subcomando `codar`)。。
5. Testes unitarios em tests/unit/test_agentes_coding.py( geracao chamando o runtime,, correcao por verificacao falhando,, limite de tentativas).
6. Documentacao e memoria( atualizar 08_CURRENT_STATE,,12_TESTS.md,,13_CHANGELOG.md,,15_HANDOFF.md e NEXT_COMMAND.md( trocar para Fase  7 — Research Engine).

**FORA DE ESCOPO:** NAO implementar ferramentas/plugins reais( alem do registry vazio);NAO multi-agente;;NAO adicionar dependencias pip.

**CRITERIOS DE ACEITACAO:**

- [ ] `python3 -m nexora agente codar "escreva um oi em python"` executou( com FakeProvider, sem rede)。
- [ ] CodingAgent corrige codigo invalido( sintaxe) ate  2 tentativas( usando AnalisadorFalhas)。
- [ ] Suite completa verde( esperado:  69 + novos,, sem regressoes)。
- [ ] Tudo commitado e pushado com mensagem descritiva.
- [ ] 15_HANDOFF.md atualizado com novo ponto de continuacao( Fase  7 — Research Engine,, aguardando comando)。

**PROTOCOLO:** seguir PROJECT_MEMORY/14_AGENT_PROTOCOL.md( sem excecoes: veracidade,,rastreabilidade,,autorizacao,,comunicacao por eventos/arquivos,,escrever em PT-BR,,usar git com mensagens descritivas,,etapas pequenas verificaveis)。

**DATA DE VALIDADE:** v0.5.0 — valido ate a conclusao desta Fase  6;apos isso,, aguardar novo comando do coordenador.
