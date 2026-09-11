# 13 — CHANGELOG

## v0.4.0 — Fase 4 (Provider System) — 2026-09-10

- [x] feat(providers: manager): ProviderManager com executar(registra latência/erros), estatisticicas, obter_healthcheck,nomes,saudaveis)
## v0.3.0 — Fase 3 (Orquestração de Agente) — 2026-09-10

- [x] `feat(orquestracao): roteador de providers)`: mapeia objetivo->provider por palavras-chave, alias e default (`NEXORA_PROVIDER_PADRAO`)。
- [x] `feat(orquestracao): orquestrador)`: ciclo Objetivo->Plano->Executor(provider roteado)->Verificador->Resultado; histórico de eventos; métricas（ total,ok,falhas）。
- [x] `feat(runtime): eventos)`: EventStore escreve JSONL（ integra `_registrar` do Orquestrador）。
- [x] `feat(cli: executar)`: subcomando `nexora executar "<objetivo>" [--provider alias]`；`info` e `--version` mantidos。
- [x] `test(orquestracao: roteador, orquestrador, cli)`: 8 novos testes（ 43 →51。
- [x] Correções: `Roteador.obter_provider` passa a instanciar a fábrica do registry； `Plano` registrado como evento no histórico； CLI test via subprocess com `PYTHONPATH`。


## v0.4.0 — Fase 4 (Provider System) — 2026-09-10

- [x] feat(providers: manager): ProviderManager com executar(registra latência/erros), estatisticas, obter_healthcheck, nomes, saudaveis)
- [x] feat(orquestracao: roteador): fallback automático por prioridade de saudáveis)( RuntimeError tipado quando nenhum saudável)

## Anteriores


- v0.2.0 — Fase 2(Providers & Conectores)— commit 901c2c8。
- v0.1.0 — Fase 1(Fundação)— commit e73a266。/ v0.0.1 — Fase 0.5(Decisão e Design)。