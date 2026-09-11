# 13 — CHANGELOG
## v0.7.0 — Fase 7 (Research Engine) — 2026-09-10

- [x] `feat(agentes: pesquisa)`: ResearchAgent wraps AgenteRuntime com planejamento de consultas, execucao de buscas via ferramentas, sintese com fontes e verificacao de citacoes.
- [x] `feat(cli: agente pesquisar)`: subcomando `nexora agente pesquisar "<pergunta>" [--fontes] [--provider]` com ferramenta fake buscar para demo sem rede.
- [x] `test(agentes: pesquisa)`: 5 novos testes( planejamento,busca,sintese,limite,CLI; 74→79.),

## v0.6.0 — Fase 6 (Coding Agent) — 2026-09-10

- [x] `feat(agentes: coding)`: CodingAgent wraps AgenteRuntime com prompt de engenharia e verificador de codigo(sintaxe Python.
- [x] `feat(cli: agente codar)`: subcomando `nexora agente codar "<tarefa>" [--linguagem] [--provider]`; `executar` mantido.
- [x] `test(agentes: coding)`: 4 novos testes( 70 →74.)

## v0.5.0 — Fase 5 (NEXORA Agent Runtime) —  2026-09-10

- [x] `feat(runtime: observacao,analise,correcao,agente)`: runtime complete com loop OBJECTIVE-EXECUTE-OBSERVE-VERIFY-ANALYZE-CORRECT-RETEST( 58 →69.

## v0.4.0 — Fase 4 (Provider System) —  2026-09-10

- [x] feat(providers: manager): ProviderManager com executar(estatisticicas,healthcheck,nomes,saudaveis. e fallback no roteador( 51→58.

## v0.3.0 — Fase 3 (Orquestração de Agente) —  2026-09-10

- [x] feat(orquestracao: roteador,orquestrador): ciclo Objetivo->Plano->Executor->Verificador->Resultado,EventStore,CLI executar( 43→51.

## Anteriores

- v0.2.0 — Fase 2(Providers & Conectores)— commit 901c2c8.
- v0.1.0 — Fase 1(Fundação— commit e73a266.
- v0.0.1 — Fase 0.5(Decisão e Design.

