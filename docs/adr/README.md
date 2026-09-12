# Architecture Decision Records (ADR)

> Registro formal das decisoes arquiteturais da NEXORA, seguindo o padrao ADR (contexto, decisao, consequencias). Toda ADR pode ser revisitada; novas ADRs devem ser adicionadas numeradas sequencialmente.

| ADR | Decisao | Status |
|-----|---------|--------|
| ADR-001 | Linguagem e ecossistema: Python | Aprovada |
| ADR-002 | Estrutura e namespace: src/nexora/ | Aprovada |
| ADR-003 | Interface de entrada do MVP: CLI primaria | Aprovada |
| ADR-004 | Backend inicial de memoria: JSON versionado | Aprovada |
| ADR-005 | Backend do event store: append-only JSON | Aprovada |
| ADR-006 | Provider Groq: validar tool-calling antes de fixar | Aprovada (condicional) |
| ADR-007 | Sandbox do MVP: subprocesso isolado | Aprovada |
| ADR-008 | Angulo do MVP: Codificacao | Aprovada |
| ADR-009 | Politica: config declarativo versionado (TOML/YAML) | Aprovada |
| ADR-010 | Multi-agente no MVP: nao | Aprovada |
| ADR-011 | Observabilidade: logs estruturados JSON rotativos | Aprovada |
| ADR-012 | Orchestrator coordena; AgentRuntime executa | Aprovada |
| ADR-013 | Ciclo legado mantido como compatibilidade ate migracao segura | Aprovada |
| ADR-014 | Idempotencia para efeitos externos | Aprovada |
| ADR-015 | Provider local Ollama | Aprovada |

### Nota sobre ADR-006
ADR-006 permanece condicional: exige validacao real da API do Groq antes de fixar modelo/tool-calling como capacidade de producao.
