# 15 — HANDOFF

> **ARQUIVO PRINCIPAL DE CONTINUIDADE DA NEXORA.** GitHub é a fonte de verdade. Um novo agente deve confirmar o HEAD real de `main` e o CI correspondente antes de continuar.

## 1. Identidade imutável
- Nome: **NEXORA**.
- Slogan: **“NEXORA — Encontre oportunidades. Crie valor. Gere recursos.”**
- North Star longa: “Construir uma inteligência artificial capaz de aprender continuamente sobre o mundo, identificar oportunidades, criar valor através de produtos, serviços, software e inovação, transformar esse valor em recursos de forma legal e sustentável, e utilizar esses recursos para ampliar continuamente sua própria capacidade de criar ainda mais valor para seu criador.”
- North Star curta: “Criar valor continuamente para ampliar continuamente a capacidade de criar valor.”
- NEXORA é uma plataforma, não apenas um modelo de IA.
- Loop central: `OBSERVAR → PESQUISAR → ENTENDER → IDENTIFICAR OPORTUNIDADE → PLANEJAR → CRIAR → TESTAR → VALIDAR → LANÇAR → MEDIR → APRENDER → MELHORAR → GERAR RECURSOS → AMPLIAR CAPACIDADE → NOVA OPORTUNIDADE`.

## 2. Fonte de verdade
- Repositório: `heldergaraujo2/Nexora`.
- Branch oficial: `main`.
- Release histórica: `v1.0.0` → `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- CI Run #164 validou o checkpoint anterior `b8b4619...` em Python 3.11–3.14.
- Desde então: `7bbdebcee7cf0b954b5e01eb1067f5e6b0d439bf` adicionou o teste de governança explícita de ferramenta; `4dabb383fd93e0e9c49d9d23f693049aa7eb8221` adicionou `ExecutionTrace`; `c5be9193086bab190180093351211b2e133c5375` adicionou testes unitários do trace; `55920a19d7f581c8f8007ddc86a76961510e0bd6` integrou o trace ao AgentRuntime; `3d07a437664ca43f2194a33a098787da7830ca64` adicionou teste do trace no runtime.
- **Não considerar os commits posteriores ao Run #164 validados até o CI do HEAD atual concluir com sucesso.**

## 3. Arquitetura canônica atual

```text
Objetivo
  ↓
Orchestrator
  ↓
Plano / Tarefas
  ↓
Seleção do executor/agente
  ↓
AgentRuntime  ← proprietário do ciclo avançado
  ↓
Permission / Policy / Checkpoint
  ↓
Provider ou Tool
  ↓
Observation
  ↓
Verification
  ↓
Analysis
  ↓
Correction / Recovery
  ↓
Retest
  ↓
Audit / Experience
  ↓
ExecutionTrace
  ↓
Resultado
  ↓
