# ADR-022 — Sinal explícito de avaliação de resultado

## Status
Accepted — foundation

## Contexto
O roteador inteligente já utiliza adequação, hardware, confiabilidade, latência e custo real quando disponível. Ainda faltava um sinal explícito de qualidade do resultado da tarefa.

Inferir qualidade a partir de texto, tamanho da resposta, custo ou latência seria frágil e criaria métricas artificiais.

## Decisão
A NEXORA passa a possuir um contrato opcional de avaliação explícita:

`ResultadoAvaliacao` contém:
- `sucesso`;
- `score` normalizado entre 0 e 1;
- critérios observáveis;
- evidências;
- metadados.

`AvaliadorResultado` agrega avaliadores explícitos e calcula a média dos scores, mantendo o resultado limitado a `[0, 1]`.

O `AgenteRuntime` pode receber um `AvaliadorResultado` opcional. Quando configurado, a avaliação é executada sobre o resultado final e registrada em:
- `ResultadoAgente.avaliacao`;
- `ResultadoAgente.metricas`;
- `ExecutionTrace.metadata.evaluation`;
- barramento de comunicação;
- registrador de experiência, quando configurado.

A avaliação **não substitui Verification** nesta primeira etapa e não altera o sucesso operacional do Runtime. Ela é um sinal observável adicional.

## Regras
1. Sem avaliador, o comportamento legado permanece intacto.
2. Sem critérios explícitos, qualidade não é inventada: o score é `0.0` e o resultado informa `nenhum_criterio_avaliacao`.
3. Nenhuma avaliação pode gerar tokens, custo ou qualidade estimados.
4. O avaliador não executa ferramentas nem efeitos externos.
5. O roteador não usará este sinal até existir histórico persistente e suficiente por tarefa/modelo.
6. Não criar outro Runtime.

## Próxima evolução
Criar histórico de avaliação por `provider + modelo + tipo de tarefa`, usando apenas avaliações reais, e posteriormente integrar esse sinal ao score do roteador com limiar mínimo de amostra.

## Testes
- contrato e serialização de `ResultadoAvaliacao`;
- agregação de múltiplos avaliadores;
- ausência de avaliação sem critérios;
- rejeição de retorno fora do contrato;
- integração `AgenteRuntime → avaliação → ExecutionTrace`;
- compatibilidade do Runtime sem avaliador.
