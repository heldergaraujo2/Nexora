# 08 — CURRENT STATE

## Fase Atual

**Fase 6 — Coding Agent** — **CONCLUÍDA e PUSHADA**: `src/nexora/agentes/coding.py` — CodingAgent wraps do AgenteRuntime com prompt de engenharia e verificador de sintaxe; CLI `nexora agente codar "<tarefa>" [--linguagem L] [--provider P]`; teste de regressão do `nexora executar`; 74 testes unitários passando.

**Status:** Fase 6 CONCLUÍDA. Próxima: **Fase 7 — Research Engine** conforme 10_MODULES.md e roadmap, aguardando comando em NEXT_COMMAND.md.

**Histórico:** Fase 0/0.5/1/2/3/4/5/6 concluídas; 74 testes unitários passando (30 base,13 providers,5 orquestracao,3 ajustes,7 fase4,11 fase5,5 fase6).


## Concluído nesta fase

- [x] src/nexora/agentes/coding.py — CodingAgent(provider, registrar, max_tentativas): wrap do AgenteRuntime com _executar(provider.generate), _verificar(texto_nao_vazio + compile Python se parecer código), _analisar(enriquece erro de sintaxe), codar(monta prompt de engenharia por linguagem).
- [x] src/nexora/agentes/__init__.py — export CodingAgent.
- [x] src/nexora/cli.py — subcomando `nexora agente codar "<tarefa>" [--linguagem] [--provider]`; `executar` mantido e f-strings corrigidas.
- [x] tests/unit/test_agentes_coding.py — 4 novos testes( geração válida, correção de sintaxe, limite de tentativas, CLI codar.
- [x] tests/unit/test_orquestracao_cli.py — +1 teste de regressão do `executar`.
- [x] 74 testes verdes: python3 -m pytest tests/ -q


## Pendente

- [ ] Fase 7 — Research Engine( conforme 10_MODULES.md e NEXT_COMMAND.md.
- [ ] Fases 8–14 + WORKSPACE COMPLETO( conforme 10_MODULES.md e aprovação em lote do analista.

