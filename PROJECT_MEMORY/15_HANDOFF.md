# 15 — HANDOFF

> Arquivo principal de continuidade. Todo novo agente deve começar por este arquivo, confirmar o HEAD e verificar o CI antes de alterar código.

## Estado Atual
- Release histórica: `v1.0.0` → tag `v1.0.0` → `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- HEAD conhecido imediatamente antes desta atualização: `314f34ff5feee09be6bfa3aea307d2310ffbd8e9`.
- O commit desta própria atualização será o novo HEAD; confirmar o SHA real ao iniciar a próxima sessão.
- O projeto não está congelado no estado v1.0.0.
- Não foi criada uma nova fase durante a reconciliação.

## Onde Parou
A Fase 16 — Long-Term Autonomy permanece concluída e preservada.

Depois dela foram implementados:
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
- Seleção por capacidade é determinística, mas simples: capacidade normalizada + disponibilidade + prioridade.
- Delegação é infraestrutura/contrato: o Delegador não executa a tarefa nem aciona automaticamente o agente executor.
- Retorno de delegação existe como mensagem correlacionada, mas a transição de estado é feita por `atualizar()`; ainda não há ciclo automático executor → resultado → verificação → memória.
- Context, Knowledge, World Model, Goals e Strategy são MVPs determinísticos e em memória.

## Classificação arquitetural
Os componentes pós-release foram tratados como **ADAPTAR/CRIAR dentro da arquitetura própria da NEXORA**, quando aplicável: materializam requisitos já definidos para registry, capacidades, comunicação e delegação. Não houve cópia de implementação privada externa.

Não há evidência suficiente para declarar um componente como REPLICAR ou SUPERAR com base apenas no código atual; essa classificação deve ser retomada quando houver comparação formal de capacidades externas.

## Testes
- No `fc77446...`: `163 passed, 2 failed`.
- Diagnóstico: dois testes esperavam `ENTREGUE` sem assinantes, em desacordo com o contrato do Bus.
- Correção mínima aplicada somente aos dois testes, sem alterar o CommunicationBus.
- CI do commit de código corrigido `16a425a8c2dacdaa841b9678f6f6651155adee07`: **success** (run 36).
- Commits posteriores desta reconciliação são documentacionais; o workflow é disparado novamente a cada push.

## CI
Workflow: `.github/workflows/tests.yml`.
Matriz: Python 3.11, 3.12, 3.13 e 3.14.
Última evidência verde do código corrigido: run 36, head `16a425...`, conclusão `success`.
O CI do HEAD documental final deve ser verificado na próxima sessão se ainda estiver em execução.

## Próximo Passo
**Não iniciar uma nova fase automaticamente.**

Recomendação técnica: avaliar, por decisão arquitetural explícita, a transformação da infraestrutura atual de registry/capability/delegation em um ciclo de execução multi-agente verificável, com execução, retorno, verificação, recuperação, auditoria, memória e governança.

Isso é recomendação, não autorização de uma nova fase.

## Instruções para o próximo agente
1. Ler este HANDOFF e `08_CURRENT_STATE.md`.
2. Confirmar o HEAD real do `main`.
3. Verificar o CI do HEAD real; se o último workflow ainda estiver em execução, aguardar sua conclusão antes de implementar.
4. Não assumir que v1.0.0 é o estado atual.
5. Não criar nova fase sem comando explícito do coordenador.
6. Antes de alterar `bus.py`, ler o arquivo atual e os testes atuais.
7. Antes de implementar algo novo, procurar código, testes e PROJECT_MEMORY para evitar duplicação.
