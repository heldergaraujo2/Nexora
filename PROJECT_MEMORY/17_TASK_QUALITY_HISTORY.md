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
- A influência da qualidade é ponderada por `peso_amostra`: 0,5 no limiar mínimo e crescimento linear até 1,0 em `2 × min_amostra`.
- O peso é uma proteção heurística de maturidade; não representa intervalo estatístico de confiança.

## Validação controlada — 2026-09-12

- Teste adversarial confirmou que qualidade não vence uma vantagem forte de capability.
- Teste adversarial confirmou que qualidade não vence uma penalidade forte de confiabilidade histórica.
- Teste controlado confirmou que, quando a capacidade-base é equivalente, uma diferença observada de qualidade consegue alterar o ranking.
- Run #344 (`34721678128`) ficou verde em Python 3.11–3.14 para a correção do cenário de hardware.
- Run #345 (`34721984271`) ficou verde em Python 3.11–3.14 para a validação da influência controlada.

## Regra de segurança

Qualidade **não pode dominar o roteamento apenas porque atingiu o primeiro limiar**. A amostra mínima torna o sinal elegível; o `peso_amostra` reduz sua influência inicial. A influência permanece limitada a ±1,0 após a ponderação.

Não são fabricadas avaliações, tokens, custos ou qualidade. Dados ausentes permanecem ausentes.

## Testes

- Unitários: persistência/reload, isolamento por provider/modelo/tipo, ausência de qualidade sem registro e rejeição de score inválido.
- Gate de amostra: abaixo do limiar bloqueia o sinal e retorna peso 0.
- Maturidade: no limiar o peso é 0,5; em duas vezes o limiar o peso chega a 1,0.
- Roteamento: ajuste no limiar mínimo é conservador; amostra madura pode usar o peso integral; sinais continuam isolados por tarefa/modelo/provider.
- Adversariais: qualidade não domina capability ou confiabilidade forte.
- Controlado: qualidade desempata candidatos de capacidade-base equivalente.
- Integração: Orchestrator → AgentRuntime → Evaluation → HistoricoAvaliacao, com persistência e reload.
- CI deve permanecer como critério final de aprovação.

## Próximo incremento

1. Introduzir evidência estruturada no Research Agent: `claim → evidence → source → confidence/provenance`.
2. Preservar compatibilidade com as fontes atuais (`titulo`, `url`, `trecho`, `consulta`).
3. Fazer a síntese de pesquisa carregar referências estruturadas, não somente texto livre.
4. Criar testes para claims sem evidência, evidência válida, múltiplas fontes e fonte ausente.
5. Integrar evidência ao resultado/telemetria sem tratar URL isolada como prova de verdade.

Recência/janelas temporais e drift ficam posteriores, somente se houver necessidade comprovada.
