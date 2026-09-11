# 06 — ARQUITETURA

## Princípio Fundamental
NEXORA ≠ modelo de IA. O modelo fornece capacidade cognitiva. NEXORA fornece o sistema completo.

## Composição

- Inteligência
- Providers
- Memória
- Conhecimento
- Contexto
- World Model
- Objetivos
- Estratégias
- Experiência
- Planejamento
- Agentes
- Comunicação
- Capacidades
- Ferramentas
- Execução
- Observação
- Verificação
- Recuperação
- Pesquisa
- Experimentação
- Produtos
- Economia
- Métricas
- Evolução
- Continuidade
- Governança

## Provider System

NEXORA deve possuir arquitetura independente de modelos:

```
NEXORA
   │
   ▼
ProviderManager
   ├── LocalProvider
   ├── GroqProvider
   ├── OnlineProvider
   └── CodingProvider / Providers especializados
```

Groq é oficialmente suportado, mas NEXORA NÃO depende exclusivamente da Groq. Providers fornecem inteligência; execução física permanece nas camadas apropriadas de runtime/tools/policy.

## Multi-Agent e Agent Registry

O Orchestrator coordena objetivos e tarefas. A arquitetura atual possui um registry próprio para agentes e capacidades:

```
Agent Registry
   ├── agente
   ├── capacidades
   ├── tags
   ├── prioridade
   ├── disponibilidade
   └── metadados
          │
          ▼
Capability Discovery
          │
          ▼
Capability Delegation
          │
          ▼
CommunicationBus
```

`RegistroAgentes` faz descoberta determinística e seleção por capacidade. `DelegadorAgentes` cria a delegação e correlaciona solicitação/resultado. O CommunicationBus apenas transporta/registra mensagens; não executa providers ou ferramentas.

## Limite atual

A infraestrutura acima ainda não constitui um ciclo multi-agente autônomo completo. A execução do agente executor, verificação do entregável, recuperação, atualização de memória e governança ainda precisam ser conectadas de forma explícita.

## Fases históricas canônicas

| Fase | Escopo | Estado |
|------|--------|--------|
| Prévia | Capability Discovery | Concluída |
| 0 | Continuidade e Memória | Concluída |
| 1 | Fundação | Concluída |
| 2 | Provider System | Concluída |
| 3 | Contexto e Memória | Concluída |
| 4 | Planejamento | Concluída |
| 4.5 | Multi-Agent Orchestration | Concluída |
| 5 | NEXORA Agent Runtime | Concluída |
| 6 | Coding Agent | Concluída |
| 7 | Research Engine | Concluída |
| 8 | Experience Engine | Concluída |
| 9 | Experimentation Engine | Concluída |
| 10 | Evolution Engine | Concluída |
| 11 | Economic Engine | Concluída |
| 12 | Security Engine | Concluída |
| 13 | Memory Engine | Concluída |
| 14 | Resource Management | Concluída |
| 15 | Portfolio Engine | Concluída |
| 16 | Long-Term Autonomy | Concluída |

A numeração acima foi reconciliada com os commits reais das fases 11–16. A evolução pós-v1.0.0 não foi convertida automaticamente em uma nova fase.

## Boundaries importantes

- Providers conhecem apenas o contrato do Provider.
- Runtime não conhece providers específicos.
- Registries são a porta de extensão de agentes/capacidades.
- CommunicationBus não executa efeitos externos.
- Delegação não deve bypassar policy, sandbox, checkpoint, auditoria ou verificação.
- Memória e conhecimento devem preservar provenance e governança conforme os requisitos arquiteturais.
