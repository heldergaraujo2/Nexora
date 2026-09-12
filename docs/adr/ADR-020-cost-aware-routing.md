# ADR-020 — Roteamento orientado por custo real histórico

## Status
Accepted — implementação inicial.

## Contexto
A NEXORA já mede tokens reais, calcula custo somente quando existe pricing autoritativo/versionado e persiste o histórico do `ProviderManager`. O próximo passo do `RoteadorInteligente` é usar esse sinal econômico sem permitir que custo substitua adequação funcional, segurança ou capacidade.

## Decisão
O `RoteadorInteligente` pode aplicar um ajuste pequeno baseado no custo real histórico observado por provider.

Regras:

1. Somente custo calculado a partir de tokens reais e preço conhecido participa.
2. É necessária uma amostra mínima de 3 gerações precificadas por provider.
3. O sinal é comparativo apenas entre providers candidatos que também possuam histórico de custo suficiente.
4. O custo observado é normalizado por milhão de tokens usando `custo_total / total_tokens`.
5. Custo pelo menos 10% abaixo da média dos candidatos recebe `+0.75`.
6. Custo pelo menos 10% acima recebe `-0.75`.
7. Diferenças menores não alteram o score.
8. A influência pode ser desativada por `considerar_custo=False`.
9. Sem dados suficientes, não existe penalização nem estimativa.
10. A decisão continua determinística e explicável pelos motivos do candidato.

## Por que não usar custo como critério dominante
Um provider mais barato pode ser inadequado para coding, tool-calling, contexto, qualidade ou disponibilidade. O score funcional continua sendo a base da decisão; custo é apenas um sinal econômico limitado.

## Limitação conhecida
O histórico atual é agregado por provider. Se um provider alternar entre vários modelos, o custo histórico representa uma média observada do provider e não um benchmark isolado de cada modelo. Uma evolução futura poderá persistir métricas por `provider/modelo`.

## Fluxo
`Provider → Usage real → PricingRegistry → custo real → ProviderManager → histórico → RoteadorInteligente → ajuste limitado → ExecutionTrace`

## Testes
Foram adicionados testes para:
- preferência por menor custo real histórico;
- ausência de influência com amostra insuficiente;
- desativação explícita do sinal de custo.

O CI do commit deste ADR deve ser considerado o critério final de aprovação do incremento.
