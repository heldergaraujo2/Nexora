# 11 — TASKS

## Concluídas

- [x] Fase 0(Continuidade e Memória): estrutura,README,.gitignore,PROJECT_MEMORY 00–15 integrado)
- [x] Capability Discovery( do agent construсor):02–05 integrados ao fluxo canônico
- [x] Integração de repositório( renumeração única,fusão 00/01,README,handoff atualizado)
- [x] Propostas A–E aprovadas pelo criador
- [x] P1–P11 recomendados pelo coordenador( provisóriosç — aguardando ratificação final

## Próximas(Fase 0.5 — Decisão e Design,(sem código:

- [ ] Responder/ratificar as decisões P1–P11 com o criador( em 09_DECISIONS.md)
- [ ] Produzir ADRs( Architecture Decision Records) das decisões( docs/adr/
- [ ] Produzir contratos iniciais por schema( JSON Schema):Objetivo,Plano/DAG,Provider,Evento,Tool,Delegação,Memória,Aprovação( docs/contracts/
- [ ] Propor a estrutura de repositório final( src/nexora/ + módulos) em design doc( docs/
- [ ] Atualizar 08_CURRENT_STATE,e 15_HANDOFF após conclusão

## Futuras(Fase 1 — Fundação,após aprovação explícita):

- [ ] Core Runtime básico( ciclo agente,event store simples,checkpoints…)
- [ ] Configuration Manager( env+arquivo declarativo YAML/TOML)
- [ ] Environment Manager
- [ ] Logging estruturado JSON rotativo
- [ ] Error Handling com classificação de falhas
- [ ] Process Manager
- [ ] CLI mínimo( python -m nexora --help)
- [ ] Interface inicial
- [ ] Version Manager
- [ ] Test Framework( pytest)
- [ ] Health Checks
- [ ] Runtime básico + runtime simples
- [ ] Gerenciamento de processos,configuração,sistema de eventos interno
## Concluido na Fase 0.5 (Decisao e Design, sem codigo:
 
- [x] 11 ADRs criados e aprovados em docs/adr/ (ADR-001..011, cobrindo P1-P11)
- [x] Indice de ADRs em docs/adr/README.md
- [x] 8 contratos JSON Schema criados e validados em docs/contracts/
- [x] Design doc em docs/design/repositorio.md propondo estrutura de repositorio,modulos e fluxo
- [x] Canal construidor-analyiso testado (HELLO) e registrado em CANAL_CONSTRUTOR.md
- [x] Caracteres zero-width/CJK sanitizados dos docs
 
## Proxima (Fase 1 — Fundacao, apos aprovacao explicita:
 
- [ ] Receber aprovacao do criador/analista para iniciar a Fase 1
- [ ] Implementar cores basicos (ciclo de agente,event store simples,checkpoints)
- [ ] Configuration Manager,Environment Manager,Logging estruturado JSON,Error Handling,Process Manager,CLI minimo,Version Manager,Test Framework,Health Checks
## Concluido na Fase 1 (Fundacao, 2026-09-10:

- [x] `src/nexora/core/` — Objetivo, Plano/Tarefa,, Ciclo,, executar_ciclo() e ResultadoCiclo

- [x] `src/nexora/providers/` — registry dinamico,, base,, FakeProvider,, pronto para Groq/Conectores (
- [x] `src/nexora/tools/registry.py` — Ferramenta + RegistryFerramentas (
- [x] `src/nexora/config/loaders.py` — JSON + ambiente ( prefixo NEXORA_)
- [x] `src/nexora/runtime/` — logs estruturados,, memoria(( episodica/semantica), verificacao( saida), sandbox( allowlist de comandos (
- [x] 30 testes unitarios passando( pytest) em tests/unit (
- [x] Empacotamento pyproject + CLI minimo( python -m nexora)

## Proxima ( Fase 2 — Providers & Conectores, apos aprovacao explicita:

- [ ] Receber aprovacao do analista/coordenador para iniciar a Fase  2
- [ ] Estender o contrato tipado de provider ( base.py); manter registry dinamico verde

- [ ] Implementar Provider Groq( API real com stdlib, sem dependencia pip;erros tipados( ProviderSemCredencial, ProviderIndisponivel)
- [ ] FakeProvider deterministico com estado auditavel
- [ ] Testes: test_providers_groq.py + ampliar test_providers_registry.py


## Concluido na Fase 2 ( Providers & Conectores,2026-09-10:

- [x] Contrato tipado em providers/base.py( generate/stream/saudavel/fechar,excecoes ProviderSemCredencial/ProviderIndisponivel]
- [x] ProviderGroq implementado( stdlib urllib.request,GROQ_API_KEY,NEXORA_GROQ_MODEL default llama-3.3-70b-versatile,erros HTTP tipados)

- [x] FakeProvider com estado auditavel( chamadas registradas;fechar limpa historico)

- [x] RegistryProviders 100% verdes e ampliado( disponiveis ordenados/substituicao deleta nome)

- [x] 13 novos testes( test_providers_groq.py/test_providers_fake.py/registry ampliado) — suite completa 43 passed,0 failed} 返回

## Proxima — Fase 3 ( Orquestracao de Agente, aguardando comando do analista:

- [ ] Receber aprovacao/comando para a Fase  3 em NEXT_COMMAND.md
- [ ] Definir loop de orquestracao( agente que recebe objetivo,planeja,executa,verifica)
- [ ] Integrar providers ao ciclo de execucao( roteamento de modelo por tarefa/objetivo)
- [ ] Definir contratos de evento/sandbox/verificacao para o fluxo completo
