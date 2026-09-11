# 07 — ROADMAP

## Roadmap Global — histórico canônico

```
FASE PRÉVIA · CAPABILITY DISCOVERY · CONCLUÍDA
FASE ZERO   · CONTINUIDADE E MEMÓRIA · CONCLUÍDA
FASE UM     · FUNDAÇÃO · CONCLUÍDA
FASE DOIS   · PROVIDER SYSTEM · CONCLUÍDA
FASE TRÊS   · CONTEXTO E MEMÓRIA · CONCLUÍDA
FASE QUATRO · PLANEJAMENTO · CONCLUÍDA
FASE 4.5    · MULTI-AGENT ORCHESTRATION · CONCLUÍDA
FASE CINCO  · NEXORA AGENT RUNTIME · CONCLUÍDA
FASE SEIS   · CODING AGENT · CONCLUÍDA
FASE SETE   · RESEARCH ENGINE · CONCLUÍDA
FASE OITO   · EXPERIENCE ENGINE · CONCLUÍDA
FASE NOVE   · EXPERIMENTATION ENGINE · CONCLUÍDA
FASE DEZ    · EVOLUTION ENGINE · CONCLUÍDA
FASE ONZE   · ECONOMIC ENGINE · CONCLUÍDA
FASE DOZE   · SECURITY ENGINE · CONCLUÍDA
FASE TREZE  · MEMORY ENGINE · CONCLUÍDA
FASE QUATORZE · RESOURCE MANAGEMENT · CONCLUÍDA
FASE QUINZE · PORTFOLIO ENGINE · CONCLUÍDA
FASE DEZESSEIS · LONG-TERM AUTONOMY · CONCLUÍDA
```

## Reconciliação de numeração
A numeração acima é a canônica operacional baseada nos commits reais das fases 11–16:
- Fase 11: Economic Engine (`b1d2887...`)
- Fase 12: Security Engine (`14b5a8c...`)
- Fase 13: Memory Engine (`9b2a2bf...`)
- Fase 14: Resource Management (`1654e15...`)
- Fase 15: Portfolio Engine (`5c26443...`)
- Fase 16: Long-Term Autonomy (`c49d3d2...`, tag `v1.0.0`)

A referência antiga que chamava Long-Term Autonomy de Fase 14 estava dessincronizada com a implementação real.

## Evolução pós-v1.0.0
O roadmap histórico foi concluído, mas o código continuou evoluindo após a tag v1.0.0. Não classificar automaticamente essa evolução como nova fase.

Foram implementados:
- Context Engine;
- Knowledge Engine;
- World Model Engine;
- Goal Engine;
- Strategy Engine;
- Communication Bus;
- integração de Runtime e Orchestrator com comunicação;
- DelegadorAgentes;
- Agent Registry / Capability Registry;
- delegação por capacidade;
- testes e CI automatizado.

## Estado atual
**Roadmap histórico concluído; arquitetura em evolução pós-release; nenhuma nova fase formalizada.**

A evolução atual deve ser tratada como trabalho arquitetural incremental até que o coordenador, com base em evidências, defina uma nova fase ou mantenha a evolução transversal.

## Próxima ação do coordenador
1. Confirmar CI verde no HEAD.
2. Consolidar a arquitetura de agentes/capacidades/delegação.
3. Definir explicitamente o próximo incremento antes de iniciar nova implementação.
