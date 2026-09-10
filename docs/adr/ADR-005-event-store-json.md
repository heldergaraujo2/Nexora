# ADR-005 — Backend do event store: append-only JSON

- Status: Aprovada (Fase 0.5)
- Data:2026-09-10
- Decisao de origem: P5 (PROJECT_MEMORY/09_DECISIONS.md)
- Relacionamentos: ADR-004 (JSON versionado,ADR-011 (logs estruturados

## Contexto

O principio "tudo e evento" exige um registro auditavel e reconstruivel de acoes,decisoes,autorizacoes,custos e observacoes. O MVP precisa de um event store simples,sem servico externo,que permita replay e auditoria( alinhado ao requisito de estado event-sourced do 04_ARCHITECTURE_REQUIREMENTS.md )。

## Decisao

Adotar **append-only JSON** como event store inicial: um arquivo( ou sequencia de arquivos por dia/volume)onde eventos sao **apenas anexados**( nunca editados/removidos),cada evento com id,carimbo,origem,tipo e payload conforme `docs/contracts/evento.schema.json`. Estrategia planejada: evoluir para SQLite/WAL quando houver volume/concorrencia。

## Consequencias

- Positivas: simplicidade e auditabilidade total( append-only e imutavel, permitindo replay fiel;diff via git;zero dependencia de infraestrutura;
- Negativas: leituras sequenciais ficam caras com volume;nao ha indices( queries exigem varredura);concorrencia de escrita exige lock simples;
- Neutras: o runtime consumira eventos via camada de abstraccao( event store interface),entao a troca de backend nao toca nos produtores/consumidores。