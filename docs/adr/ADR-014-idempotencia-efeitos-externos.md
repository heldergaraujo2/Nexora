# ADR-014 — Idempotência para efeitos externos

## Status

ACEITA — contrato inicial, sem habilitar retries externos.

## Contexto

O `AgentRuntime` possui retry para operações que podem ser repetidas com segurança, mas ferramentas que produzem efeitos externos (pagamento, publicação, envio, alteração remota, criação de recurso etc.) não podem ser automaticamente repetidas sem uma identidade de operação e uma política explícita de recuperação.

A arquitetura da NEXORA exige o fluxo:

`precondition → authorization → idempotency → execution → verification → compensation → audit`

A etapa de idempotência deve existir antes de permitir retries de efeitos externos.

## Decisão

Adicionar um contrato mínimo em `src/nexora/runtime/idempotencia.py` com:

- `chave` única da operação;
- `fingerprint` da operação para detectar reutilização indevida da chave;
- estado `IN_PROGRESS`, `SUCCEEDED` ou `FAILED`;
- registro do resultado conhecido;
- operação atômica de `reivindicar` protegida por lock no store em memória;
- rejeição de uma mesma chave associada a outro fingerprint;
- função determinística `fingerprint_operacao()` baseada em JSON canônico + SHA-256.

A primeira reivindicação cria `IN_PROGRESS`. Reivindicações posteriores com a mesma identidade devolvem o mesmo registro e **não autorizam uma segunda execução**.

Uma operação `FAILED` também não será automaticamente reexecutada apenas porque a mesma chave foi apresentada novamente. Uma política futura deverá decidir explicitamente se, quando e como uma operação falha pode ser recuperada.

## Limites deliberados desta etapa

- O store é somente em memória e vale apenas dentro do processo.
- Não há persistência durável.
- Não há lock distribuído.
- Não há retry de efeito externo habilitado por este ADR.
- Não há compensação/rollback automático.
- Não há integração obrigatória com todas as ferramentas ainda.

## Consequências

Positivas:

- cria uma barreira explícita contra duplicação acidental;
- torna colisões de identidade detectáveis;
- prepara a arquitetura para retries seguros no futuro;
- permite testar a semântica antes de integrar efeitos reais.

Negativas:

- operações ainda não sobrevivem a reinício do processo;
- o chamador continua responsável por decidir quando executar e concluir a operação;
- a garantia não é distribuída.

## Próxima evolução

Depois de validar este contrato, a integração deverá ocorrer no caminho canônico de ferramentas, preservando:

`Permission → Policy → Checkpoint → Idempotency → Tool → Observation → Verification → Audit → Result`

Somente após essa integração e seus testes deverá ser avaliada a habilitação de retries para efeitos externos, sempre condicionada a autorização, idempotência e verificação.
