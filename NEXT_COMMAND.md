# NEXT COMMAND — Fase 8: Experience Engine

> Canal de comando da coordenacao. Este arquivo contem o comando atual, a ser executado pelo agente construtor( OpenHands). Ao concluir,, o agente deve atualizar PROJECT_MEMORY/15_HANDOFF.md e marcar esta secao como executada;; entao,, o coordenador redigira o proximo comando aqui. O comando anterior( Fase  7 — Research Engine) foi concluido e pushado;; 79 testes passando.

**Origem:** Coordenador/Arquiteto( Arena agent central, apos conclusao da Fase  7 e continuidade do roadmap.

## COMANDO — Fase 8: Experience Engine

**OBJETIVO:** Implementar o Experience Engine da NEXORA( motor de experiencia do agente: registrar, consultar e resumir decisoes e resultados ao longo do tempo, harmonizando-se com o runtime e a memoria existente(, conforme 10_MODULES.md.

**ESCOPO (o que produzir(:**

1. `src/nexora/experiencia/`( modulo com registrador de experiencias( e consultas deterministicas insipidadas na memoria JSON existente(.,
2. Integracao com o runtime: registrar eventos de sucesso/falha por tipo de tarefa.
3. CLI( `nexora experiencia`( no cli.py, para listar e resumir experiencias(.
4. Testes unitarios( em tests/unit/test_experiencia.py(.
5. Documentacao e memoria( atualizar 08_CURRENT_STATE,,12_TESTS.md,,13_CHANGELOG.md,,15_HANDOFF.md e NEXT_COMMAND.md( trocar para Fase  9.

**FORA DE ESCOPO:** NAO implementar multi-agente;;NAO adicionar dependencias pip alem das ja existentes;;NAO alterar contratos existentes sem necessidade.

**CRITERIOS DE ACEITACAO:**

- [ ] `pytest tests/ -q` verde com novos testes( esperado:  79 + novos,, sem regressoes.
- [ ] CLI `nexora experiencia` funciona( com FakeProvider, sem rede.
- [ ] Experiencias registradas sao consultaveis e resumiveis de forma deterministica.
- [ ] Tudo commitado e pushado com mensagem descritiva.
- [ ] 15_HANDOFF.md atualizado com novo ponto de continuacao( Fase  9,, aguardando comando.

**PROTOCOLO:** seguir PROJECT_MEMORY/14_AGENT_PROTOCOL.md( sem excecoes: veracidade,,rastreabilidade,,autorizacao,,comunicacao por eventos/arquivos,,escrever em PT-BR,,usar git com mensagens descritivas,,etapas pequenas verificaveis.

**DATA DE VALIDADE:** v0.7.0 — valido ate a conclusao desta Fase  8;apos isso,, aguardar novo comando do coordenador.

