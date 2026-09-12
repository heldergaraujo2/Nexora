# ADR-021 — Histórico de custo e desempenho por provider/modelo

**Status:** accepted — foundation

## Contexto

O roteamento da NEXORA inicialmente usava histórico agregado por provider. Isso não distinguia dois modelos do mesmo provider com preços, latência ou confiabilidade diferentes.

## Decisão

1. `ProviderManager` mantém métricas históricas também por par exato `provider + modelo`.
2. O histórico por modelo contém chamadas, sucesso/erro, latência, tokens e custo real.
3. A persistência usa schema v4 e mantém leitura compatível com schemas v1, v2 e v3.
4. Custo somente é registrado quando existem tokens reais e preço publicado para o modelo.
5. Quando o par candidato possui pelo menos três chamadas, o roteador usa primeiro seu histórico específico de confiabilidade e latência, evitando misturar modelos diferentes do mesmo provider.
6. Se o par ainda não possui amostra suficiente, o roteador mantém o histórico agregado do provider como fallback de compatibilidade.
7. O mínimo de três gerações precificadas permanece obrigatório para o sinal de custo.
8. A influência do custo permanece limitada a ±0,75 e somente compara candidatos que tenham amostra suficiente.
9. Não há estimativa de custo nem mistura silenciosa de modelos quando existe histórico específico suficiente.
10. `considerar_custo=False` continua desativando o sinal de custo.

## Consequência

A matriz de decisão passa a distinguir modelos do mesmo provider para confiabilidade, latência e custo. Isso prepara a NEXORA para combinar qualidade, capacidade, latência, tokens, custo e confiabilidade em granularidade de modelo.

## Limitação atual

O sinal continua sendo histórico observado e determinístico. Ainda não representa qualidade semântica, valor da tarefa ou custo futuro previsto. Essas dimensões permanecem etapas posteriores do roteador.
