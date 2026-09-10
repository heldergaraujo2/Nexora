# ADR-006 — Provider Groq: validar tool-calling antes de fixar

- Status: Aprovada ( condicional )
- Data:2026-09-10
- Decisao de origem: P6 (PROJECT_MEMORY/09_DECISIONS.md)
- Relacionamentos: ADR-001 (Python),ADRs de provider system( Fase  2 do roadmap)

## Contexto

O primeiro provider planejado e o Groq. Antes de fixar qual modelo/tool-calling/streaming usar,precisamos de verificacao real da API do Groq( disponibilidade de tool-calling no modelo escolhido,formato de tools,streaming,custo,rate limits,)porque isso determina o contrato `provider.schema.json` e a capacidade real do MVP( ver H1,H5,H7 na Capability Discovery)。

## Decisao

Nao fixar o modelo/tool-calling do Groq nesta fase. O ADR-006 sera **validado por um experimento controlado** na Fase  2( Provider System,( quando implementarmos a camada de Providers),realizando chamadas reais e registrando o resultado em `docs/adr/` como adenda( ou novo ADR)。 O contrato de provider( `docs/contracts/provider.schema.json`)sera desenhado agnosticamente,permitindo qualquer provider compativel( Groq,fake provider para testes,OpenRouter,LiteLLM,etc.。



## Consequencias

- Positivas: arquitetura nao fica refem de detalhes de um provider especifico;FakeProvider garantira testes deterministacis desde a Fase  2;troca de provider nao toca o nucleo( principio model-agnostico;
- Negativas: o MVP da Fase  2 depende de pivot de verificacao( sem isso,usar fake/fallback);exige credencial Groq no ambiente( via env var,gerenciada pelo credential broker,nao no repositorio;
- Neutras: o resultado da validacao podera mudar o contrato de tool-calling( adenda ao ADR ou ADR-012( se romper compatibilidade)。