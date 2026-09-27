# NEXORA — ECOSYSTEM HARVEST / OPEN-SOURCE INTEGRATION
## 2026-09-27

Este documento registra a auditoria de ecossistema e as decisões de engenharia resultantes.
A regra é **REPLICAR / ADAPTAR / SUPERAR / CRIAR**, não transformar a NEXORA em wrapper de outro produto.

## Fontes e uso arquitetural

| Projeto | Área | Decisão NEXORA |
|---|---|---|
| Graphiti | knowledge graph temporal | ADAPTAR conceitos temporais |
| AgentMemory | retrieval híbrido | ADAPTAR RRF + lexical/vector/graph |
| Letta | estado/memória de agente | ADAPTAR conceitos |
| LangGraph | execução durável | ADAPTAR persistência de checkpoint |
| PydanticAI | retry/durable execution | ADAPTAR taxonomia de retry |
| Microsoft Agent Governance Toolkit | governance/security | AUDITAR/ADAPTAR padrões |
| MCP | interoperabilidade | ADAPTAR contratos; execução continua no Registry |
| Research Agent | pesquisa/citações/guardrails | ADAPTAR orçamento e segurança |
| AgentSynth | verificação por estado/resultado | ADAPTAR filosofia de outcome verification |
| A-Evolve | evolução | ADAPTAR avaliação de candidatos |
| Self-Improving Agent | gate mensurável | ADAPTAR acceptance gate |
| Dream Cycle | melhoria contínua | ADAPTAR ciclo de hipóteses |
| OpenSandbox | isolamento | ADAPTAR como backend futuro |
| browser-use | browser automation | ADAPTAR como capability adapter futuro |
| SWE-agent | coding loop | ADAPTAR padrões de coding agent |
| LiteLLM Router | routing/fallback/health | ADAPTAR conceitos já existentes no ProviderManager |
| OpenTelemetry GenAI | observabilidade | ADAPTAR nomenclatura e spans |
| OpenAI Agents SDK | handoffs/guardrails/tracing | REFERÊNCIA arquitetural |
| Agent Economy | economia multiagente | ADAPTAR conceitos para Opportunity/Economy |
| economia de agentes — estudos experimentais | economia | REFERÊNCIA empírica, não premissa de receita |

## Implementações incorporadas nesta rodada

### Memory
- `src/nexora/memoria/hibrida.py`
- BM25-like lexical ranking determinístico.
- hooks opcionais semantic/graph.
- Reciprocal Rank Fusion.
- decay temporal configurável.
- contrato de memória independente de fornecedor.

### World Model
- `src/nexora/world/grafo_temporal.py`
- entidades.
- fatos temporais.
- validade desde/até.
- consultas as-of.
- encerramento de fatos.
- fonte/metadados.

### Runtime
- `src/nexora/runtime/retry.py`
- tipos de retry.
- limite de tentativas.
- autorização/precondições.
- bloqueio de retry de efeito externo não idempotente.
- AgentRuntime usa RetryPolicy.

### Checkpoint
- `src/nexora/runtime/checkpoint.py`
- persistência JSON opcional.
- schema versionado.
- escrita atômica.
- reload entre processos/restarts.
- recuperação continua sendo restauração lógica, não rollback de efeito externo.

### Sandbox
- `src/nexora/runtime/sandbox_backend.py`
- contrato de backend.
- subprocesso local como backend padrão.
- adapter Docker fail-closed para futura implementação explícita.
- Sandbox existente agora aceita backend intercambiável.

### MCP
- `src/nexora/integracoes/mcp.py`
- contratos Tool/Resource/Prompt.
- `mcp_adapter.py` importa Tools para o Registry.
- execução MCP passa pela fronteira governada do Tool Registry quando integrada à NEXORA.

### Research
- `src/nexora/agentes/pesquisa_guardrails.py`
- orçamento de consultas/fontes/domínios.
- bloqueio de localhost, loopback, private/link-local/reserved IPs.
- ResearchAgent aplica o orçamento e filtra fontes antes do contexto.

### Observabilidade
- `src/nexora/observabilidade/genai.py`
- spans GenAI.
- eventos.
- duração.
- erros.
- exporter opcional.
- AgentRuntime emite span por tentativa quando tracer é fornecido.

### Evolution
- `src/nexora/evolucao/engine.py`
- candidatos.
- hipótese.
- mudança.
- rollback.
- avaliação.
- gate de melhoria.
- rejeição por regressão/risco/evidência insuficiente.
- `dream_cycle.py` coordena observação → hipótese → experimento → gate.

### Economy
- `src/nexora/economia/oportunidades.py`
- valor esperado.
- risco.
- custo.
- receita.
- mercado.
- score determinístico.
- `loop.py` implementa estados descoberta → protótipo → validação → lançamento → medição → melhoria → receita → reinvestimento.
- Não executa transações financeiras automaticamente.

## Licenciamento e proveniência

Esta rodada implementa contratos e algoritmos originais da NEXORA inspirados em padrões públicos.
Não foram copiados trechos proprietários de código de terceiros.

Antes de incorporar qualquer código externo diretamente:
1. confirmar licença do repositório;
2. verificar licença de dependências;
3. preservar notices quando exigidos;
4. registrar origem;
5. preferir implementação original quando a ideia for simples;
6. isolar código externo em adapter quando a dependência for realmente necessária.

## Limitações deliberadas

- Não há vetor database obrigatório.
- Não há dependência obrigatória de Graphiti/LangGraph/Letta/OpenSandbox/etc.
- Não há execução Docker automática.
- Não há transporte MCP de rede implementado neste núcleo.
- Não há prova semântica automática de verdade.
- Não há transação financeira real.
- Evolução não altera código de produção automaticamente.
- Browser automation e SWE-agent continuam como adapters/capabilities futuras.
- OpenTelemetry externo pode ser conectado por exporter sem tornar SDK externo obrigatório.

## Próximos incrementos

1. Integrar World Model e Memory Híbrida ao Context/Knowledge real.
2. Evoluir Checkpoint para backend compartilhado/distribuído.
3. Integrar outcome verification ao resultado real das ferramentas.
4. Criar ProviderRouter com health/cost/capability/quality em um contrato único.
5. Criar adapters reais opcionais para MCP/OpenSandbox/browser.
6. Criar benchmark de evolução e regression gate.
7. Fechar Product Engine → Market → Revenue → Reinvestment com aprovação humana e métricas reais.
