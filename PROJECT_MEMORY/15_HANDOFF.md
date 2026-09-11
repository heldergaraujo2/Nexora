# 15 — HANDOFF

> Arquivo principal de continuidade. Todo novo agente deve começar por este arquivo e validar o HEAD/CI antes de alterar código.

## Estado Atual
- Release histórica: `v1.0.0` na tag `v1.0.0` → `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- HEAD atual após reconciliação documental: será o commit desta atualização de documentação.
- O projeto não está congelado no estado v1.0.0: houve evolução pós-release significativa.
- Não foi criada uma nova fase. O estado é **evolução arquitetural pós-release em reconciliação**.

## Onde Parou
A Fase 16 — Long-Term Autonomy permanece concluída e preservada.

Depois dela foram implementados e testados, em diferentes commits:
- Context Engine;
- Knowledge Engine;
- World Model Engine;
- Goal Engine;
- Strategy Engine;
- Communication Bus;
- integração de Runtime e Orchestrator com comunicação;
- DelegadorAgentes;
- Agent Registry / Capability Registry;
- delegação por capacidade.

## Arquitetura real dos agentes
- `AgenteRegistro` descreve agente, capacidades, tags, prioridade, disponibilidade e metadados.
- `RegistroAgentes` registra, lista, descobre por capacidade e seleciona deterministicamente o melhor agente disponível.
- `CommunicationBus` transporta mensagens e mantém correlação/estado; não executa ferramentas/providers.
- `DelegadorAgentes` cria delegações, publica solicitações e publica resultados quando a delegação é atualizada.
- `delegar_por_capacidade()` escolhe automaticamente o agente disponível de maior prioridade para a capacidade solicitada.
- Runtime e Orchestrator publicam eventos de ciclo no Bus.

## Limites / Lacunas verificadas
- Registry ainda é em memória e não possui ciclo completo de versionamento/persistência/governança.
- Seleção por capacidade é determinística, mas ainda simples: capacidade normalizada + disponibilidade + prioridade.
- Delegação é infraestrutura/contrato: o Delegador não executa a tarefa nem aciona automaticamente o agente executor.
- Retorno de delegação existe como mensagem correlacionada, mas a transição de estado é feita por `atualizar()`; não há ainda ciclo automático executor → resultado → verificação → memória.
- Context, Knowledge, World Model, Goals e Strategy são MVPs determinísticos e em memória.

## Classificação arquitetural
Os componentes pós-release foram tratados como **ADAPTAR/CRIAR dentro da arquitetura própria da NEXORA**, quando aplicável: eles materializam requisitos já definidos para registry, capacidades, comunicação e delegação. Não houve cópia de implementação privada externa.

Não há evidência suficiente para declarar um componente como REPLICAR ou SUPERAR com base apenas no código atual; essa classificação deve ser retomada quando houver comparação formal de capacidades externas.

## Testes
- Antes da correção: CI no `fc77446...` executou `163 passed, 2 failed`.
- As falhas estavam nos testes de integração de Runtime/Orchestrator com o Bus.
- Diagnóstico: os testes esperavam `ENTREGUE` sem assinantes; o contrato atual do Bus mantém `PENDENTE` nesse cenário.
- Correção mínima aplicada somente nos dois testes para refletir o contrato existente.
- CI foi disparado novamente e deve ser verificado no HEAD final antes de encerrar esta reconciliação.

## CI
Workflow: `.github/workflows/tests.yml`.
Matriz configurada: Python 3.11, 3.12, 3.13 e 3.14.
O resultado final da execução mais recente deve ser registrado após conclusão do workflow.

## Próximo Passo
**Não iniciar uma nova fase automaticamente.**

Após o CI verde, o próximo trabalho recomendado é definir, por decisão arquitetural explícita, o próximo incremento da arquitetura de agentes: transformar a infraestrutura atual de registry/capability/delegation em um ciclo de execução multi-agente verificável, com execução, retorno, verificação, recuperação, auditoria e integração com memória/governança.

Isso é uma **recomendação**, não uma fase aprovada.

## Instruções para o próximo agente
1. Ler este HANDOFF e `08_CURRENT_STATE.md`.
2. Confirmar o HEAD atual.
3. Confirmar CI verde no HEAD.
4. Não assumir que v1.0.0 é o estado atual.
5. Não criar nova fase sem comando explícito do coordenador.
6. Antes de alterar `bus.py`, ler o arquivo atual e os testes atuais.
7. Antes de implementar algo novo, procurar código, testes e PROJECT_MEMORY para evitar duplicação.
