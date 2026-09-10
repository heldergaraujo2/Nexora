# NEXORA — Identidade

## Identidade

- **Nome:** NEXORA
- **Slogan:** "NEXORA — Encontre oportunidades. Crie valor. Gere recursos."
- **Natureza:** Plataforma de agentes de IA
- **Status:** pré-implementação
- **Fase:** Capability Discovery (Fase prévia ao roadmap)
- **Repositório:** `/workspace/project` (greenfield, git inicializado sem commits)

## Objetivo

Plataforma de agentes de IA capaz de:
1. Receber objetivos em linguagem natural;
2. Compreender o objetivo;
3. Planejar tarefas complexas;
4. Utilizar diferentes Providers de IA;
5. Executar ações de maneira controlada.

 Visão de longo prazo: evoluir para uma plataforma de agentes generalista, com capacidade de planejamento, memória, ferramentas, execução, verificação, segurança e extensibilidade.



## Princípio arquitetural central

A inteligência não deve ficar presa a um único modelo ou fornecedor. A arquitetura deve possuir uma camada de Providers capaz de trabalhar com diferentes modelos/serviços de IA. Novos Providers devem ser adicionados sem reescrever o núcleo da Nexora.



## Referências de engenharia

- **Arena.ai Agent Mode** — referência prática principal de capacidades funcionais observáveis (não de código)
- **OpenHands SDK** — referência de arquitetura de agente de software (model-agnostic, event-sourced, tools, segurança, memória
- **Claude Agent SDK / Computer Use (Anthropic)e outros para capacidades específicas (ver 02_CAPABILITY_DISCOVERY.mde 03_CAPABILITY_MATRIX.md)
- **Devin (Cognition)** — referência de coding agent end-to-end com sandbox
- **Outros agentes modernos** conforme citados na descoberta (ver 02_CAPABILITY_DISCOVERY.md e 03_CAPABILITY_MATRIX.md)