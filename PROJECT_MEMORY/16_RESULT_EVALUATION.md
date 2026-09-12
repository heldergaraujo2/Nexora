# 16 — RESULT EVALUATION

## Estado
Foundation implementada em 2026-09-12.

## Objetivo
Adicionar à NEXORA um sinal de qualidade baseado em evidência explícita do resultado, sem inventar métricas e sem substituir o ciclo canônico de Verification.

## Implementado
- `src/nexora/runtime/avaliacao.py`
- `ResultadoAvaliacao`: sucesso, score `[0,1]`, critérios, evidências e metadados.
- `AvaliadorResultado`: composição de avaliadores explícitos e média determinística.
- `AgenteRuntime` aceita avaliador opcional.
- Resultado da avaliação é propagado para `ResultadoAgente`, métricas, `ExecutionTrace.metadata.evaluation`, registrador e CommunicationBus.
- Sem avaliador, compatibilidade legada permanece.
- Sem critérios, o sistema não presume qualidade.
- ADR-022 formaliza a decisão.

## Testes
- `tests/unit/test_avaliacao_resultado.py`
- `tests/unit/test_agente_runtime_avaliacao.py`
- CI é obrigatório antes de considerar o incremento concluído.

## Limite atual
A avaliação ainda é apenas um sinal por execução. Ela não influencia o roteador automaticamente.

## Próximo passo
Criar histórico persistente de avaliação por `provider + modelo + tipo de tarefa`, com limiar mínimo de amostra, e somente então estudar sua incorporação ao score do `RoteadorInteligente`.

## Regra
Qualidade somente pode ser usada quando houver evidência real e critérios explícitos. Não estimar qualidade por texto, custo, latência ou tamanho da resposta.
