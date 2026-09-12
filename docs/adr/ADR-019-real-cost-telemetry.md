# ADR-019 — Telemetria de custo real por provider/modelo

**Status:** accepted — foundation
**Data:** 2026-09-12

## Contexto

A NEXORA ja mede tokens reais retornados pelos providers, mas nao possuia uma camada de precificacao versionada. Sem essa camada, preencher `ExecutionTrace.cost` exigiria estimativa ou preco implicito, o que nao e aceitavel para observabilidade economica.

## Decisao

Adicionar um `PricingRegistry` deterministico, versionado por snapshot, com:

- provider e modelo explicitos;
- moeda explicitamente registrada;
- preco separado para tokens de entrada e saida por 1 milhao de tokens;
- versao e data de vigencia;
- fonte autoritativa do preco;
- custo calculado somente quando `GenerationResult.usage` fornece contagens reais validas.

O `ProviderManager` calcula e acumula `custo_total` apenas quando existe correspondencia exata entre provider/modelo e uma entrada do registro. Quando o preco nao existe ou o uso nao e mensuravel, o custo permanece desconhecido (`None` no trace) e nao e estimado.

`ExecutionTrace.cost` recebe o custo calculado em USD no caminho `Orquestrador -> ProviderManager -> Provider`.

## Snapshot inicial

O snapshot inicial usa precos publicos do catalogo de modelos da Groq em 2026-09-12 para:

- `groq/openai/gpt-oss-120b`: US$ 0,15 / MTok de entrada e US$ 0,60 / MTok de saida;
- `groq/openai/gpt-oss-20b`: US$ 0,075 / MTok de entrada e US$ 0,30 / MTok de saida.

Modelos Groq marcados como `Contact Sales` nao sao incluidos e portanto nao recebem custo estimado.

## Persistencia

O schema de historico do `ProviderManager` evoluiu de v2 para v3 e inclui:

- `custo_total`;
- `geracoes_com_custo`.

Historicos v1 e v2 continuam sendo carregados com os novos campos iniciando em zero.

## Consequencias

### Positivas

- custo observavel sem inventar dados;
- base para roteamento sensivel a custo;
- rastreabilidade de versao/fonte do preco;
- compatibilidade com providers que nao fornecem uso ou precificacao publica.

### Limitacoes

- o snapshot precisa ser atualizado quando o provider altera sua tabela;
- custos contratados individualmente nao sao inferidos;
- descontos, tiers, cache e modalidades especiais ainda nao sao modelados genericamente;
- custo local de infraestrutura/energia nao e tratado como custo de API.

## Testes obrigatorios

A funcionalidade deve manter testes para:

1. calculo entrada + saida;
2. provider/modelo sem preco retornando desconhecido;
3. validacao de tokens;
4. acumulacao e persistencia de custo;
5. propagacao para `ExecutionTrace.cost`;
6. integracao sem executar o provider duas vezes.
