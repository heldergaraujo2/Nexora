# NEXORA

> "Encontre oportunidades. Crie valor. Gere recursos."

## North Star

> "Construir uma inteligência artificial capaz de aprender continuamente sobre o mundo, identificar oportunidades, criar valor através de produtos, serviços, software e inovação, transformar esse valor em recursos de forma legal e sustentável, e utilizar esses recursos para ampliar continuamente sua própria capacidade de criar ainda mais valor para seu criador."

**Versão curta:** "Criar valor continuamente para ampliar continuamente a capacidade de criar valor."

## O que é a NEXORA?

NEXORA é uma plataforma de inteligência e agentes autônomos. Não é apenas um modelo de IA — o modelo é apenas uma parte do sistema. NEXORA é o sistema completo: inteligência, providers, memória, conhecimento, contexto, world model, objetivos, estratégias, agentes, comunicação, capacidades, ferramentas, execução, observação, verificação, pesquisa, experimentação, produtos, economia, métricas, evolução, continuidade e governança.

## Estado atual

- **Release histórica:** `v1.0.0`, tag apontando para `c49d3d2...`.
- **Estado real:** o código continuou evoluindo após a release; `main` não está congelada.
- **Arquitetura pós-release:** Context, Knowledge, World Model, Goals, Strategy, Communication Bus, Agent Registry, Capability Registry e Capability Delegation já existem em diferentes níveis de MVP/infraestrutura.
- **Long-Term Autonomy:** concluída e preservada.
- **Próxima fase:** nenhuma formalizada. A próxima evolução depende de decisão explícita do coordenador.

## Estrutura do Projeto

```
PROJECT/
├── src/                    Código fonte
├── tests/                  Testes
├── docs/                   Documentação e ADRs
├── NEXT_COMMAND.md         Canal de comando da coordenação
└── PROJECT_MEMORY/         Memória e continuidade do projeto
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

## GitHub é a fonte de verdade

O código real deve sempre ser reconciliado com `PROJECT_MEMORY`. Em caso de divergência:

**GIT → AUDITORIA → DECISÃO → IMPLEMENTAÇÃO → TESTES → PROJECT_MEMORY → COMMIT → PUSH → HANDOFF**

## Arquitetura de agentes atual

- `RegistroAgentes` mantém agentes e capacidades em memória.
- Descoberta por capacidade é determinística e considera disponibilidade/prioridade.
- `CommunicationBus` transporta mensagens e eventos, sem executar providers ou ferramentas.
- `DelegadorAgentes` cria solicitações e resultados correlacionados.
- Runtime e Orchestrator publicam eventos de ciclo no Bus.
- A execução automática completa entre agentes ainda não está implementada.

## Fluxo de Coordenação

| Papel | Função |
|-------|--------|
| Coordenador/Arquiteto | Audita estado, valida decisões, define comandos e revisa resultados |
| Executor | Implementa alterações autorizadas, executa testes e atualiza continuidade |
| Criador | Decisões finais, aprovações de etapas e gates de ações sensíveis |

## Segurança e Governança

- Legalidade, transparência, autorização, rastreabilidade e auditoria.
- Ações sensíveis exigem autorização explícita do criador.
- NEXORA nunca deve afirmar que um produto possui capacidade que ele não possui.
