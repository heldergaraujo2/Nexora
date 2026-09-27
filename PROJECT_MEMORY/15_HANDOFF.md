# 15 — HANDOFF

> **ARQUIVO PRINCIPAL DE CONTINUIDADE DA NEXORA.** GitHub é a fonte de verdade. Antes de continuar, confirmar HEAD real de `main` e o CI correspondente.

## 1. Identidade imutável
- Nome: **NEXORA**.
- Slogan: **“NEXORA — Encontre oportunidades. Crie valor. Gere recursos.”**
- North Star curta: **“Criar valor continuamente para ampliar continuamente a capacidade de criar valor.”**
- NEXORA é uma plataforma, não apenas um modelo.
- Loop central: `OBSERVAR → PESQUISAR → ENTENDER → IDENTIFICAR OPORTUNIDADE → PLANEJAR → CRIAR → TESTAR → VALIDAR → LANÇAR → MEDIR → APRENDER → MELHORAR → GERAR RECURSOS → AMPLIAR CAPACIDADE → NOVA OPORTUNIDADE`.

## 2. Estado atual — 2026-09-12
- O caminho canônico é `Orchestrator → AgentRuntime → governança/provider/tool → Observation → Verification → Analysis → Correction/Recovery → Retest → Audit/Experience → Evaluation → ExecutionTrace → Result`.
- `AgentRuntime` continua sendo o único proprietário do ciclo avançado.
- `core/ciclo.py` continua legado/compatibilidade; **não remover ainda**.
- Idempotência continua barreira explícita antes de efeitos externos e não habilita retry automático.
- `ExecutionTrace` registra contexto de provider/modelo e telemetria real quando disponível.
- `ProviderManager` possui histórico persistente opcional por provider e por modelo, com tokens e custo real quando existe pricing exato.
- `RoteadorInteligente` usa confiabilidade/latência específicas de `provider + modelo` quando há amostra mínima e faz fallback controlado para histórico agregado.
- Custo histórico usa somente custo real medido.
- `AvaliadorResultado` fornece qualidade explícita baseada em critérios/evidências reais.
- `HistoricoAvaliacao` persiste qualidade por `provider + modelo + tipo_tarefa`.
- Qualidade influencia o roteamento somente com amostra mínima, pelo menos dois candidatos comparáveis e peso de maturidade da amostra.
- O `ResearchAgent` preserva evidência estruturada `claim → evidence → source`, sem atribuir confiança artificial.
- Cada evidência possui `source_id` ordinal para compatibilidade com `[fonte:N]` e `source_ref` SHA-256 determinístico da proveniência material.
- O ResearchAgent agora também calcula adequação lexical determinística para cada claim citado, distinguindo `SUSTENTADA`, `INSUFICIENTE` e `INDETERMINADA`.

## 3. CI validado
- Runs #344, #345, #351 e #352 — **100% GREEN** em Python 3.11/3.12/3.13/3.14.
- O Run #357 (`34725783075`) também foi confirmado **100% GREEN** em Python 3.11/3.12/3.13/3.14.
- O incremento de adequação de evidência criou novos commits depois do Run #357; o CI do HEAD atual ainda está **PENDENTE** e deve ser confirmado antes de declarar este incremento OK.

## 4. Incrementos concluídos
### Quality Routing
- Histórico persistente de avaliação por `provider + modelo + tipo_tarefa`.
- Gate de amostra mínima e peso de maturidade.
- Influência limitada a ±1,0.
- Testes adversariais impedem que qualidade domine capability ou confiabilidade fortes.

### Evidência estruturada de pesquisa
- `EvidenciaPesquisa` e `AfirmacaoPesquisa`.
- Proveniência: título, URL, trecho e consulta.
- `confianca=None` sem avaliação explícita.
- Fonte inexistente não cria evidência.
- Propagação para `ResultadoAgente`, métricas e `ExecutionTrace.metadata`.
- `source_ref` determinístico.
- ADRs `ADR-025` e `ADR-026`.

### Adequação de evidência — implementação concluída, validação CI pendente
- Novo `src/nexora/runtime/verificacao_evidencia.py`.
- Sinais lexicais determinísticos e auditáveis; nenhuma alegação de prova semântica.
- Estados: `SUSTENTADA`, `INSUFICIENTE`, `INDETERMINADA`.
- Integração com `AfirmacaoPesquisa`, métricas e trace.
- Testes para correspondência forte, ausência de suporte, múltiplas fontes, fonte válida porém não sustentadora, trecho vazio e parâmetros inválidos.
- ADR: `ADR-027-evidence-adequacy-verification.md`.

## 5. Próximo passo após CI
Se o CI do HEAD atual ficar verde, o próximo incremento obrigatório é **verificação de qualidade da evidência além de sobreposição lexical**, mantendo a distinção entre sinal auditável e prova semântica. Se falhar, corrigir primeiro o CI e não avançar.

## 6. Limites reais
- Checkpoint/idempotência/Registry/delegações ainda possuem componentes em memória.
- Sandbox é governança de subprocesso, não isolamento OS forte.
- Auditoria JSONL não é prova criptográfica de imutabilidade.
- World Model/Knowledge ainda não constituem inteligência mundial completa.
- Economic Engine ainda não fecha o loop oportunidade → produto → mercado → receita → reinvestimento.
- Autonomia econômica completa ainda não existe.
- Ollama ainda requer validação real com daemon/modelo instalado.
- Groq ainda requer validação real HTTP/tool-calling antes de ser considerado integração de produção validada.
- `ExecutionTrace` ainda não possui backend distribuído universal.
- Qualidade histórica é observacional e contextual; não é previsão.
- `source_ref` identifica a proveniência observada, mas não autentica a fonte remota nem prova a veracidade do conteúdo.
- Adequação lexical é apenas um sinal de cobertura textual; não é prova semântica nem prova de verdade.

