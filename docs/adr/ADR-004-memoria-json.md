# ADR-004 — Backend inicial de memoria: JSON versionado

- Status: Aprovada (Fase 0.5)
- Data:2026-09-10
- Decisao de origem: P4 (PROJECT_MEMORY/09_DECISIONS.md)
- Relacionamentos: ADR-005 (event store JSON,ADR-011 (logs JSON

## Contexto

A NEXORA precisa de persistencia inicial para memoria( curto e longo prazo,)sem introduzir dependencias pesadas( banco,vetorial) antes da validacao do nucleo. A memoria deve ser auditavel,revisivel e versionavel pelo proprio git( alinhado ao "source of truth = repositorio" );e os schemas devem ser definidos desde cedo( ver docs/contracts/memoria.schema.json )。

## Decisao

Adotar **JSON versionado** como backend inicial da memoria,armazenado em diretorio rastreado pelo git( ex: `PROJECT_MEMORY/data/` )com arquivos por dominio/tipo( memoria_semantica.json,memoria_episodica.json,memoria_procedural.json e decisao_log.json),cada um seguindo o schema de memoria。 A evolucao planejada: SQLite quando houver volume/consultas complexas,e depois vetorial( embeddings) para recuperacao semantica。

。



## Consequencias

- Positivas: simplicidade total( sem servico,sem dependencias);cada mudanca de memoria e versionada e revisavel via git( diff,historico,rollback);facil de inspecionar e debugar;

- Negativas: nao escala para muitas escritas( reescrita de arquivo,contention)nem consultas ricas nao-vetoriais;recuperacao semantica exige fase vetorial depois;
- Neutras: a interface/abstracao de memoria( com schemas)facilitara trocar backend sem tocar nos modulos consumidores。