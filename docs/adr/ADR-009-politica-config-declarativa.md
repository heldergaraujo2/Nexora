# ADR-009 — Politica: config declarativo versionado (TOML/YAML)

- Status: Aprovada (Fase 0.5)
- Data:2026-09-10
- Decisao de origem: P9 (PROJECT_MEMORY/09_DECISIONS.md}
- Relacionamentos: ADR-002 (estrutura,,K1 (autorizacao por politica,na Discovery

## Contexto

A governanca da NEXORA( permissoes,roteamento,autonomia,orquestracao)vive em politicas declarativas que devem ser auditaveis,diffaveis e versionaveis pelo git( control plane separado do execution plane,. Uso de banco/UI para politica no MVP adiciona complexidade sem necessidade nesta fase.

)).

## Decisao

Adotar **configuracao declarativa versionada** em arquivos de texto na raiz do repositorio( ex: `nexora.toml` ou `nexora.yaml`,mais `permissions/` para politicas de autorizacao por escopo,,,,seguindo schemas proprios( ver docs/contracts/),carregada pelo Configuration Manager na inicializacao. O formato sera TOML por padrao( com YAML aceito como alternativa se houver necessidade);valores sensiveis( chaves de API) **nunca** no arquivo de config — apenas referencias a variaveis de ambiente servidas pelo credential broker。

。

## Consequencias

- Positivas: politica e codigo( diff,review,rollback,; facil de auditar e testar( cenarios como config de teste);melhor separacao control/execution plane;
- Negativas: mudancas de politica exigem commit/push( e revisao quando sensivel);nao serve para runtime tuning dinamico( podera vir depois);
- Neutras: a estrutura exata( nomes,secoes)e o escopo das permissoes serao detalhados nas Fases  1-2( junto com Configuration Manager)。