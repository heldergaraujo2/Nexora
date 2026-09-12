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
9. A amostra recebe `peso_amostra` determinístico: no limiar mínimo o peso é 0,5; ele cresce linearmente até 1,0 em `2 × min_amostra` e não ultrapassa 1,0.
10. O ajuste de qualidade usa esse peso antes do limite final de ±1,0, evitando que o primeiro conjunto de avaliações elegíveis domine o roteamento.

## Limites

- O score de qualidade é observacional, não preditivo.
- Ainda não existe ponderação temporal, janela de recência ou detecção de drift.
- Ainda não há avaliação semântica universal; a qualidade depende dos critérios/evidências fornecidos pelo `AvaliadorResultado`.
- `peso_amostra` é uma proteção heurística de maturidade, não um intervalo estatístico de confiança.

## Testes

- Limiar abaixo da amostra impede o sinal e retorna peso 0.
- Limiar atingido expõe score, taxa e peso 0,5.
- Duas vezes o limiar permite peso 1,0.
- Provider, modelo e tipo são isolados.
- Ajuste no limiar mínimo é conservador e não ultrapassa a política existente.
- Ajuste com amostra madura pode atingir o limite de ±1,0.
- Limiar inválido é rejeitado.
- CI continua sendo o critério final de aprovação.
