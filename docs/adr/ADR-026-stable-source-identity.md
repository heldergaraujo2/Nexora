# ADR-026 — Identidade determinística da fonte de pesquisa

## Status
Implementação; aprovação final condicionada ao CI do HEAD.

## Contexto
O contrato inicial de evidência usava `source_id` como índice da fonte coletada. Esse índice é útil para interpretar `[fonte:N]`, mas muda quando a ordem das fontes muda. Isso limita deduplicação, auditoria e futuras referências persistentes.

## Decisão
Adicionar `source_ref`, um fingerprint SHA-256 determinístico calculado exclusivamente a partir de `titulo`, `url`, `trecho` e `consulta`.

O `source_id` ordinal permanece para compatibilidade com o formato `[fonte:N]`. O `source_ref` passa a ser a identidade estável da observação daquela fonte no contrato estruturado.

Regras:
- mesma proveniência material produz o mesmo `source_ref`;
- mudança de qualquer campo de proveniência produz outro `source_ref`;
- `source_id` não participa do fingerprint;
- não usar o fingerprint como prova de veracidade da fonte;
- não introduzir confiança artificial.

## Consequências
### Positivas
- Evidências podem ser correlacionadas independentemente da posição ordinal.
- Fica preparada uma futura camada de deduplicação e persistência de evidências.
- A proveniência permanece explícita e auditável.

### Limitações
- O fingerprint identifica o conteúdo/proveniência observada, não autentica a origem remota.
- Alterações no trecho ou metadados produzem uma nova identidade.

## Testes
- `source_ref` possui 64 caracteres hexadecimais.
- Mesmo material com `source_id` diferente produz o mesmo fingerprint.
- O conjunto completo de testes e CI Python 3.11–3.14 permanece obrigatório.
