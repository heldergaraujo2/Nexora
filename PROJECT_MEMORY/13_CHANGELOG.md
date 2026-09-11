# 13 — CHANGELOG

## HEAD atual — Reconciliação pós-v1.0.0 — 2026-09-11

A tag `v1.0.0` permanece ancorada no commit `c49d3d2df314bb8c2d849c4466736f15841e8893`. O `main` continuou evoluindo e não deve ser tratado como congelado.

### Evolução arquitetural pós-release
Foram identificados 39 commits entre a Fase 16 e o HEAD `fc77446...`, cobrindo:
- inicialização/empacotamento final do namespace `nexora`;
- CI automatizado com matriz Python 3.11–3.14;
- Context Engine;
- Knowledge Engine;
- World Model Engine;
- Goal Engine;
- Strategy Engine;
- Communication Bus;
- integração do Agent Runtime com o bus;
- publicação do ciclo do Orchestrator no bus;
- serviço de delegação de tarefas;
- Agent Registry e Capability Registry;
- delegação baseada em capacidade;
- testes correspondentes.

### Correção de testes do CommunicationBus
- [x] Os testes de runtime e orquestração foram alinhados ao contrato existente do Bus: sem assinantes, mensagens permanecem `PENDENTE`; `ENTREGUE` ocorre quando há callback/entrega observada.
- [x] Nenhuma alteração de comportamento foi feita no CommunicationBus.

## v1.0.0 — Release — 2026-09-11

- Fase 16 — Long-Term Autonomy concluída no commit `c49d3d2...`.
- `MetaLongoPrazo` e `RegistroAutonomia` com persistência JSONL determinística.
- CLI `nexora autonomia definir|atualizar|listar|resumir`.
- Suite documentada naquele ponto: 128 testes passando.
- Tag `v1.0.0` criada em `c49d3d2...`.

## v0.16.0 — Fase 16 — Long-Term Autonomy

- [x] `autonomia/registro.py`: `MetaLongoPrazo` e `RegistroAutonomia`.
- [x] CLI de autonomia.
- [x] 6 novos testes: 122 → 128.

## v0.15.0 — Fase 15 — Portfolio Engine

- [x] `portfolio/registro.py`: `ItemPortfolio` e `RegistroPortfolio`.
- [x] CLI de portfolio.
- [x] 6 novos testes: 116 → 122.
