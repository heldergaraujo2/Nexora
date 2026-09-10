# NEXT COMMAND — Fase 4 — Provider System (roteamento avançado)

> Protocolo: seguir o `14_AGENT_PROTOCOL.md`; implementar,testar,atualizar memória( 08/09/11/13/15),commit e push ao concluir。

## Pré-requisitos

- Fase 3 concluída e pushada( roteador, orquestrador, CLI executar;51 testes verdes)

 
## Escopo

Provider System/roteamento avançado( conforme 10_MODULES.md):

1. **Fallback por health-check**:`Roteador.obter_provider` deve tentar o provider recomendado e, envão disponível, tentar o próximo por ordem do registry( registrando o evento de fallback)。
2. **Seleção por capacidade**:método `listar_por_capacidade(tool_calling=..., streaming=...)` no `RegistryProviders`( filtrando por `ProviderCapability`)。
3. **Ordenação e prioridade**:registro mantém ordem de prioridade( `registrar(nome, fabrica, prioridade=...)` opcional);`recomendar` pode receber `preferencias`。
4o **Registro de latência/erro**:`ProviderManager` é responsável por medir tempo de `generate` e registrar falhas（ expondo `estatisticas()` com contagem de chamadas,erros e latência média）。
5。 **Health-check**:`saudavel()` já existe no contrato;**novo** `obter_healthcheck(nome)` que retorna o resultado detalhado do health-check sem instanciar o provider necessariamente。
 
## Critérios de Aceitação

- [ ] `Roteador` tenta fallback automático quando provider recomendado não está saudável
- [ ] `RegistryProviders.listar_por_capacidade` filtra corretamente
- [ ] `ProviderManager` expõe `estatisticas()` com chamadas,erros,latência média
- [ ] `obter_healthcheck(nome)` retorna detalhes( saudavel,motivo,ultima_falha)
)
- [ ] Todos os 51 testes anteriores continuam verdes
- [ ] Novos testes unitários para cada capacidade implementada
- [ ] Memória atualizada( 08/09/11/13/15)e NEXT_COMMAND.md reescrito para a Fase 5
- [ ] Commit e push da Fase 4
 
## Protocolo

1. Auditar estado atual( `git status`,,suíte de testes)
2. Implementar por incrementos pequenos com testes
3. Rodar suíte completa ao final( `python3 -m pytest tests/ -q`)
4. Atualizar memória( 08_CURRENT_STATE,09_DECISIONS,11_TASKS,13_CHANGELOG,15_HANDOFF)

5o Commit(e push com mensagem descritiva do tipo `feat(fase-4): ...`