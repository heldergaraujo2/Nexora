# 13 — CHANGELOG

## Evolução multiagente e governança de execução — 2026-09-11

A tag `v1.0.0` permanece ancorada em `c49d3d2df314bb8c2d849c4466736f15841e8893`. O `main` continuou evoluindo sem criar uma nova fase.

### Execução delegada
- [x] `ExecutorDelegacoes` introduz a camada explícita de execução das delegações recebidas pelo CommunicationBus.
- [x] Integração opcional com `AgenteRuntime`, preservando execução, verificação, análise, correção e reteste.
- [x] Recovery no nível da delegação com `max_tentativas`.

### Experiência e auditoria
- [x] Resultados terminais podem ser registrados no `RegistroExperiencias`.
- [x] `RegistroAuditoria` fornece log append-only em JSONL.
- [x] Executor registra aceite, conclusão e falha.

### Policy / Governança
- [x] `PolicyEngine` mínimo com ALLOW/DENY, filtros, ordem determinística e default DENY.
- [x] Executor consulta a política antes da execução.
- [x] Decisão auditada com efeito, permitido, motivo, versão, origem e fingerprint.
- [x] Loader declarativo TOML versão 2 com schema estrito e IDs únicos.
- [x] Fingerprint canônico SHA-256 da semântica da política.
- [x] `DENEGADA` separa negação de governança de falha de execução.
- [x] `GerenciadorPermissoes` / `PedidoPermissao` estabelecem uma fronteira explícita de autorização sem executar a ação.
- [x] `GerenciadorPolitica` implementa reload validado e troca atômica, preservando a política anterior quando a nova é rejeitada.
- [x] Registry de ferramentas pode exigir permissão antes do executor, preservando compatibilidade sem governança configurada.
- [x] Sandbox mantém allowlist e pode exigir Policy antes de `subprocess.run`; DENY impede a execução.
- [x] Contexto de auditoria do Sandbox registra somente o comando-base, evitando copiar argumentos potencialmente sensíveis.
- [ ] YAML ainda não implementado.

### Correção de empacotamento
- [x] Criado/exportado `src/nexora/experiencia/__init__.py`, corrigindo importação no CI.

### Validação
- [x] CI histórico `34653209175` verde para Python 3.11–3.14 no HEAD `dec0bbd4430bbe5883476112704ea78c97b90be3`.
- [ ] CI do HEAD atual `8745681cb21a71690a2360f0b7851ca2d3e50027` ainda não retornou workflow associado e não deve ser marcado como verde.
- [x] Testes adicionados para permission boundary, policy lifecycle, tool governance e Sandbox governance.

## Reconciliação pós-v1.0.0 — 2026-09-11

Foram identificados e reconciliados os componentes arquiteturais pós-release anteriores a esta etapa: Context, Knowledge, World Model, Goal, Strategy, Communication Bus, Runtime/Orchestrator, Delegation, Agent Registry, capability delegation e testes correspondentes.

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
