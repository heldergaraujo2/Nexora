# ADR-010 — Multi-agente no MVP: nao

- Status: Aprovada (Fase 0.5)
- Data:2026-09-10
- Decisao de origem: P10 (PROJECT_MEMORY/09_DECISIONS.md}
- Relacionamentos: ADR-008 (angulo codificacao,secao G (multi-agent,na Discovery

## Contexto

A orquestracao multi-agente( delegacao,comunicacao entre agentes,revisao cruzada,)agrega complexidade significativa( protocolos,registrys,estado por agente,)antes do nucleo estar validado. O MVP pode entregar o valor de um agente unico com ciclo completo( objetivo->plano->execucao->verificacao->memoria->eventos,)deixando a orquestracao para a Fase  4.5 do roadmap( Multi-Agent Orchestration。。



## Decisao

Adotar **agente unico ( orchestrator monolitico interno )** no MVP,desenhando porem os **contratos de delegacao( `docs/contracts/delegacao.schema.json` )e o registry de agentes desde cedo( como artefatos/design,nao codigo activo);assim,a orquestracao futura reutilizara os mesmos contratos sem reescrever o nucleo。

## Consequencias

- Positivas: reducao de risco e escopo( fluxo de um agente so);contratos prontos para evolucao( registry de agentes,delegacao tipada,verificacao de entregavel);oque aprendermos no agente unico alimenta o design da orquestracao;

- Negativas: capacidades multi-agente ficam para depois( nao sera possivel paralelizar tarefas independentes no MVP;;a "experiencia" de coordenar multiplos agentes sera limitada;
- Neutras: o orchestrator interno podera assumir papel de "agente principal" quando a orquestracao vier,com sub-agentes especializados registrados( conforme 04_ARCHITECTURE_REQUIREMENTS.md,G1-G3 。