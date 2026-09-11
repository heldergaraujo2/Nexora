# 10 — MODULES

## Módulos e estado real

| Módulo | Localização principal | Estado |
|---------|------------------------|--------|
| Core | `src/nexora/core/` | Implementado |
| Configuration | `src/nexora/config/` | Implementado |
| Providers / ProviderManager | `src/nexora/providers/` | Implementado, incluindo Groq |
| Tools Registry | `src/nexora/tools/registry.py` | Implementado |
| Runtime | `src/nexora/runtime/` | Implementado |
| Orchestrator | `src/nexora/orquestracao/orquestrador.py` | Implementado |
| Coding Agent | `src/nexora/agentes/coding.py` | Implementado |
| Research Agent | `src/nexora/agentes/pesquisa.py` | Implementado |
| Context | `src/nexora/contexto/` | MVP implementado |
| Knowledge | `src/nexora/conhecimento/` | MVP implementado |
| World Model | `src/nexora/mundo/` | MVP implementado |
| Goals | `src/nexora/objetivos/` | MVP implementado |
| Strategy | `src/nexora/estrategias/` | MVP implementado |
| Memory | `src/nexora/memoria/` | Implementado |
| Communication Bus | `src/nexora/comunicacao/bus.py` | Infraestrutura implementada |
| Delegation | `src/nexora/comunicacao/delegacao.py` | Infraestrutura implementada |
| Agent Registry | `src/nexora/agentes/registro.py` | Implementado em memória |
| Capability Registry / Discovery | `AgenteRegistro` + `RegistroAgentes` | Implementado em memória |
| Capability Delegation | `DelegadorAgentes.delegar_por_capacidade()` | Implementado como seleção + mensagem |
| Autonomy | `src/nexora/autonomia/` | Fase 16 concluída |
| Security | `src/nexora/seguranca/` | Implementado historicamente |
| Economy | `src/nexora/economia/` | Implementado historicamente |
| Resources | `src/nexora/recursos/` | Implementado historicamente |
| Portfolio | `src/nexora/portfolio/` | Implementado historicamente |

## Estado dos componentes de agentes
O registry, capability discovery e delegation são atualmente infraestrutura de coordenação. Ainda não existe um ciclo automático completo que selecione um agente, execute a tarefa, verifique o entregável, atualize estado/memória e recupere falhas sem intervenção explícita.

## Princípio
Não recriar módulos existentes. Antes de implementar algo novo:
1. procurar no código;
2. procurar nos testes;
3. procurar no PROJECT_MEMORY;
4. verificar contratos e limites arquiteturais.

## Diretórios

```
PROJECT/
├── src/                 código fonte
├── tests/               testes
├── docs/                documentação e ADRs
└── PROJECT_MEMORY/      memória e continuidade
```
