# 09 — DECISIONS

## Decisões de Coordenação(Tomadas em 2026-09-10)

| # | Data | Decisão | Justificativa | Status |
|---|------|---------|-------------|--------|
| D01 | 2026-09-10 | Iniciar implementação pela Fase 0(Continuidade e Memória) | Roadmap define que NEXORA não deve depender do histórico de conversas; GitHub é source of truth | Aprovada |
| D02 |1868 2026-09-10 | GitHub como fonte de verdade(source of truth) | Seção 5 do roadmap | Aprovada |
| D03 |2522 2026-09-10 | `15_HANDOFF.md` será o principal arquivo de continuidade | Seção 5 do roadmap | Aprovada |
| D04 |3229 2026-09-10 | Reconciliar a numeração do PROJECT_MEMORY para linha única canônica(00–15:) | 02–05 = Capability Discovery(do agent);06–15 = infraestrutura(nossa Fase 0) — elimina conflito entre as duas histórias | Aprovada(autonomia delegada pelo criador) |
| D05 | Reconciliar 00_IDENTITY e 01_NORTH_STAR(nossa base + contribuições do agent) | As versões do agent têm princípios valiosos("North Star não congelada","criação de valor em cadeia",referências de engenharia) | Aprovada(autonomia delegada pelo criador) |
| D06 | Integrar a Discovery do agent(02–05) ao fluxo canônico | Capability Discovery é pré-requisito da Fase 1(Fundação) | Aprovada(autonomia delegada pelo criador) |
| D07 | Criar `NEXT_COMMAND.md` como canal de comando da coordenação | Permite ao coordenador auditar/redigir comandos que o agent construtor executa(filename versionado,auditável,revisável) | Aprovada |

## Propostas A–E de Alteração do Roadmap(Aprovadas pelo criador em 2026-09-10,vía autonomia delegada;validadas pelo coordenador)

| Prop. | Alteração | Veredito | Justificativa |
|--------|---------|---------|--------------|
| A | Coding/Research/Experience são papéis de agente/ferramenta sobre núcleo único(não subsistemas independentes) | **Aprovada** | Reduz duplicação arquitetural;núcleo model-agnóstico único |
| B | Segurança/Governança como requisito transversal desde a Fase técnica(não fase tardia) | **Aprovada** | Contenção deve vir com a primeira execução |
| C | Experimentação/benchmarking antecipados(mesmo simples,)para governar providers/prompts | **Aprovada** | Governa escolhas sem rework |
| D | Economic Engine:participação humana sempre em decisões legais/contratuais(invariante) | **Aprovada** | Alinhamento ao criador e legalidade |
| E | Auto-expansão sempre gateada por revisão humana( exceto mudanças triviais delegadas) | **Aprovada** | Evita auto-modificação descontrolada |

## Decisões P1–P11(Recomendações do Coordenador — validadas provisoriamente;ratificação final pendente do criador)

| Cód. | Decisão | Veredito provisório | Impacto |
|------|---------|---------|--------|
| P1 | Linguagem/ecossistema | **Python** | Ecossistema de IA/tooling maduro |
| P2 | Estrutura/namespace | **`src/nexora/`**(layout moderno) | Separa código de config,testável |
| P3 | Interface de entrada do MVP | **CLI** primária(+ SDK Python depois) | Mínimo,scriptável,testável |
| P4 | Backend inicial de memória | **JSON versionado** | Simples e auditável via git;evoluir p/ SQLite/vetorial |
| P5 | Backend do event store | **Append-only JSON** | Alinhado ao "tudo é evento";evoluir p/ SQLite/WAL |
| P6 | Groq: modelo e tool-calling | **Validar tool-calling no modelo Groq disponível** | Depende de verificação real da API antes de fixar |
| P7 | Sandbox do MVP | **subprocess isolado**(+ bubblewrap se disponível) | Leve,sem Docker no MVP;Docker depois |
| P8 | Ângulo do MVP | **Codificação**(agente de software) | Valor tangível e testável já |
| P9 | Onde vive a política | **Config declarativo versionado**(TOML/YAML) | Auditável,diffável,sem banco/UI no MVP |
| P10 | Multi-agente no MVP | **Não** — orchestrator monolítico+contratos prontos | Reduz risco;registry define evolução |
| P11 | Observabilidade | **Logs estruturados JSON** rotativos | Simples;OTel depois |

## ADRs de Arquitetura(Pendentes — Fase 0.5)

> As decisões P1–P11 acima serão formalizadas como ADRs( Architecture Decision Records) na Fase  0.5( Decisão e Design), em `docs/adr/`( ou seção própria neste arquivo), com data, contexto e consequências.. Este registro é o rascunho provisório.



## Regras de Decisão

- Não avançar grandes etapas ignorando falhas conhecidas(Protocolo de Desenvolvimento,14_AGENT_PROTOCOL.md)
- Ações financeiras e legais sensíveis exigem autorização explícita(12 e  34 do roadmap;Proposta D acima)
- NEXORA nunca deve afirmar que um produto possui capacidade que ele não possui(Regra de Veracidade,seção 19 do roadmap)