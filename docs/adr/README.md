# Architecture Decision Records (ADR)

> Registro formal das decisoes arquiteturais da NEXORA, seguindo o padrao ADR( contexto, decisao, consequencias ). Numeracao sequencial ADR-001 .. ADR-011, correspondendo as decisoes P1-P11 de `PROJECT_MEMORY/09_DECISIONS.md`. Fase 0.5 — Decisao e Design( sem codigo de producao )。

| ADR | Decisao | Status |
|-----|---------|--------|
| ADR-001 | Linguagem e ecossistema: Python | Aprovada( Fase 0.5 ) |
| ADR-002 | Estrutura e namespace: src/nexora/ | Aprovada( Fase 0.5 ) |
| ADR-003 | Interface de entrada do MVP: CLI primaria | Aprovada( Fase  0.5 ) |
| ADR-004 | Backend inicial de memoria: JSON versionado | Aprovada( Fase  0.5 ) |
| ADR-005 | Backend do event store: append-only JSON | Aprovada( Fase  0.5 ) |
| ADR-006 | Provider Groq: validar tool-calling antes de fixar | Aprovada( condicional ) |
| ADR-007 | Sandbox do MVP: subprocesso isolado | Aprovada( Fase  0.5 ) |
| ADR-008 | Angulo do MVP: Codificacao | Aprovada( Fase  0.5 ) |
| ADR-009 | Politica: config declarativo versionado( TOML/YAML ) | Aprovada( Fase  0.5 ) |
| ADR-010 | Multi-agente no MVP: nao | Aprovada( Fase  0.5 ) |
| ADR-011 | Observabilidade: logs estruturados JSON rotativos | Aprovada( Fase  0.5 ) |

> Nota: ADR-006 e condicional — exige validacao real da API do Groq antes de fixar o modelo.
> Toda ADR pode ser revisitada;novas ADRs devem ser adicionadas numeradas sequencialmente.