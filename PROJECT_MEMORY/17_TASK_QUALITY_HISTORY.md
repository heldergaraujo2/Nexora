# 17 — TASK QUALITY HISTORY

## Objetivo

Preservar qualidade observada de tarefas para permitir, futuramente, que o roteamento inteligente use qualidade real sem fabricar métricas.

## Implementado — 2026-09-12

- `AvaliadorResultado` continua produzindo `ResultadoAvaliacao` explícito.
- `HistoricoAvaliacao` persiste métricas por `provider + modelo + tipo_tarefa`.
- Métricas atuais: avaliações, sucessos e score médio derivado de scores observados.
- Persistência opcional via caminho explícito ou `NEXORA_EVALUATION_HISTORY_PATH`.
- Schema inicial versionado (`schema_version=1`).
- Escrita atômica com arquivo temporário e `os.replace`.
- Carregamento tolerante a histórico inválido.
- `Tarefa.tipo` permite declarar o tipo de tarefa explicitamente.
- Sem tipo declarado, o Orchestrator usa classificação mínima determinística para manter compatibilidade.
- Orchestrator registra avaliação somente quando existe `AvaliadorResultado` e uma execução possui provider/modelo identificáveis.

## Regra de segurança

O histórico **não altera o score do RoteadorInteligente ainda**.

A existência de uma média histórica não é suficiente para afirmar que um modelo é melhor. Antes de influenciar seleção será necessário estabelecer amostra mínima, critérios estáveis e testes que impeçam mistura entre tipos de tarefa e modelos.

## Testes

- Unitários: persistência/reload, isolamento por provider/modelo/tipo, ausência de qualidade sem registro e rejeição de score inválido.
- Integração: Orchestrator → AgentRuntime → Evaluation → HistoricoAvaliacao, com persistência e reload.
- CI deve permanecer como critério final de aprovação.

## Próximo incremento

1. Definir limiar mínimo de amostra para qualidade.
2. Adicionar testes de isolamento e insuficiência de amostra.
3. Expor uma API de consulta adequada ao RoteadorInteligente.
4. Só então permitir que qualidade influencie o score, mantendo fallback seguro quando a amostra for insuficiente.
5. Evoluir posteriormente para avaliação temporal/contextual quando houver evidência suficiente.
