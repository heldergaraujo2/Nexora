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
- CI Run #170 validou o HEAD `ec146cb797f35b6d30e98f7d0e8d36b93f344487` com conclusão `success`.
- Runs posteriores anteriores foram considerados no histórico, mas o HEAD atual ainda precisa de CI correspondente.
- Neste checkpoint: `97951898a217f1c92cb70ce5514216626b7adeea` registrou o contrato de idempotência; `bdbc467a5c8f2d3ceab668075823a948aa801275` tornou a reivindicação atomicamente identificável; `83b2341a1b21d92cabae755ac9b1cd90ba9df096` integrou a barreira ao Registry; `95e852ce71dfbf024bf16158d0fd1114b952ced0` integrou o Orchestrator; `837bf6edec575141bc7d14cb139f672de310d319` persistiu a chave explícita na Tarefa; `cb7cad491c2fdc7b9c933ed597bd71aaca83df45` adicionou testes de integração.
- **Não considerar o HEAD deste checkpoint validado até o CI correspondente concluir com sucesso.**

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
Idempotency (quando configurada para a operação)
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

## 4. ADRs de execução
### ADR-012
Arquivo: `docs/adr/ADR-012-orchestrator-agent-runtime.md`.

Decisões principais:
- Orchestrator = coordenador de alto nível.
- AgentRuntime = limite canônico do ciclo de execução.
- `core/ciclo.py` não deve ser removido por suposição.
- Migração incremental e orientada por testes.
- Uma tarefa não pode ser executada duas vezes por camadas concorrentes.
- Ferramentas continuam sujeitas a governança.
- Retry de efeitos externos exige idempotência/autorização.

### ADR-013
Arquivo: `docs/adr/ADR-013-ciclo-legado-inventario-consumidores.md`.

Resultado da revisão do ciclo legado:
- `src/nexora/orquestracao/orquestrador.py` usa `AgenteRuntime` no caminho normal e não importa o ciclo legado.
- `tests/unit/test_ciclo.py` é o consumidor interno explícito que preserva o contrato histórico.
- A busca atual não encontrou outras referências internas relevantes aos símbolos/caminho do ciclo.
- `src/nexora/core/ciclo.py` foi explicitamente marcado como legado/compatibilidade.
- A remoção ainda não está autorizada: consumidores externos não podem ser inferidos apenas pela busca interna.

### ADR-014
Arquivo: `docs/adr/ADR-014-idempotencia-efeitos-externos.md`.

Decisão:
- Idempotência é uma barreira explícita antes da execução de efeitos externos.
- A chave identifica a operação; o fingerprint identifica os parâmetros semânticos da operação.
- Reutilização com mesmo fingerprint não executa novamente.
- Reutilização com fingerprint diferente é conflito de integridade.
- Operação `IN_PROGRESS` não é executada novamente.
- Operação `FAILED` não recebe retry automático; retry futuro exige mecanismo explícito.
- O store atual é in-memory e concorrente; persistência durável/distribuída ainda não está implementada.

## 5. O que foi implementado neste checkpoint
### AgentRuntime / ExecutionTrace
- Exceções de execução e verificação são controladas como observações.
- O fluxo de análise/recovery continua `EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR`.
- `ResultadoAgente` transporta `trace` estruturado.
- `ExecutionTrace` registra IDs, agente/tarefa, provider/model, tokens, latência, custo, retry, falha, policy version/fingerprint, checkpoint, status e timestamps.

### Orchestrator
- Não usa mais `ExecutorCiclo`/`VerificadorCiclo` no caminho normal.
- Cada tarefa passa por um `AgenteRuntime`.
- O trace recebe contexto real disponível.
- Tarefas com ferramenta continuam passando pelo `RegistryFerramentas`.
- Retry automático de ferramenta continua limitado a uma tentativa nesta integração.
- Quando o Registry possui idempotência, tarefas de ferramenta recebem automaticamente uma chave estável `objetivo:tarefa:ferramenta`.
- O planner pode declarar `idempotencia_chave` explicitamente e a Tarefa preserva essa chave.
- Nenhum token/custo/modelo é inventado.

