# ADR-021 — Histórico de custo por provider/modelo

**Status:** accepted — foundation

## Contexto

O roteamento de custo da NEXORA inicialmente usava custo histórico agregado por provider. Isso não distinguia dois modelos do mesmo provider com preços, comportamento ou uso diferentes.

## Decisão

1. `ProviderManager` mantém métricas históricas também por par exato `provider + modelo`.
2. O histórico por modelo contém chamadas, sucesso/erro, latência, tokens e custo real.
3. A persistência evolui para schema v4 e mantém leitura compatível com schemas v1, v2 e v3.
4. Custo somente é registrado quando existem tokens reais e preço publicado para o modelo.
5. O roteador usa o histórico específico do par candidato antes de qualquer consideração de custo.
6. O mínimo de três gerações precificadas permanece obrigatório para influenciar a decisão.
7. A influência permanece limitada a ±0,75 e somente compara candidatos que tenham amostra suficiente.
8. Não há estimativa de custo nem mistura silenciosa de modelos.
9. `considerar_custo=False` continua desativando o sinal de custo.

## Consequência

A matriz de decisão passa a distinguir modelos do mesmo provider e prepara a NEXORA para otimizar qualidade, capacidade, latência, tokens, custo e confiabilidade em granularidade de modelo.

## Limitação atual

O sinal de custo continua sendo histórico observado e determinístico. Ainda não representa qualidade semântica, valor da tarefa ou custo futuro previsto. Essas dimensões permanecem etapas posteriores do roteador.
