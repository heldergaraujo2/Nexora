# 12 — TESTS

## Política de Testes

- Testar antes de concluir qualquer tarefa.
- Registrar o último teste e seu resultado no PROJECT_MEMORY.


## Estado dos Testes

| Teste | Escopo | Resultado |
|--------|--------|-----------|
| Fase 1 (unit) | core+providers+tools+config+runtime | 30 passed( 2026-09-10) |
| Fase 2 (unit) | providers tipados+registry+groq |43 passed( 2026-09-10) |
| Fase 3 (unit) |orquestracao(roteador,orquestrador,CLI)+ suite completa |51 passed( 2026-09-10) |
| Fase 4 (unit)| Provider System: ProviderManager + fallback do Roteador |58 passed( 2026-09-10) |
| Fase 5 (unit)| runtime do agente: observacao,analise,correcao,agente |69 passed( 2026-09-10) |
| Fase 6 (unit)| Coding Agent: CodingAgent + CLI agente codar + regressao executar |74 passed( 2026-09-10) |
| Fase 7 (unit)| Research Engine: ResearchAgent + CLI agente pesquisar + ferramenta fake buscar |79 passed( 2026-09-10) |


## Último Teste

- **Data:**itude 2026-09-10
- **Escopo:** Suíte completa após Fase  7 (Research Engine.
- **Resultado:** 79 passed,0 falhas; CLI `nexora executar`, `nexora agente codar` e `nexora agente pesquisar` validados com exit 0.


## Regra

Nao avançar para a próxima fase sem testes passando.

