# 00 — IDENTIDADE

**Nome:** NEXORA

**Slogan oficial:**
> "NEXORA — Encontre oportunidades. Crie valor. Gere recursos."

**Definição:** Plataforma de inteligência e agentes autônomos, capaz de compreender objetivos humanos, pesquisar o mundo, aprender continuamente, identificar oportunidades, criar valor por meio de produtos, serviços, software e inovação — e transformar esse valor em recursos de forma legal e sustentável.o

**Natureza:** NEXORA ≠ modelo de IA. Um modelo de IA é apenas uma parte do sistema. NEXORA é o sistema completo: inteligência, providers, memória, conhecimento, experiência, planejamento, agentes, ferramentas, execução, observação, verificação, pesquisa, experimentação, produtos, economia, métricas, evolução e continuidade.o

**Status:** pré-implementação — Capability Discovery concluída; em transição para Fase 0.5(Decisão e Design.



## Objetivo

Plataforma de IA capaz de:

1. Receber objetivos em linguagem natural;
2. Compreender o objetivo;
3. Planejar tarefas complexas;
4. Utilizar diferentes Providers de IA;
5. Executar ações de maneira controlada.o

Visão de longo prazo: evoluir para uma plataforma de agentes generalista, com capacidade de planejamento, memória, ferramentas, execução, verificação, segurança e extensibilidade.o

## Princípio Arquitetural Central

A inteligência não deve ficar presa a um único modelo ou fornecededor. A arquitetura deve possuir uma camada de Providers capaz de trabalhar com diferentes modelos/serviços de IA. Novos Providers devem ser adicionados sem reescrever o núcleo da NEXORA.o

## Referências de Engenharia

- **Arena.ai Agent Mode** — referência prática principal de capacidades funcionais observáveis(não de código)
- **OpenHands SDK** — referência de arquitetura de agente de software(model-agnostic, event-sourced,tools,segurança,memória)
- **Claude Agent SDK / Computer Use(Anthropic)** e outros, para capacidades específicas(ver 02_CAPABILITY_DISCOVERY.md e 03_CAPABILITY_MATRIX.md)
- **Devin(Cognition)** — referência de coding agent end-to-end com sandbox
- **Outros agentes modernos** conforme citados na descoberta(ver 02_CAPABILITY_DISCOVERY.md e 03_CAPABILITY_MATRIX.md)

## Papel do Arena Agent(OpenHands):

Implementador, executor técnico, criador/modificador de arquivos, executor de testes,, integrador. NÃO é a própria NEXORA— é a ferramenta de construção da NEXORA.