# ADR-018 — Histórico Persistente de Providers

## Status

Accepted — fundação inicial.

## Contexto

O `ProviderManager` já mede chamadas, sucesso, falhas e latência por provider. Enquanto esses dados existirem somente em memória, o `RoteadorInteligente` perde a amostra histórica quando o processo é reiniciado.

A persistência precisa ser simples, reproduzível e desacoplada de banco de dados nesta etapa, sem transformar métricas ausentes em estimativas.

## Decisão

Adotar persistência opcional do histórico do `ProviderManager` em JSON versionado.

- `ProviderManager(persistencia_path=...)` habilita persistência explícita.
- `NEXORA_PROVIDER_HISTORY_PATH` permite configuração por ambiente.
- Sem caminho configurado, o comportamento permanece somente em memória.
- A escrita usa arquivo temporário e `os.replace` para reduzir risco de arquivo parcialmente escrito.
- O payload possui `schema_version` para permitir evolução controlada.
- Histórico inválido, incompatível ou ilegível não impede a inicialização; os dados inválidos são ignorados.
- Somente métricas efetivamente medidas são persistidas.
- A persistência não cria retry, não executa providers e não altera a decisão de governança.

## Consequências

### Positivas

- histórico sobrevive a reinicialização do processo;
- roteamento pode usar amostras acumuladas ao longo do tempo quando o caminho persistente estiver configurado;
- não adiciona banco de dados ou dependência externa;
- mantém compatibilidade com o comportamento in-memory existente.

### Limitações

- não é um store distribuído nem coordena múltiplas instâncias concorrentes;
- não oferece trilha criptográfica de auditoria;
- o arquivo local depende das permissões e confiabilidade do filesystem;
- migrações de schema futuras exigirão tratamento explícito.

## Testes

A evolução exige testes de escrita, recarga após novo `ProviderManager`, falhas persistidas, schema, escrita atômica e configuração por ambiente. O CI do HEAD deve ser verde antes de considerar o incremento concluído.
