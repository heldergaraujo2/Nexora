# 13 — CHANGELOG

## Evolução multiagente e governança de execução — 2026-09-11

A tag `v1.0.0` permanece ancorada em `c49d3d2df314bb8c2d849c4466736f15841e8893`. O `main` continuou evoluindo sem criar uma nova fase.

### Execução delegada
- [x] `ExecutorDelegacoes` introduz a camada explícita de execução das delegações recebidas pelo CommunicationBus.
- [x] Integração opcional com `AgenteRuntime`, preservando o ciclo existente de execução, verificação, análise, correção e reteste.
- [x] Recovery no nível da delegação com `max_tentativas` e contador de tentativas.

### Experiência e auditoria
- [x] Resultados terminais de delegação podem ser registrados no `RegistroExperiencias`.
- [x] `RegistroAuditoria` fornece log append-only em JSONL.
- [x] Executor registra eventos de aceite, conclusão e falha, incluindo tentativas e erro.

### Policy / Governança
- [x] `src/nexora/governanca/policy.py` introduz `PolicyEngine` mínimo.
- [x] Regras suportam ALLOW/DENY, filtros por solicitante/executor/tarefa, ordem determinística e default DENY.
- [x] `ExecutorDelegacoes` consulta a política antes da execução.
- [x] A decisão de política é auditada com efeito, permitido e motivo.
- [x] DENY impede a execução do handler e encerra a delegação como `FALHOU`, pois o enum atual ainda não possui estado `DENEGADA`.
- [ ] Loader declarativo TOML/YAML ainda não implementado; ADR-009 permanece como referência arquitetural para essa evolução.

### Correção de empacotamento
- [x] Criado/exportado `src/nexora/experiencia/__init__.py`, corrigindo a importação do registro de experiências no CI.

### Validação
- [x] CI final verde no workflow `34647078404` para Python 3.11, 3.12, 3.13 e 3.14.

## Reconciliação pós-v1.0.0 — 2026-09-11

Foram identificados e reconciliados os componentes arquiteturais pós-release anteriores a esta etapa:
- Context Engine;
- Knowledge Engine;
- World Model Engine;
- Goal Engine;
- Strategy Engine;
- Communication Bus;
- integração de Agent Runtime e Orchestrator com comunicação;
- DelegadorAgentes;
- Agent Registry / Capability Registry;
- delegação por capacidade;
- testes correspondentes.

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
