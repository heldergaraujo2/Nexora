# ADR-027 — Verificação determinística de adequação de evidência

## Status
Accepted

## Contexto
O ResearchAgent já preserva citações, proveniência e `source_ref`, mas a existência de uma citação não demonstra que o trecho da fonte sustenta o claim. Também não devemos fabricar confiança sem um avaliador semanticamente válido.

## Decisão
Adicionar um verificador explícito de adequação lexical, determinístico e auditável. Ele compara os termos relevantes do claim com os termos do trecho citado e retorna `SUSTENTADA`, `INSUFICIENTE` ou `INDETERMINADA`.

`SUSTENTADA` significa apenas cobertura lexical suficiente segundo o limiar configurado. Não significa prova da verdade, validade da fonte, atualidade ou compreensão semântica.

O resultado é anexado às afirmações do ResearchAgent e exposto em métricas e `ExecutionTrace.metadata`, preservando a estrutura anterior de evidências e mantendo `confianca=None` quando não houver avaliador real.

## Consequências
- Claims com fonte existente mas sem suporte textual deixam de parecer automaticamente comprovados.
- O comportamento é reproduzível e auditável.
- A abordagem é deliberadamente conservadora: verificação semântica real continua sendo trabalho futuro.
- Testes unitários cobrem suporte forte, ausência de suporte, múltiplas fontes, trecho vazio e parâmetros inválidos.
