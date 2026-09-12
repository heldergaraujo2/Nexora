# ADR-025 — Evidência estruturada no Research Agent

## Status
Implementação inicial; aprovação final condicionada ao CI do HEAD.

## Contexto
O `ResearchAgent` já coletava fontes e exigia citações `[fonte:N]`, mas o resultado continuava predominantemente textual. Isso dificultava distinguir uma afirmação citada de uma fonte realmente preservada pelo runtime.

## Decisão
Adicionar uma camada mínima e determinística de evidência estruturada:

```text
claim
  ↓
evidence
  ↓
source_id / titulo / url / trecho / consulta
  ↓
proveniência
```

O contrato inclui:
- `EvidenciaPesquisa` para representar a fonte observada;
- `AfirmacaoPesquisa` para ligar uma afirmação textual a uma evidência;
- `confianca=None` quando não existe avaliação explícita de confiança.

O `ResearchAgent`:
- mantém as fontes atuais e sua compatibilidade;
- converte somente citações `[fonte:N]` válidas em vínculos estruturados;
- ignora referências a fontes inexistentes no índice coletado;
- adiciona as evidências ao `ResultadoAgente`;
- replica a estrutura em `metricas` e `ExecutionTrace.metadata`;
- não trata uma URL isolada como prova de verdade.

## Consequências
### Positivas
- Pesquisa deixa de depender exclusivamente de texto livre para preservar proveniência.
- Claims podem ser auditados contra fonte, trecho e consulta.
- A estrutura pode evoluir futuramente para confiança, múltiplas fontes e resolução de entidades.
- Compatibilidade com o contrato atual de busca é preservada.

### Limitações
- A extração de claim é deliberadamente sintática e baseada na frase que contém a citação.
- Não existe ainda verificação semântica de que o trecho realmente sustenta a afirmação.
- `confianca` permanece ausente até existir um avaliador explícito.

## Testes
- Unitários para vínculo claim → evidence → source.
- Fonte inexistente não gera evidência.
- Saída sem citação continua falhando na verificação existente.
- Integração valida propagação para `ResultadoAgente` e `ExecutionTrace`.
- CI do HEAD é o critério final de aprovação.
