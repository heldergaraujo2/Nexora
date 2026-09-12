# ADR-017 — Roteamento Inteligente de Provider e Modelo

## Status

Accepted — fundação inicial.

## Contexto

A NEXORA pode utilizar múltiplos providers e modelos. A escolha não deve ficar presa a um único fornecedor nem tratar o modelo como uma decisão independente das capacidades reais do ambiente.

O roteamento precisa considerar, de forma determinística e explicável:

- adequação do modelo à tarefa;
- hardware disponível;
- capacidades declaradas pelo provider;
- capacidade de contexto;
- saúde do provider quando explicitamente exigida.

A execução permanece responsabilidade do `AgentRuntime`; o roteador apenas toma a decisão.

## Decisão

Adotar `RoteadorInteligente` como camada de decisão provider/modelo.

O fluxo é:

`Candidatos → Adequação do modelo → Hardware → Capacidades do provider → Saúde opcional → Score → Decisão explicável → AgentRuntime`

O roteador:

1. ignora providers não registrados;
2. ignora candidatos inválidos;
3. rejeita requisitos de capability não suportados;
4. rejeita contexto incompatível;
5. pode rejeitar provider indisponível quando `exigir_provider_saudavel=True`;
6. utiliza o score determinístico de adequação do modelo;
7. retorna motivos explícitos para cada decisão;
8. não executa providers, ferramentas ou tarefas;
9. não inventa benchmarks, custo, tokens ou latência.

A arquitetura deve permanecer provider-agnostic. Nenhum provider é hard-coded como caminho obrigatório.

## Evolução planejada

Histórico real de execução poderá ser incorporado progressivamente, usando somente métricas efetivamente medidas pela NEXORA, como latência, sucesso e falhas. Esses dados deverão produzir ajustes limitados e explicáveis, sem substituir a adequação funcional do modelo.

Custos, tokens e benchmarks só poderão participar do roteamento quando houver dados reais e confiáveis para eles.

## Consequências

### Positivas

- decisões reproduzíveis;
- explicabilidade do motivo da escolha;
- compatibilidade com múltiplos providers;
- separação clara entre decisão e execução;
- extensão futura para histórico operacional sem criar um terceiro runtime.

### Limitações atuais

- histórico persistente ainda não participa do score;
- custo e orçamento ainda não participam do roteamento;
- não há benchmark automático de qualidade;
- a saúde do provider só é consultada quando explicitamente exigida.

## Testes

Toda evolução do roteamento deve incluir testes unitários e, quando cruzar componentes, testes de integração. CI deve permanecer verde antes de declarar a evolução concluída.
