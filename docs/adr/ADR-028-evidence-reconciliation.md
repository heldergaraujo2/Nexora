# ADR-028 — Reconciliação de múltiplas evidências

## Status
Aceita — implementação incremental.

## Contexto
A NEXORA já estrutura evidências de pesquisa e verifica sua adequação individual. Isso distingue existência de fonte de suporte lexical, mas ainda faltava uma camada para comparar múltiplas evidências sobre a mesma afirmação.

## Decisão
Adicionar `ReconciliadorEvidencias` em `src/nexora/runtime/reconciliacao_evidencia.py`.

A reconciliação:

- considera apenas evidências com adequação `SUSTENTADA`;
- deduplica por `source_ref` para evitar falsa independência;
- exige cobertura lexical mínima configurável;
- classifica como `CORROBORADA` quando existem pelo menos duas referências independentes com suporte compatível;
- classifica como `CONFLITANTE` quando há sinais lexicais explícitos de polaridade incompatível entre fontes adequadas;
- classifica como `NAO_CORROBORADA` quando não há suporte suficiente ou existe apenas uma fonte independente;
- não transforma URL, `source_ref`, quantidade de fontes ou sobreposição lexical em prova de verdade;
- mantém `confianca=None` por padrão.

## Limitações
A implementação é deliberadamente conservadora e determinística. Ela não executa compreensão semântica completa, não verifica a verdade factual e não resolve conflitos complexos, contexto temporal, causalidade ou dependência entre fontes. Diferentes URLs podem representar a mesma informação original; por isso `source_ref` é usado apenas como sinal de deduplicação, não como prova de independência epistemológica.

## Testes
O contrato é protegido por testes unitários para corroboração, fonte única, fontes irrelevantes, inadequação, duplicidade, conflito explícito, serialização, validação de configuração e claim vazio.
