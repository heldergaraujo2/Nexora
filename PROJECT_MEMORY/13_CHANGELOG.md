# 13 — CHANGELOG

## 2026-09-10 — Integração de repositório e coordenação

- **Integração das duas linhas de história:**
  - Capability Discovery do agent construсor(02–05) integrada ao fluxo canônico
  - Numeração canônica única aplicada(00–15:00–05 = Identidade/North Star/Discovery;06–15 = infraestrutura)
  - 00_IDENTITY e 01_NORTH_STAR fundidas(nossa base + princípios e referências do agent)
- **Decisões de coordenação registradas** em 09_DECISIONS.md
- **Propostas A–E de alteração do roadmap aprovadas**( validadas pelo coordenador;autonomia delegada pelo criador)

- **P1–P11 recomendados provisoriamente**( arquitetura:Python,src/nexora/,CLI,JSON memória,append-only JSON,etc.)— para formalização na Fase  0.5
- **Estado atualizado** em 08_CURRENT_STATE.md e 11_TASKS.md
- **15_HANDOFF atualizado** com novo ponto de continuação(Fase 0.5—Decisão e Design)

## 2026-09-10 — Fase 0( esqueleto inicial)

- Estrutura de diretórios( src/,tests/,docs/,PROJECT_MEMORY/)
- 12 arquivos de memória originais( nossa Fase  0):00–11
- README,.gitignore
- Commits iniciais( 503c7d2,d912905 na branch master erefundidos no histórico unificado via integração)



##2026-09-10 — Capability Discovery( do agent construсor;

- Commit `0e271d9` —"docs: Capability Discovery(fase pre-implementacao)"
- 6 arquivos:00/01 versionados do agent;02_CAPABILITY_DISCOVERY(≈1.250 linhas,13 categorias);03_CAPABILITY_MATRIX;04_ARCHITECTURE_REQUIREMENTS;5_DISCOVERY_HANDOFF始 início do handoff da Discovery))
## 2026-09-10 — Fase 0.5 concluida — Decisao e Design
 
- 11 ADRs criados e aprovados em docs/adr/ (ADR-001..011) formalizam P1-P11
- Indice de ADRs em docs/adr/README.md
- 8 contratos JSON Schema criados e VALIDADOS em docs/contracts/ (objetivo,plano,provider,evento,tool,delegacao,memoria,aprovacao)
- Design doc criado em docs/design/repositorio.md que propoe estrutura,modulos e fluxo
- Canal construidor-analyiso estabelecido e testado (palavra HELLO confirmada;CANAL_CONSTRUTOR.md criado)
- Caracteres zero-width/CJK removidos de todos os docs e schemas
- Schemas JSON corrompidos pelo canal regenerados com echo linha-a-linha
## 2026-09-10 — Fase 1 concluida — Fundacao ( commit e73a266:

- Nucleo do agente: `core/objetivo.py`, `core/plano.py`, `core/ciclo.py` ( Objetivo, Plano/Tarefa, Ciclo, Executor, Verificador, executar_ciclo, ResultadoCiclo(
- Providers: `providers/base.py`, `providers/registry.py`, `providers/fake.py` ( contracto tipado, fake deterministico, registry dinamico com ProviderDesconhecido(
- Ferramentas: `tools/registry.py` ( Ferramenta + RegistryFerramentas(
- Config: `config/loaders.py` ( JSON + ambiente com prefixo NEXORA_(
- Runtime: `runtime/logs.py`, `runtime/memoria.py`, `runtime/verificacao.py`, `runtime/sandbox.py` ( logs estruturados, memoria episodica/semantica, verificacao de saida, sandbox com allowlist(
- 30 testes unitarios passando em `tests/unit/` ( commit pushado para origin/main(


## 2026-09-10 — Fase 2 concluida — Providers & Conectores

- `providers/base.py`: contrato tipado estendido( generate/stream/saudavel/fechar;excecoes ProviderSemCredencial e ProviderIndisponivel)
- `providers/registry.py`: registry dinamico inalterado( 100% testes verdes)
- `providers/fake.py`: estado auditavel( chamadas registradas;fechar/limpar)
- `providers/groq.py` NOVO: Provider Groq com stdlib( urllib.request;GROQ_API_KEY;NEXORA_GROQ_MODEL default llama-3.3-70b-versatile; erros HTTP mapeados para ProviderSemCredencial/ProviderIndisponivel)
- `providers/__init__.py`: exporta ProviderGroq/FakeProvider/excecoes tipadas}
- Testes: 13 novos filtros em tests/unit/test_providers_groq.py,test_providers_fake.py e ampliacao do registry)
- Suite completa: 43 passed,0 failed}
