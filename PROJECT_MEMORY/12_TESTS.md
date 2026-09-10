# 12 — TESTS

## Política de Testes

- Testar antes de concluir qualquer tarefa.
- Registrar o último teste e seu resultado no PROJECT_MEMORY.



## Estado dos Testes

| Teste | Escopo | Resultado |
|--------|--------|-----------|
| Fase 1 (unit) | core+providers+tools+config+runtime | 30 passed (`python3 -m pytest tests/ -q`, 2026-09-10) |
| Fase 2 (unit) | providers tipados+registry+groq | 43 passed ( 2026-09-10) |
| Fase 3 (unit) | orquestração(roteador, orquestrador, CLI)+ suite completa | 51 passed em 0.26s( 2026-09-10) |



## Último Teste

- **Data:** 2026-09-10
- **Escopo:** Suíte completa após Fase 3（ CLIs `info` e `executar` validados manualmente com `sucesso=True etapas=1`
- **Resultado:** 51 passed, 0 falhas；CLI `nexora executar "teste rapido" --provider fake` → `sucesso=True etapas=1`.



## Regra

Não avançar para a próxima fase sem testes passando.