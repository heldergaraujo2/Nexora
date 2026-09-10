# 06 — ARQUITETURA

## Princípio Fundamental

NEXORA ≠ modelo de IA. O modelo fornece capacidade cognitiva. NEXORA fornece o sistema completo.

## Composição

- Inteligência
- Providers
- Memória
- Conhecimento
- Experiência
- Planejamento
- Agentes
- Ferramentas
- Execução
- Observação
- Verificação
- Pesquisa
- Experimentação
- Produtos
- Economia
- Métricas
- Evolução
- Continuidade

## Visão de Alto Nível

```
NEXORA
   │
   ├── INTELLIGENCE  (Local AI / Online AI)
   └── RUNTIME       (Tools: WEB, CODE, FILES...)
```

## Provider System (Fase 2)

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

Groq será oficialmente suportado (acesso à API existente), porém NEXORA NÃO deve depender exclusivamente da Groq. Providers são responsáveis pela INTELIGÊNCIA — não pela execução física do computador.



## Multi-Agent (Fase 4.5)

NEXORA Orchestrator coordena agentes especializados: Coding, Research, Market Intelligence, Product, Pricing, Marketing, Sales/Distribution, Analytics, Experimentation, Evolution e Resource. O Orchestrator interpreta objetivos, divide problemas, escolhe agentes, distribui tarefas, controla dependências, verifica resultados e registra experiência.

.

 O Agent Registry mantém registro de todos os agentes (nome, função, capacidades, limitações, provider preferencial, ferramentas permitidas, custo, desempenho, histórico, métricas, versão, estado e permissões).

 

## Fases

| Fase | Escopo |
|------|--------|
| Prévia | Capability Discovery |
| 0 | Continuidade e Memória |
| 1 | Fundação |
| 2 | Provider System |
| 3 | Contexto e Memória |
| 4 | Planejamento |
| 4.5 | Multi-Agent Orchestration |
| 5 | NEXORA Agent Runtime |
| 6 | Coding Agent |
| 7 | Research Engine |
| 8 | Experience Engine |
| 9 | Experimentation Engine |
| 10 | Evolution Engine |
| 11 | Economic Engine |
| 12 | Resource Management |
| 13 | Portfolio Engine |
| 14 | Long-Term Autonomy |