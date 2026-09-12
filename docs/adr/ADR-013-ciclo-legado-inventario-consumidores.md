# ADR-013 — Ciclo simples como legado e inventário de consumidores

**Data:** 2026-09-12  
**Status:** Aprovada para migração gradual

## Contexto

A ADR-012 definiu o `AgenteRuntime` como proprietário do ciclo avançado de execução e determinou que `src/nexora/core/ciclo.py` fosse preservado temporariamente como contrato de compatibilidade.

A revisão do estado atual do repositório mostrou que:

- `src/nexora/orquestracao/orquestrador.py` importa e utiliza `AgenteRuntime` como caminho normal de execução;
- o Orchestrator não importa `Executor`, `Verificador` ou `executar_ciclo` de `core/ciclo.py`;
- o teste legado `tests/unit/test_ciclo.py` é um consumidor explícito do contrato histórico;
- não foi encontrada, na busca do repositório, outra referência textual aos símbolos `ExecutorCiclo`, `VerificadorCiclo`, `executar_ciclo` ou `core.ciclo` além do próprio contrato/teste legado e da documentação relacionada.

A evidência atual é suficiente para classificar `core/ciclo.py` como **legado/compatibilidade**, mas não é suficiente para removê-lo imediatamente: o teste público existente ainda protege o contrato histórico e a remoção sem uma etapa dedicada poderia quebrar consumidores externos não indexados.

## Decisão

1. `src/nexora/core/ciclo.py` permanece no repositório como contrato legado/compatibilidade.
2. O módulo é explicitamente documentado como legado e recomenda `AgenteRuntime` para novos caminhos.
3. Nenhum novo componente de produção deve importar `core/ciclo.py` para criar um segundo motor de execução.
4. `tests/unit/test_ciclo.py` permanece durante a migração para proteger compatibilidade.
5. Antes da remoção futura, será feita uma etapa explícita de migração/depuração que:
   - confirme novamente os consumidores no código;
   - avalie a superfície pública do pacote;
   - determine se consumidores externos precisam de período de compatibilidade;
   - substitua/remova os testes somente quando o novo contrato estiver coberto;
   - execute a matriz completa de CI.
6. A NEXORA não criará um terceiro runtime para substituir este módulo.

## Estado de migração

```text
core/ciclo.py
    │
    ├── tests/unit/test_ciclo.py  ← consumidor legítimo atual
    │
    └── produção nova             ← NÃO USAR

orquestracao/orquestrador.py
    │
    └── AgentRuntime               ← caminho canônico
```

## Critério para aposentadoria

O arquivo só poderá ser removido ou reduzido quando houver evidência documentada de que:

1. não existem consumidores internos ativos;
2. a superfície pública legada foi avaliada;
3. existe cobertura equivalente para o caminho canônico;
4. a remoção não cria um segundo caminho de execução;
5. CI permanece verde em Python 3.11–3.14.

## Não objetivos

- Não alterar a semântica do ciclo legado nesta etapa.
- Não remover `Long-Term Autonomy`.
- Não alterar Permission/Policy/Checkpoint/Registry.
- Não adicionar retry externo.
- Não declarar a migração definitivamente concluída apenas por ausência de referências internas.