Orchestrator
```

### Regra fundamental
**Não criar um terceiro ciclo de execução.** O Orchestrator coordena; o AgentRuntime executa o ciclo do agente. `core/ciclo.py` permanece legado/compatibilidade até migração segura.

## 4. ADR-012
Arquivo: `docs/adr/ADR-012-orchestrator-agent-runtime.md`.

Decisões:
- Orchestrator = coordenador de alto nível.
- AgentRuntime = limite canônico do ciclo de execução.
- `core/ciclo.py` não deve ser removido por suposição.
- Migração incremental e orientada por testes.
- Uma tarefa não pode ser executada duas vezes por camadas concorrentes.
- Ferramentas continuam sujeitas a `Permission → Policy → Checkpoint → Tool → Observation → Verification → Audit → Result`.
- Retry de efeitos externos exige idempotência/autorização; a primeira integração não adiciona retry externo implícito.

## 5. O que foi implementado neste checkpoint
### AgentRuntime
- Exceções de execução agora viram `Observacao` com erro.
- Exceções de verificação também são controladas como observação.
- O fluxo de análise/recovery continua `EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR`.
- `ResultadoAgente` agora pode transportar um `trace` estruturado.
- `ExecutionTrace` foi introduzido em `src/nexora/runtime/trace.py` com IDs de execução/trace/span, agente/tarefa, provider/model, tokens, latência, custo, retry, falha, policy version/fingerprint, checkpoint, status e timestamps.
- O runtime gera/atualiza o trace, contabiliza retries e finaliza o status de forma determinística.

### Orchestrator
- Não usa mais `ExecutorCiclo`/`VerificadorCiclo` no caminho normal.
- Cada tarefa passa por um `AgenteRuntime`.
- Provider continua executando tarefas sem ferramenta.
- Tarefas com ferramenta continuam passando pelo `RegistryFerramentas`.
- Retry automático de ferramenta está limitado a uma tentativa nesta primeira integração para não repetir efeitos externos sem idempotência.
- Resultado do runtime é normalizado para o contrato do Orchestrator e preserva tentativas/histórico.

### Governança
- O teste `test_orquestrador_ferramenta_passa_uma_vez_pela_governanca` valida Orchestrator → Registry → Permission/Policy → Checkpoint → Tool e confirma uma única execução.

### Testes
Arquivos:
- `tests/integration/test_orquestrador_agent_runtime.py`
- `tests/unit/test_execution_trace.py`
- `tests/unit/test_agente_runtime_trace.py`

Os testes cobrem recovery do provider, exceção controlada, execução única governada de ferramenta e contrato do ExecutionTrace.

## 6. Governança — NÃO QUEBRAR
Fluxo canônico:
`Pedido → Permission → Policy → Checkpoint → Tool → Observation → Verification → Audit → Result`

- Policy default DENY.
- Permission ocorre antes da ação.
- Checkpoint ocorre antes da ferramenta.
- Registry é o executor governado da ferramenta.
- Orchestrator não deve executar ferramenta contornando o Registry.
- Sandbox é governança/controle de subprocesso, não isolamento OS forte.
- Auditoria JSONL é append-only por convenção, não prova criptográfica de imutabilidade.

## 7. Long-Term Autonomy — NÃO QUEBRAR
A Fase 16 está concluída e preservada.

Arquivo principal: `src/nexora/autonomia/registro.py`.

Não substituir essa camada para integrar novos componentes. A integração atual deve aproximar a NEXORA do North Star, não reduzir sua capacidade de autonomia futura.

## 8. Limites reais
- Checkpoints são em memória.
- Não existe rollback de efeitos externos.
- Não existe camada completa de idempotência externa.
- Registry/capabilities são em memória.
- ExecutorDelegacoes é síncrono/in-memory.
- YAML de política não existe.
- World Model/Knowledge ainda são infraestrutura, não inteligência mundial completa.
- Economic Engine ainda não fecha o loop oportunidade → produto → mercado → receita → reinvestimento.
- Autonomia econômica completa ainda não existe.
- Groq ainda requer validação real HTTP/tool-calling antes de ser tratado como integração de produção validada.
- `ExecutionTrace` é contrato de observabilidade; ainda não há backend persistente/telemetria distribuída nem preenchimento universal de tokens/custo/policy/checkpoint.

## 9. Anomalia conhecida
`src/nexora/runtime/analise.py` já apresentou SHA inconsistente no tooling. **Não inventar SHA.** Se for necessário alterá-lo, resolver a identidade do blob primeiro.

## 10. Próximo trabalho
1. Confirmar CI do HEAD que inclui o ExecutionTrace.
2. Se CI falhar, corrigir antes de avançar.
3. Integrar `ExecutionTrace` progressivamente no Orchestrator, preenchendo `task_id` e contexto de provider quando disponíveis, sem inventar dados.
4. Revisar o contrato de `core/ciclo.py` e seus consumidores; somente depois decidir aposentadoria gradual.
5. Evoluir `ExecutionTrace` para spans/eventos e persistência somente quando houver necessidade real, mantendo o contrato atual compatível.
6. Depois: idempotência externa, evidência de pesquisa, economia computacional e evolução do World Model.

## 11. O que NÃO fazer
- Não criar outra NEXORA.
- Não criar outro repositório.
- Não criar nova fase sem necessidade arquitetural.
- Não duplicar Runtime, Permission, Policy, Checkpoint ou Tool Registry.
- Não apagar Long-Term Autonomy.
- Não tratar sandbox como isolamento OS forte.
- Não tratar auditoria como histórico criptograficamente inviolável.
- Não chamar infraestrutura de autonomia completa antes de fechar o loop real do North Star.
- Não introduzir retry de efeito externo sem idempotência e governança.
- Não preencher métricas de trace com valores inventados ou estimados sem evidência.

## 12. Regra operacional
A cada avanço significativo:
`AUDITAR → DECIDIR → IMPLEMENTAR → TESTAR → ATUALIZAR PROJECT_MEMORY → COMMIT → PUSH → VERIFICAR CI → HANDOFF`.

O repositório deve permanecer sempre em estado reproduzível e documentado. O North Star é a direção; testes, arquitetura e GitHub são as evidências do estado real.
