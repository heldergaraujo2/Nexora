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
- O `ResearchAgent` agora preserva evidência estruturada `claim → evidence → source`, sem atribuir confiança artificial.
- Cada evidência possui `source_id` ordinal para compatibilidade com `[fonte:N]` e `source_ref` SHA-256 determinístico da proveniência material.

## 3. CI validado
- Run #344 (`34721678128`) — **100% GREEN**.
- Python 3.11: success.
- Python 3.12: success.
- Python 3.13: success.
- Python 3.14: success.
- Run #345 (`34721984271`) — **100% GREEN**.
- Python 3.11: success.
- Python 3.12: success.
- Python 3.13: success.
- Python 3.14: success.
- Run #351 (`34722084768`) — **100% GREEN**.
- Python 3.11: success.
- Python 3.12: success.
- Python 3.13: success.
- Python 3.14: success.
- Run #352 (`34722089714`) — **100% GREEN**.
- Python 3.11: success.
- Python 3.12: success.
- Python 3.13: success.
- Python 3.14: success.
- Os Runs #351/#352 validaram a integração da evidência estruturada com pesquisa, resultado e trace.

## 4. Incremento concluído — Quality Routing
Implementado e validado:
- Histórico persistente de avaliação por `provider + modelo + tipo_tarefa`.
- Gate de amostra mínima.
- Peso de maturidade `0,5 → 1,0` conforme a amostra cresce até `2 × min_amostra`.
- Influência final limitada a ±1,0.
- Testes adversariais confirmam que qualidade não domina capability forte nem confiabilidade histórica forte.
- Teste controlado confirma que qualidade consegue desempatar candidatos com capacidade-base equilibrada.
- Commit de validação controlada: `84335341a8effe42649f34979829e0a6de2841de`.

## 5. Incremento concluído — Evidência estruturada de pesquisa
Implementado:
- `EvidenciaPesquisa` e `AfirmacaoPesquisa`.
- Preservação de título, URL, trecho e consulta.
- `confianca=None` quando não há avaliação explícita.
- Claims só são ligados a índices de fonte realmente existentes.
- Evidências são propagadas para `ResultadoAgente`, métricas e `ExecutionTrace.metadata`.
- `source_ref` determinístico para identidade estável da proveniência material.
- Testes para fonte válida, fonte inexistente, ausência de citação, vínculo claim/evidence e estabilidade do fingerprint.
- ADRs: `ADR-025-evidence-structured-research.md` e `ADR-026-stable-source-identity.md`.

## 6. Próximo incremento obrigatório
**Verificação de adequação da evidência, sem fingir compreensão semântica.**
1. Introduzir um verificador explícito que diferencie `fonte existente` de `evidência suficiente`.
2. Não marcar uma claim como comprovada apenas porque contém `[fonte:N]`.
3. Começar com sinais determinísticos e auditáveis; não atribuir confiança probabilística sem fundamento.
4. Criar testes para correspondência forte, correspondência insuficiente, múltiplas fontes e fonte válida porém não sustentadora.
5. Integrar o resultado ao `ResearchAgent`, `ResultadoAgente` e `ExecutionTrace` sem quebrar compatibilidade.
6. CI verde antes de considerar o incremento concluído.

## 7. Limites reais
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

## 8. O que NÃO fazer
- Não criar outra NEXORA, outro repositório ou terceiro Runtime.
- Não duplicar Permission, Policy, Checkpoint ou Tool Registry.
- Não apagar Long-Term Autonomy.
- Não transformar NEXORA em wrapper de produto externo.
- Não introduzir retry de efeito externo sem idempotência, autorização, precondições e verificação.
- Não remover `core/ciclo.py` prematuramente.
- Não declarar autonomia econômica completa antes de fechar o loop real do North Star.
- Não tratar URL, fingerprint ou citação como prova automática de verdade.

## 9. Protocolo operacional
`AUDITAR → DECIDIR → IMPLEMENTAR → TESTAR → ATUALIZAR PROJECT_MEMORY → COMMIT → PUSH → VERIFICAR CI → HANDOFF`

GitHub permanece a fonte de verdade.
