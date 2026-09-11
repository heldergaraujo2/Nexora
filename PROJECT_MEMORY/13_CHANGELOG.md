# 13 — CHANGELOG
## v0.9.0 — Fase 9( Experimentation Engine)— 2026-09-11

- [x] `feat(experimentacao)`: Experimento com variantes de abordagem e ExecutorExperimentos(executa variantes via provider, verifica saida, registra metricas deterministicas: total,sucessos,resultados.
- [x] `feat(cli: experimento)`: subcomando `nexora experimento rodar --nome --tarefa --variante [--provider]`; demais CLIs mantidos.
- [x] `test(experimentacao)`: 5 novos testes( 84 →89.)

## v0.8.0 — Fase 8( Experience Engine)— 2026-09-11

- [x] `feat(experiencia: registro)`: RegistroExperiencias com registrar/listar/resumir em JSONL append-only, consultas deterministicas por tipo com taxa de sucesso.
- [x] `feat(cli: experiencia)`: subcomando `nexora experiencia resumir|listar --arquivo`; demais CLIs mantidos.
- [x] `test(experiencia)`: 5 novos testes( 79 →84.)

## v0.7.0 — Fase 7( Research Engine)—  2026-09-10

- [x] `feat(agentes: pesquisa)`: ResearchAgent com planejamento de consultas, buscas via ferramentas, sintese com fontes e verificacao de citacoes.
- [x] `feat(cli: agente pesquisar)`: subcomando `nexora agente pesquisar` com ferramenta fake buscar para demo sem rede.
- [x] `test(agentes: pesquisa)`: 5 novos testes( 74 →79.)

## v0.6.0 — Fase 6( Coding Agent)—  2026-09-10

- [x] `feat(agentes: coding)`: CodingAgent com prompt de engenharia e verificador de codigo(sintaxe Python.
- [x] `feat(cli: agente codar)`: subcomando `nexora agente codar`; `executar` mantido.
- [x] `test(agentes: coding)`: 4 novos testes( 70 →74.)

## v0.5.0 — Fase 5( NEXORA Agent Runtime)—  2026-09-10

- [x] `feat(runtime: observacao,analise,correcao,agente)`: runtime complete com loop OBJECTIVE-EXECUTE-OBSERVE-VERIFY-ANALYZE-CORRECT-RETEST( 58 →69.

## v0.4.0 — Fase 4( Provider System)—  2026-09-10

- [x] feat(providers: manager): ProviderManager com executar(estatisticas,healthcheck,nomes,saudaveis.e fallback no roteador( 51→58.

## v0.3.0 — Fase 3( Orquestração de Agente)—  2026-09-10

- [x] feat(orquestracao: roteador,orquestrador): ciclo Objetivo->Plano->Executor->Verificador->Resultado,EventStore,CLI executar( 43→51.

## Anteriores

- v0.2.0 — Fase 2(Providers & Conectores)— commit 901c2c8.
- v0.1.0 — Fase 1(Fundação— commit e73a266.
- v0.0.1 — Fase 0.5(Decisão e Design.

