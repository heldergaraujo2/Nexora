# 17 — TASK QUALITY HISTORY

## Objetivo

Preservar qualidade observada de tarefas para permitir que o roteamento inteligente use qualidade real sem fabricar métricas.

## Implementado — 2026-09-12

- `AvaliadorResultado` produz `ResultadoAvaliacao` explícito.
- `HistoricoAvaliacao` persiste métricas por `provider + modelo + tipo_tarefa`.
- Métricas atuais: avaliações, sucessos e score médio derivado de scores observados.
- Persistência opcional via caminho explícito ou `NEXORA_EVALUATION_HISTORY_PATH`.
- Schema inicial versionado (`schema_version=1`).
- Escrita atômica com arquivo temporário e `os.replace`.
- Carregamento tolerante a histórico inválido.
- `Tarefa.tipo` permite declarar o tipo de tarefa explicitamente.
- Sem tipo declarado, o Orchestrator usa classificação mínima determinística para manter compatibilidade.
- Orchestrator registra avaliação somente quando existe `AvaliadorResultado` e uma execução possui provider/modelo identificáveis.
- `qualidade_para_roteamento()` aplica gate de amostra mínima.
- O `RoteadorInteligente` só usa qualidade quando o par exato `provider + modelo + tipo_tarefa` possui amostra suficiente e há pelo menos dois candidatos com evidência comparável.
- O sinal de qualidade é adicional aos sinais de capability, confiabilidade, latência e custo.
- A influência da qualidade agora é ponderada por `peso_amostra`: 0,5 no limiar mínimo e crescimento linear até 1,0 em `2 × min_amostra`.
- O peso é uma proteção heurística de maturidade; não representa intervalo estatístico de confiança.

## Regra de segurança

Qualidade **não pode dominar o roteamento apenas porque atingiu o primeiro limiar**. A amostra mínima torna o sinal elegível; o `peso_amostra` reduz sua influência inicial. A influência permanece limitada a ±1,0 após a ponderação.

Não são fabricadas avaliações, tokens, custos ou qualidade. Dados ausentes permanecem ausentes.

## Testes

- Unitários: persistência/reload, isolamento por provider/modelo/tipo, ausência de qualidade sem registro e rejeição de score inválido.
- Gate de amostra: abaixo do limiar bloqueia o sinal e retorna peso 0.
- Maturidade: no limiar o peso é 0,5; em duas vezes o limiar o peso chega a 1,0.
- Roteamento: ajuste no limiar mínimo é conservador; amostra madura pode usar o peso integral; sinais continuam isolados por tarefa/modelo/provider.
- Integração: Orchestrator → AgentRuntime → Evaluation → HistoricoAvaliacao, com persistência e reload.
- CI deve permanecer como critério final de aprovação.

## Próximo incremento

1. Validar experimentalmente o impacto da qualidade no ranking com cenários controlados e sem alterar a execução real.
2. Adicionar recência/janelas temporais somente quando houver necessidade comprovada de detectar mudança de comportamento.
3. Evoluir para avaliação contextual/semântica e evidências mais fortes antes de transformar qualidade em sinal dominante.
