# 13 — CHANGELOG
## v0.6.0 — Fase 6 (Coding Agent) — 2026-09-10

- [x] `feat(agentes: coding)`: CodingAgent wraps AgenteRuntime com prompt de engenharia(tarefa,linguagem)e verificador de código(sintaxe Python via compile; retorna ResultadoAgente.
- [x] `feat(agentes: __init__)`: export público do pacote.
- [x] `feat(cli: agente codar)`: subcomando `nexora agente codar "<tarefa>" [--linguagem] [--provider]`; `executar` mantido.
- [x] `test(agentes: coding)`: 4 novos testes( geração válida, correção de sintaxe, limite de tentativas, CLI.
- [x] `test(orquestracao: cli)`: +1 regressão do `executar`( 70 →74.

## v0.5.0 — Fase 5 (NEXORA Agent Runtime) — 2026-09-10

- [x] `feat(runtime: observacao)`: Observacao dataclass(etapa_id,saida,ok,erro,metadados,carimbo.
- [x] `feat(runtime: analise)`: AnalisadorFalhas classifica falhas por marcadores(429/500/timeout,retentavel/irreversivel,plano retry/abort.
- [x] `feat(runtime: correcao)`: Corrector aplica acoes(rerun/troca_provider/ajuste_prompt.e registra eventos.
- [x] `feat(runtime: agente)`: AgenteRuntime loop completo com max_tentativas,e correção só para ajuste_prompt.
- [x] `test(runtime)`:11 novos testes( 58→69.

## v0.4.0 — Fase 4 (Provider System) — 2026-09-10

- [x] feat(providers: manager): ProviderManager com executar(estatisticicas,healthcheck,nomes,saudaveis.
- [x] feat(orquestracao: roteador): fallback automático por prioridade de saudáveis(RuntimeError tipado.

## v0.3.0 — Fase 3 (Orquestração de Agente) — 2026-09-10

- [x] feat(orquestracao: roteador): mapeia objetivo->provider por palavras-chave,alias e default.
- [x] feat(orquestracao: orquestrador): ciclo Objetivo->Plano->Executor->Verificador->Resultado;histórico;métricas.
- [x] feat(runtime: eventos): EventStore escreve JSONL.- [x] feat(cli: executar): subcomando `nexora executar "<objetivo>" [--provider alias]`.
- [x] test(orquestracao):8 novos testes( 43→51.e correções de registry/plano/CLI.

## Anteriores

- v0.2.0 — Fase 2(Providers & Conectores)— commit 901c2c8.
- v0.1.0 — Fase 1(Fundação— commit e73a266.
- v0.0.1 — Fase 0.5(Decisão e Design.