### Idempotência
- `src/nexora/runtime/idempotencia.py` fornece store concorrente em memória, fingerprint determinístico e estados `IN_PROGRESS`, `SUCCEEDED`, `FAILED`.
- `RegistryFerramentas` aceita `StoreIdempotenciaMemoria` opcional.
- A ordem canônica é `Permission → Policy → Checkpoint → Idempotency → Tool → Observation → Verification → Audit → Result`.
- Sem store configurado, o comportamento legado do Registry permanece preservado.
- Com store configurado, duplicidades não reexecutam a ferramenta.
- Falhas anteriores não são automaticamente repetidas.

### Ciclo legado
- `src/nexora/core/ciclo.py` permanece funcional e documentado como contrato legado/compatibilidade.
- Nenhum novo caminho de produção deve usá-lo para criar outro motor de execução.

## 6. Governança — NÃO QUEBRAR
Fluxo canônico:
`Pedido → Permission → Policy → Checkpoint → Idempotency → Tool → Observation → Verification → Audit → Result`

- Policy default DENY.
- Permission ocorre antes da ação.
- Checkpoint ocorre antes da ferramenta.
- Idempotência, quando habilitada, ocorre antes do efeito.
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
- Store de idempotência atual é em memória; não protege reinício de processo ou múltiplas instâncias.
- Não existe estratégia completa de recuperação de operações `IN_PROGRESS` após crash.
- Registry/capabilities são em memória.
- ExecutorDelegacoes é síncrono/in-memory.
- YAML de política não existe.
- World Model/Knowledge ainda são infraestrutura, não inteligência mundial completa.
- Economic Engine ainda não fecha o loop oportunidade → produto → mercado → receita → reinvestimento.
- Autonomia econômica completa ainda não existe.
- Groq ainda requer validação real HTTP/tool-calling antes de ser tratado como integração de produção validada.
- `ExecutionTrace` ainda não possui backend persistente/telemetria distribuída nem preenchimento universal de tokens/custo/policy/checkpoint.

## 9. Anomalia conhecida
`src/nexora/runtime/analise.py` já apresentou SHA inconsistente no tooling. **Não inventar SHA.** Se for necessário alterá-lo, resolver a identidade do blob primeiro.

## 10. Próximo trabalho
1. Confirmar CI correspondente ao HEAD atual em Python 3.11–3.14.
2. Se CI falhar, corrigir antes de avançar.
3. Auditar a superfície pública de `core/ciclo.py` antes de remoção/simplificação.
4. Adicionar integração de idempotência também ao caminho de execução que efetivamente recebe tarefas persistidas/repetidas, quando essa camada existir.
5. Evoluir o store de idempotência para persistência durável somente quando o runtime exigir recuperação após crash/múltiplas instâncias.
6. Não habilitar retry externo automaticamente; primeiro implementar precondições, autorização, recuperação e verificação explícitas.
7. Depois: evidência de pesquisa, economia computacional e evolução do World Model.

## 11. O que NÃO fazer
- Não criar outra NEXORA.
- Não criar outro repositório.
- Não criar nova fase sem necessidade arquitetural.
- Não duplicar Runtime, Permission, Policy, Checkpoint ou Tool Registry.
- Não apagar Long-Term Autonomy.
- Não tratar sandbox como isolamento OS forte.
- Não tratar auditoria como histórico criptograficamente inviolável.
- Não chamar infraestrutura de autonomia completa antes de fechar o loop real do North Star.
- Não introduzir retry de efeito externo sem idempotência, autorização, precondições e governança.
- Não preencher métricas de trace com valores inventados ou estimados sem evidência.
- Não remover `core/ciclo.py` apenas porque a busca interna não encontrou consumidores adicionais.

## 12. Regra operacional
A cada avanço significativo:
`AUDITAR → DECIDIR → IMPLEMENTAR → TESTAR → ATUALIZAR PROJECT_MEMORY → COMMIT → PUSH → VERIFICAR CI → HANDOFF`.

O repositório deve permanecer sempre em estado reproduzível e documentado. O North Star é a direção; testes, arquitetura e GitHub são as evidências do estado real.