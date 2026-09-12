# ADR-024 — Quality routing sample gate

## Status
Accepted — foundation

## Contexto

A NEXORA já persiste avaliações observadas por `provider + modelo + tipo_tarefa`. Uma média isolada não deve ser tratada como evidência suficiente para alterar a seleção de modelos.

## Decisão

1. `HistoricoAvaliacao.qualidade_para_roteamento()` passa a ser a API explícita para consultar prontidão da amostra.
2. O chamador informa `min_amostra` e recebe `amostra_suficiente` junto com métricas observadas.
3. Score médio e taxa de sucesso só ficam disponíveis para o roteador como sinal elegível quando a amostra atinge o limiar.
4. A chave de isolamento permanece exatamente `provider + modelo + tipo_tarefa`.
5. Amostras de outros modelos, providers ou tipos não são agregadas.
6. O `RoteadorInteligente` usa essa API e, quando pelo menos dois candidatos possuem amostra suficiente, pode aplicar o sinal de qualidade ao score de forma determinística e limitada a ±1.0.
7. Com amostra insuficiente, o ajuste de qualidade é exatamente zero.
8. A qualidade não substitui capability, confiabilidade, latência ou custo; é apenas um sinal adicional.

## Limites

- O score de qualidade é observacional, não preditivo.
- Ainda não existe ponderação temporal, janela de recência ou detecção de drift.
- Ainda não há avaliação semântica universal; a qualidade depende dos critérios/evidências fornecidos pelo `AvaliadorResultado`.

## Testes

- Limiar abaixo da amostra impede o sinal.
- Limiar atingido expõe score e taxa observados.
- Provider, modelo e tipo são isolados.
- Limiar inválido é rejeitado.
- CI continua sendo o critério final de aprovação.
