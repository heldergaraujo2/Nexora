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
- No limiar mínimo, `peso_amostra=0,5`; em `2 × min_amostra`, chega a `1,0`; a influência final permanece limitada a ±1,0.

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
- O Run #345 valida também o cenário controlado em que qualidade diferencia candidatos com capacidade-base equivalente.

## 4. Incremento concluído — Quality Routing
Implementado e validado:
- Histórico persistente de avaliação por `provider + modelo + tipo_tarefa`.
- Gate de amostra mínima.
- Peso de maturidade `0,5 → 1,0` conforme a amostra cresce até `2 × min_amostra`.
- Influência final limitada a ±1,0.
- Testes adversariais confirmam que qualidade não domina capability forte nem confiabilidade histórica forte.
- Teste controlado confirma que qualidade consegue desempatar candidatos com capacidade-base equilibrada.
- Commit de validação controlada: `84335341a8effe42649f34979829e0a6de2841de`.

## 5. Regras de qualidade
1. Teste escrito não significa teste aprovado.
2. Toda funcionalidade nova precisa de testes unitários e integração quando cruza componentes.
3. CI do HEAD é o critério final de aprovação.
4. Nunca inventar score, tokens, custo ou evidência.
5. Qualidade só entra no roteador após amostra mínima e testes de isolamento por tipo/provider/modelo.
6. Não misturar histórico entre modelos ou tipos de tarefa.
7. Peso de maturidade é uma proteção heurística, não deve ser descrito como confiança estatística.
8. Qualidade não é benchmark universal; é sinal observacional contextual ao tipo de tarefa.

## 6. Próximo incremento obrigatório
**Evidência estruturada para pesquisa.**
1. Introduzir contrato explícito `Evidence`/`Claim` sem quebrar as fontes atuais.
2. Preservar `source`, `url`, `consulta`, trecho e confiança/proveniência quando disponíveis.
3. Fazer o `ResearchAgent` produzir resultado verificável sem depender somente de texto livre.
4. Criar testes unitários e integração para ausência de fonte, fonte válida, claim sem evidência e múltiplas fontes.
5. Integrar a evidência ao resultado/telemetria sem transformar uma string de URL em prova de verdade.
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

## 8. O que NÃO fazer
- Não criar outra NEXORA, outro repositório ou terceiro Runtime.
- Não duplicar Permission, Policy, Checkpoint ou Tool Registry.
- Não apagar Long-Term Autonomy.
- Não transformar NEXORA em wrapper de produto externo.
- Não introduzir retry de efeito externo sem idempotência, autorização, precondições e verificação.
- Não remover `core/ciclo.py` prematuramente.
- Não declarar autonomia econômica completa antes de fechar o loop real do North Star.

## 9. Protocolo operacional
`AUDITAR → DECIDIR → IMPLEMENTAR → TESTAR → ATUALIZAR PROJECT_MEMORY → COMMIT → PUSH → VERIFICAR CI → HANDOFF`

GitHub permanece a fonte de verdade.
