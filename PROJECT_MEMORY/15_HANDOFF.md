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
