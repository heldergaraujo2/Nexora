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
- `HistoricoAvaliacao` agora persiste qualidade por `provider + modelo + tipo_tarefa`.
- **Qualidade ainda NÃO influencia o roteamento.**

## 3. Último checkpoint validado
- CI run #315 (`34714728583`) — **100% GREEN**.
- Python 3.11: success.
- Python 3.12: success.
- Python 3.13: success.
- Python 3.14: success.
- O run #315 validou a fundação de avaliação de resultado antes do novo incremento de histórico de qualidade.

## 4. Trabalho deste incremento
Implementado:
- `src/nexora/runtime/historico_avaliacao.py` — histórico persistente versionado (`schema_version=1`).
- `src/nexora/core/plano.py` — `Tarefa.tipo` explícito e retrocompatível.
- `src/nexora/orquestracao/orquestrador.py` — integração opcional de `AvaliadorResultado` + `HistoricoAvaliacao`; registra qualidade após execução.
- `tests/unit/test_historico_avaliacao.py` — persistência, isolamento, ausência de qualidade e validação.
- `tests/integration/test_orquestrador_avaliacao_historico.py` — fluxo real Orchestrator → Runtime → Evaluation → History → reload.
- `docs/adr/ADR-023-persistent-task-quality-history.md` — decisão arquitetural.
- `PROJECT_MEMORY/17_TASK_QUALITY_HISTORY.md` — continuidade do incremento.

## 5. Regras de qualidade
1. Teste escrito não significa teste aprovado.
2. Toda funcionalidade nova precisa de testes unitários e integração quando cruza componentes.
3. CI do HEAD é o critério final de aprovação.
4. Nunca inventar score, tokens, custo ou evidência.
5. Qualidade não entra no roteador antes de amostra mínima e testes de isolamento por tipo/provider/modelo.
6. Não misturar histórico entre modelos ou tipos de tarefa.

## 6. Próximo passo obrigatório
Após o CI deste incremento ficar verde:
1. definir limiar mínimo de amostra de qualidade;
2. adicionar testes de insuficiência de amostra e isolamento;
3. expor consulta de qualidade para o `RoteadorInteligente` sem ainda alterar o score;
4. integrar qualidade ao score somente após evidência suficiente;
5. manter fórmula determinística e explicável: `capability × quality × reliability × latency × tokens × cost`.

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
