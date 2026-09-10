# ADR-011 — Observabilidade: logs estruturados JSON rotativos

- Status: Aprovada (Fase 0.5)
- Data:2026-09-10
- Decisao de origem: P11 (PROJECT_MEMORY/09_DECISIONS.md}
- Relacionamentos: ADR-005 (event store,),ADR-004 (memoria JSON,secao K4 (audit trail,na Discovery

## Contexto

A NEXORA precisa de observabilidade para diagnostico,auditoria e metricas( custo,erros,)sem introduzir OpenTelemetry/endpoints desde o MVP. Apython logging padrao(saida texto multiformato)nao estrutura o suficiente para maquinas( parsing,correlacao,queries,)e o event store nao deve ser o unico destino de diagnostico operacional( logs diferem de eventos de dominio: frequencia,retencao,volume)。

## Decisao

Adotar **logs estruturados em JSON,rotativos**,via modulo de logging proprio( wrapper sobre `logging`,`com campos padrao:timestamp,nivel,evento,conversation_id,tool,erro,dados extra(,com rotacao por tamanho( e retencao configurable( via config declarativa,,destino padrao em `logs/`( gitignored),e um script/util simples de inspecao( ex: filtrar por nivel,campo,)sem depender de infraestrutura externa。 OTel fica para fase posterior( quando houver infraestrutura de observabilidade central。



## Consequencias

- Positivas: maquinas conseguem filtrar/correlacionar( jq,scripts;campos estaveis facilitam dashboards/budgets de custo;rotacao controla disco;independente de infraestrutura;
- Negativas: consultas complexas exigem ferramentas externas( ex:jq,ou OTel depois);log em JSON e menos legivel para humanos( ter modo texto opcional);
- Neutras: logs estruturados complementam(eventos de dominio no event store que sao fonte de verdade de baixo nivel; redudancia intencional entre logs e eventos e aceitavel( logs = operacao,eventos = auditoria/dominio)。