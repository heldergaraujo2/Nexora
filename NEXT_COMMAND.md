# NEXT COMMAND — Fase 0.5: Decisão e Design

> **Canal de comando da coordenação.** Este arquivo contém o comando atual,a ser executado pelo agent construсor(OpenHands). Ao concluir,o agent deve atualizar `PROJECT_MEMORY/15_HANDOFF.md` e marcar esta seção como executada;então,o coordenador redigirá o próximo comando aqui.

**Origem:** Coordenador/Arquiteto(Arena agent central) — após auditoria do estado do repositório e aprovação do criador.

 Entregue via o link do repositório.



## COMANDO — Fase 0.5: Decisão e Design(sem código!

**OBJETIVO:** Converter a Capability Discovery já auditada e integrada(02–05) em **decisões formais** (ADRs) e **contratos iniciais por schema**, mais a **estrutura de repositório proposta** — tudo como **documentação**,sem escrever código de produção.



**CONTEXTO OBRIGATÓRIO — leia nesta ordem:**

1. `PROJECT_MEMORY/15_HANDOFF.md`( este repo — ponto de continuidade)
2. `PROJECT_MEMORY/08_CURRENT_STATE.md`( estado e estrutura)
3. `PROJECT_MEMORY/09_DECISIONS.md`( decisões aprovadas + P1–P11 provisórios)

4. `PROJECT_MEMORY/04_ARCHITECTURE_REQUIREMENTS.md`( requisitos arquiteturais)
5. `PROJECT_MEMORY/05_DISCOVERY_HANDOFF.md`( handoff da Discovery,seções 6–9)
6. `PROJECT_MEMORY/07_ROADMAP.md`( roadmap v1)
7. `PROJECT_MEMORY/14_AGENT_PROTOCOL.md`( protocolo obrigatório)



**ESCOPO( o que produzir:**

1. **ADRs**( Architecture Decision Records) das **decisões P1–P11**(decisões provisisórias em 09_DECISIONS.md)— formalizá-las com contexto,decisão,e consequências,cada uma em `docs/adr/ADR-00X-<nome>.md`( ou um único `docs/adr.md` bem estruturado,se preferir — mas por arquivo é mais auditável)
2. **Contratos iniciais por schema**( JSON Schema) em `docs/contracts/`:
   - `objetivo.schema.json`( intenção,escopo,restrições,critérios de sucesso,autonomia nível,orçamento)

   - `plano.schema.json`( DAG de subtarefas com dependências,validação acíclica…)
   - `provider.schema.json`( interface tipada:generate/stream/tools/capabilities/errors…)
   - `evento.schema.json`( eventos de primeira classe:carimbo,origem,tipo,dados…)
   - `tool.schema.json`( registry versionado:schema,risco,permissão,documentação…)
   - `delegacao.schema.json`( contrato de delegação:especialidade,entregável,verificação…)
   - `memoria.schema.json`( curto/longo prazo,provenance,versionamento,governança…)
   - `aprovacao.schema.json`( gates de aprovação humana:ação,escopo,decisor,evidência…)
3. **Estrutura de repositório proposta**( como PROPOSTA,não implementação):um `docs/design/repositorio.md` descrevendo:
   - Diretórios( src/nexora/,tests/,docs/,PROJECT_MEMORY/…)
   - Nomes/namespaces dos módulos( core,config,logging,providers,tools,runtime,…em conformidade com 04)
   - Arquivos-base previstos( __init__.py,pyproject.toml,AGENTS.md,…)
   - Fluxo de módulos( como o ciclo agente atravessa providers→tools→verify→memory→events)
   - Não criar código — apenas o desenho proposta
4. **Atualizar a memória do projeto** ao concluir:
   - `PROJECT_MEMORY/08_CURRENT_STATE.md`( estado: Fase  0.5 concluída`)
   - `PROJECT_MEMORY/09_DECISIONS.md`( formalizar P1–P11 como "decisões registradas",com data e responsável;adicionar ADRs referenciados)

   - `PROJECT_MEMORY/11_TASKS.md`( marcar os itens da Fase  0.5 concluídos)
   - `PROJECT_MEMORY/13_CHANGELOG.md`( registrar a mudança«
   - `PROJECT_MEMORY/15_HANDOFF.md`( novo ponto de continuação:Fase  1 — Fundação,aguardando aprovação explícita)


**CRITÉRIOS DE ACEITAÇÃO( tudo verificável:**

- [ ] Nenhum código de produção criado( sem src/,sem dependências,etc.)
- [ ] Nenhum teste formal exigido( sem código)
- [ ] P1–P11 formalizados como ADRs( com contexto,decisão,e consequências)
- [ ] Contratos em `docs/contracts/` cobrindo pelo menos:Objetivo,Plano/DAG,Provider,Evento,Tool,Delegação,Memória,Aprovação
- [ ] Estrutura de repositório proposta documentada( `docs/design/repositorio.md` ou similar)
- [ ] 08/09/11/13/15 atualizados e consistentes
- [ ] Tudo commitado com mensagem descritiva( ex:`docs(fase-0.5): ADRs,contratos e estrutura proposta`)
- [ ] `15_HANDOFF.md` indica o novo ponto de continuação(Fase `1` — Fundação) e que a próxima etapa exige aprovação explícita do criador/coordenador

**PROTOCOLO:** seguir `PROJECT_MEMORY/14_AGENT_PROTOCOL.md`( sem exceções:veracidade,rastreabilidade,autorização,comunicação por eventos/arquivos,escrever em PT-BR,usar git com mensagens descritivas,etapas pequenas verificáveis)

 mantendo tudo em PT-BR,em markdown limpo(sem zero-width spaces,sem caracteres estranhos,verificar antes de commitar。

**DATA DE VALIDADE:** v0.1 — válido até a conclusão desta Fase  0.5;após isso,aguardar novo comando do coordenador.