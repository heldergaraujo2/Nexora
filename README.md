# NEXORA

> "Encontre oportunidades. Crie valor. Gere recursos."

## North Star

> "Construir uma inteligência artificial capaz de aprender continuamente sobre o mundo, identificar oportunidades, criar valor através de produtos, serviços, software e inovação, transformar esse valor em recursos de forma legal e sustentável, e utilizar esses recursos para ampliar continuamente sua própria capacidade de criar ainda mais valor para seu criador."

**Versão curta:** "Criar valor continuamente para ampliar continuamente a capacidade de criar valor."

## O que é a NEXORA?

NEXORA é uma plataforma de inteligência e agentes autônomos. Não é apenas um modelo de IA — o modelo é apenas uma parte do sistema. NEXORA é o sistema completo: inteligência, providers, memória, conhecimento, experiência, planejamento, agentes, ferramentas, execução, observação, verificação, pesquisa, experimentação, produtos, economia, métricas, evolução e continuidade.o

, 

## Estrutura do Projeto

```
PROJECT/
├── src/                    Código fonte( ainda vazio — Fase 1+)
├── tests/                  Testes( ainda vazio)
├── docs/                   Documentação( ADRs,contratos,design…)
├── NEXT_COMMAND.md         Canal de comando da coordenação( comando atual da Fase  0.5)
└── PROJECT_MEMORY/         Memória e continuidade do projeto(numeração canônica 00–15)
    ├── 00_IDENTITY.md
    ├── 01_NORTH_STAR.md
    ├── 02_CAPABILITY_DISCOVERY.md
    ├── 03_CAPABILITY_MATRIX.md
    ├── 04_ARCHITECTURE_REQUIREMENTS.md
    ├── 05_DISCOVERY_HANDOFF.md
    ├── 06_ARCHITECTURE.md
    ├── 07_ROADMAP.md
    ├── 08_CURRENT_STATE.md
    ├── 09_DECISIONS.md
    ├── 10_MODULES.md
    ├── 11_TASKS.md
    ├── 12_TESTS.md
    ├── 13_CHANGELOG.md
    ├── 14_AGENT_PROTOCOL.md
    └── 15_HANDOFF.md
```

## Estado Atual

- **Fase:** 0.5 — Decisão e Design( sem código:ADRs,contratos,estrutura proposta)
- **Antecedente:** Capability Discovery concluída(60+ capacidades,13 categorias)e integrada
- **Versão:**  v0.0.2
- **Sistema de continuidade:** O projeto é sua própria fonte de verdade. **GitHub = SOURCE OF TRUTH.** Novos agentes devem ler `PROJECT_MEMORY/15_HANDOFF.md` primeiramente,e executar o comando atual em `NEXT_COMMAND.md`.

## Fluxo de Coordenação

| Papel | Ator | Função |
|-------|-----|--------|
| Coordenador/Arquiteto | Arena Agent central( eu) | Audita estado,valida decisões,redige comandos(em `NEXT_COMMAND.md`),revisa resultados |
| Executor | Arena Agent construсor(OpenHands | Executa o comando atual de `NEXT_COMMAND.md`,atualiza `15_HANDOFF.md`,commita |
| Criador | Você | Decisões finais,aprovações de etapas,gates de ações sensíveis |

## Segurança e Governança

- Legalidade,transparência,autorização,rastreabilidade e auditoria.
- Ações sensíveis exigem autorização explícita do criador( inclui decisões legais/contratuais — invariante)。
- NEXORA nunca deve afirmar que um produto possui capacidade que ele não possui(Regra de Veracidade)。