## 7. O que NÃO fazer
- Não criar outra NEXORA, outro repositório ou terceiro Runtime.
- Não duplicar Permission, Policy, Checkpoint ou Tool Registry.
- Não apagar Long-Term Autonomy.
- Não transformar NEXORA em wrapper de produto externo.
- Não introduzir retry de efeito externo sem idempotência, autorização, precondições e verificação.
- Não remover `core/ciclo.py` prematuramente.
- Não declarar autonomia econômica completa antes de fechar o loop real do North Star.
- Não tratar URL, fingerprint, citação ou sobreposição lexical como prova automática de verdade.

## 8. Protocolo operacional
`AUDITAR → DECIDIR → IMPLEMENTAR → TESTAR → ATUALIZAR PROJECT_MEMORY → COMMIT → PUSH → VERIFICAR CI → HANDOFF`

GitHub permanece a fonte de verdade.
\n## 9. Ecosystem Integration Foundation — 2026-09-27\n\nA NEXORA passou por uma auditoria ampla do ecossistema open-source de agentes. A lista e as decisões estão em `docs/ECOSYSTEM_HARVEST.md`.\n\n### Capacidades já implementadas nesta rodada\n- Memory híbrida: `src/nexora/memoria/hibrida.py`.\n- World Model temporal: `src/nexora/world/grafo_temporal.py`.\n- Retry tipado/seguro: `src/nexora/runtime/retry.py`, integrado ao AgentRuntime.\n- Checkpoint persistente opcional: `src/nexora/runtime/checkpoint.py`.\n- Sandbox backend plugável: `src/nexora/runtime/sandbox_backend.py` + Sandbox atualizado.\n- MCP contracts: `src/nexora/integracoes/mcp.py`.\n- MCP → Tool Registry: `src/nexora/integracoes/mcp_adapter.py`.\n- Research guardrails: `src/nexora/agentes/pesquisa_guardrails.py` + ResearchAgent atualizado.\n- GenAI tracing: `src/nexora/observabilidade/genai.py` + AgentRuntime atualizado.\n- Evolution Engine: `src/nexora/evolucao/engine.py`.\n- Dream Cycle: `src/nexora/evolucao/dream_cycle.py`.\n- Opportunity Engine: `src/nexora/economia/oportunidades.py`.\n- Economic Loop: `src/nexora/economia/loop.py`.\n\n### Segurança preservada\n- Retry de efeito externo não idempotente é negado pela RetryPolicy.\n- MCP não recebe bypass do Registry governado.\n- Sandbox Docker não executa automaticamente; adapter falha fechado.\n- EvolutionEngine não promove mutações sem evidência/gate.\n- Economic Loop não movimenta dinheiro.\n- Research guardrails bloqueiam destinos locais/reservados antes do contexto.\n\n### Estado de validação\nOs commits desta rodada foram implementados e acompanhados por testes unitários. **O CI do HEAD final deve ser confirmado antes de declarar a rodada 100% validada.**\n\n### Próximo trabalho\n1. Confirmar CI.\n2. Integrar MemoryHibrida + GrafoTemporal ao Context/Knowledge real, sem criar segundo sistema de memória.\n3. Integrar outcome verification às ferramentas reais.\n4. Criar adapters reais opcionais para MCP/OpenSandbox/browser.\n5. Fortalecer evolução com benchmarks/regressão.\n6. Expandir Economy até Product → Market → Revenue → Reinvestment, mantendo aprovação humana para efeitos financeiros.\n\n\n## 10. Fechamento da Ecosystem Integration Foundation — 2026-09-27\n\n### Validação\n- HEAD final: `abbbd856207bac518cd311f591bfa5fe679525ac`.\n- CI Run #416 (`36345435513`): **GREEN** em Python 3.11, 3.12, 3.13 e 3.14.\n- Total validado: **392 testes passando**.\n\n### Últimas correções\n- Sandbox preserva compatibilidade com patching de `nexora.runtime.sandbox.subprocess` enquanto usa backend plugável.\n- ResearchAgent remove marcadores de citação `[fonte:N]` antes de agrupar claims para reconciliação; a citação continua preservada na evidência original.\n- BrowserAdapter é fail-closed quando nenhum backend externo foi injetado.\n- GateReinvestimento exige autorização humana antes de qualquer efeito financeiro.\n\n### Estado final desta rodada\nA auditoria de ecossistema deixou de ser apenas pesquisa e agora possui fundamentos implementados e testados para Memory, World Model, Runtime/Retry, Checkpoint persistente, Sandbox backend, MCP, Research Guardrails, Observability, Evolution, Economy, Browser adapter e reinvestimento governado.\n\n### Próximo trabalho\nA próxima grande integração não é adicionar mais frameworks. É conectar os novos fundamentos aos módulos canônicos já existentes: Memory/World/Context/Knowledge, Verification/Outcome, Provider routing, Tool/MCP adapters e Product/Economy. Sempre auditar antes para evitar duplicação.\n
## Checkpoint documental final — 2026-09-27
- HEAD mais recente no momento deste registro: `6e09c1b4096947a028bfe94ad981947df1295e1a`.
- Run #421 (`36345499730`) confirmado GREEN em Python 3.11/3.12/3.13/3.14.
- Os 392 testes continuam passando no checkpoint de código imediatamente anterior; as alterações posteriores deste checkpoint são apenas documentação de continuidade.
