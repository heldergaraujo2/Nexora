# ADR-001 — Linguagem e ecossistema: Python

- Status: Aprovada (Fase 0.5)
- Data: 2026-09-10
- Decisao de origem: P1 (PROJECT_MEMORY/09_DECISIONS.md)
- Relacionamentos: ADR-002 (estrutura de repositorio), ADR-008 (angulo do MVP: codificacao)

## Contexto

A NEXORA precisa de uma linguagem e ecossistema para implementar o nucleo model-agnostico,memoria,eventos e tooling de agentes. As alternativas avaliadas foram Python,Node/TypeScript e hibrido. O ecossistema de IA/agentico e dominado por Python(maduro,com SDK de agentes,providers e ferramentas), mas Node/TS tem vantagens no ecossistema web.

).

## Decisao

Adotar **Python** como linguagem principal da plataforma, com ecossistema gerenciado por `uv`( ou `pip` como fallback,)e tipagem estatica gradual( via `mypy` ou similar quando viavel)。

## Consequencias

- Positivas: ecossistema de IA maduro( providers,SDK de agentes,ferramentas); integracao natural com Groq e demais providers; menor fricao para contratos de tools e memoria;
 curva de aprendizado ampla;
 testing com pytest consolidado。
- Negativas: desempenho de runtime para loops de alta frequencia pode exigir otimizacao futura( ex: Rust mas para subprocessos sandbox) ;distribuicao empacotada ( via PyInstaller ou similar,exige atencao no futuro);
- Neutras: Node/TS permanece viavel para ferramentas frontend/UI caso a plataforma exponha dashboards( fora do escopo do MVP)。