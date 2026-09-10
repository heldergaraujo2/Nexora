# ADR-007 — Sandbox do MVP: subprocesso isolado

- Status: Aprovada (Fase 0.5)
- Data:2026-09-10
- Decisao de origem: P7 (PROJECT_MEMORY/09_DECISIONS.md)
- Relacionamentos: ADR-008 (angulo codificacao),K2 (sandbox e isolamento na Capability Discovery)

## Contexto

Execucao de codigo/comandos exige isolamento( default-deny,quotas,lifecycle,)mas o MVP nao deve depender de Docker/containers( peso,complexidade,)nem de infraestrutura remota. A execucao de comandos( terminal para o coding agent,e para ferramentas de build/teste)precisa ser contida o suficiente para nao comprometer o host nem vazar segredos( ver K2/K3 na Discovery)。

## Decisao

Adotar **subprocesso isolado** como sandbox do MVP:execucao via `subprocess` com:

- usuario/grupo nao privilegiado quando viavel;
- diretorio de trabalho escopado( workspace/projeto);
- env minimo e sanitizado( sem segredos do host injetados automaticamente;injeccao seletiva via credential broker;
- limites: timeout,quilobyte de saida,maximo de processos filho;
- rede: bloqueada por padrao( allowlist quando obrigatorio;
- auditoria: cada execucao registrada como evento( comando,saida,exit code,custo);

Se bubblewrap estiver disponivel no ambiente,sua camada extra de isolamento( mount namespace)sera usada quando viavel. Docker fica para fase posterior( quando multiplos subprocessos/services exigirem isolamento mais forte)。

## Consequencias

- Positivas: leve,imediato,sem dependencias de infraestrutura; suficiente para conter erros simples e limitar superficie( rede off por padrao,env sanitizado;;auditavel portando no event store;
- Negativas: nao e isolamento de kernel forte( processos podem ver o host se nao houver bubblewrap/compartimentos);vazamento entre execucoes de um mesmo workspace precisa de hygiene( workspace efemero ou reset por tarefa);
- Neutras: a interface de sandbox( `Sandbox.execute(command)`)mantem o runtime desacoplado,permitindo trocar para Docker/gVisor depois sem tocar nos consumidores。