# ADR-008 — Angulo do MVP: Codificacao

- Status: Aprovada (Fase 0.5)
- Data:2026-09-10
- Decisao de origem: P8 (PROJECT_MEMORY/09_DECISIONS.md}
- Relacionamentos: ADR-001 (Python),ADR-003 (CLI,ADR-007 (sandbox,secao B (Coding Agent,na Discovery

## Contexto

A NEXORA precisa validar o nucleo( objetivo,plano,execucao,verificacao,memoria,eventos)com um caso de uso concreto que entregue valor tangivel e testavel. As opcoes eram:agente de codificacao( escrever/editar arquivos,rodar testes,git,,agente de pesquisa( buscar,ler,sintezar,)ou automacao de workflow( acionar APIs,processos. Codificacao tem o criterio de aceitacao mais objetivo( testar que a saida funciona) e exercita a maioria das capacidades do nucleo( tools,terminal,sandbox,verificacao,eventos,memoria。

)。

## Decisao

Adotar **agente de codificacao** como angulo de validacao do MVP( ex: tarefas tipo "implementar uma funcao e rodar os testes" em repositorio escopado), focando em capacidades:ler/editar arquivos,rodar comandos sandbox,rodar testes e interpretar resultados,registrar eventos e custo,e verificar entre etapas。

## Consequencias

- Positivas: criterios de sucesso objetivos( testes passando);exercita pipeline completo( objetivo->plano->tools->verificacao->memoria->eventos);valor tangivel desde o inicio;
- Negativas: implementar bem dedica carga significativa de ferramentas( editor,terminal,git,)na Fase  6 do roadmap( Coding Agent — mas as ferramentas base serao parte da Fundacao);
- Neutras: pesquisa e automacao podem ser adicionadas depois reutilizando o mesmo nucleo( research engine e experience engine,nao subsistemas independentes( Proposta A,do 09_DECISIONS.md)。