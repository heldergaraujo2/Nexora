# ADR-018 — Histórico Persistente de Providers

## Status

Accepted — fundação inicial com schema v2.

## Contexto

O `ProviderManager` mede chamadas, sucesso, falhas e latência por provider. O histórico pode ser persistido para que o `RoteadorInteligente` mantenha amostras após reinicializações.

A persistência precisa ser simples, reproduzível e desacoplada de banco de dados nesta etapa, sem transformar métricas ausentes em estimativas.

Com a integração do caminho real do Orchestrator, também é necessário preservar telemetria de tokens quando o provider fornece contadores confiáveis.

## Decisão

Adotar persistência opcional do histórico do `ProviderManager` em JSON versionado.

- `ProviderManager(persistencia_path=...)` habilita persistência explícita.
- `NEXORA_PROVIDER_HISTORY_PATH` permite configuração por ambiente.
- Sem caminho configurado, o comportamento permanece somente em memória.
- A escrita usa arquivo temporário e `os.replace` para reduzir risco de arquivo parcialmente escrito.
- O payload possui `schema_version`.
- Schema v2 adiciona `prompt_tokens`, `completion_tokens`, `total_tokens` e `geracoes_com_tokens` por provider.
- Schema v1 continua sendo carregado com defaults para os novos campos, permitindo evolução compatível.
- Histórico inválido, incompatível ou ilegível não impede a inicialização; os dados inválidos são ignorados.
- Somente métricas efetivamente medidas são persistidas.
- Tokens somente são registrados quando o provider fornece inteiros não negativos válidos. A NEXORA não estima tokens.
- O caminho `Orquestrador → ProviderManager.executar_instancia()` mede a instância já selecionada, sem criar ou executar uma segunda instância.
- A telemetria de tokens é propagada ao `ExecutionTrace` real.
- A persistência não cria retry, não executa providers por conta própria e não altera a decisão de governança.
- Custo não é estimado. Só poderá ser incorporado quando houver pricing autoritativo e versionado por provider/modelo.

## Consequências

### Positivas

- histórico sobrevive a reinicialização do processo;
- roteamento pode usar amostras acumuladas ao longo do tempo quando o caminho persistente estiver configurado;
- tokens medidos podem acompanhar o histórico e o trace;
- não adiciona banco de dados ou dependência externa;
- mantém compatibilidade com o comportamento in-memory existente;
- evita dupla execução do provider para obter métricas.

### Limitações

- não é um store distribuído nem coordena múltiplas instâncias concorrentes;
- não oferece trilha criptográfica de auditoria;
- o arquivo local depende das permissões e confiabilidade do filesystem;
- pricing/custo permanece ausente sem fonte autoritativa;
- providers que não fornecem usage não geram tokens por estimativa;
- migrações de schema futuras exigirão tratamento explícito.

## Testes

A evolução exige testes de escrita, recarga após novo `ProviderManager`, falhas persistidas, schema, escrita atômica, configuração por ambiente, contagem de tokens e integração real com o Orchestrator.

O checkpoint atual foi validado pelo CI run `34704095484`, com sucesso em Python 3.11, 3.12, 3.13 e 3.14.
