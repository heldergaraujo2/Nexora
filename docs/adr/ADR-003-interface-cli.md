# ADR-003 — Interface de entrada do MVP: CLI primaria

- Status: Aprovada (Fase 0.5)
- Data:�2026-09-10
- Decisao de origem: P3 (PROJECT_MEMORY/09_DECISIONS.md)
- Relacionamentos: ADR-002 (estrutura,ADR-011 (logs JSON)

## Contexto

O primeiro caso de uso da NEXORA precisa de uma interface de interacao que seja minima,testavel e integravel a automacoes. As opcoes eram CLI,API REST ou SDK Python. Uma API REST adicionaria servidor,portas e orquestracao de processos desde o inicio;um SDK exigiria desenhar superficie de API publica antes de validar o nucleo membrane。



## Decisao

Adotar **CLI como interface primaria do MVP**, executavel via `python -m nexora`,com saida estruturada( JSON quando possivel) e flags para configuracao,debug e verbose. Um SDK Python podera ser exposto depois,reutilizando as mesmas camadas internas( sem reescrever o nucleo)。

## Consequencias

- Positivas: superficie minima e testavel( chamadas de subprocesso em testes);facil integracao com automacoes e orquestracao( ex: via cron,CI/CD,outros agentes);sem servico/portas no MVP;
- Negativas: nao serve para acesso remoto/Web direto( exigira API depois);UX nao-visual( comando e flags);
- Neutras: a CLI sera o cliente do runtime( mesmo processo) — o runtime em si permanece biblioteca( `nexora.runtime` )。