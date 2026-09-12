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
- O roadmap pós-v1.0 está formalizado em `PROJECT_MEMORY/07_ROADMAP.md` nas Fases 17–25.
- O último CI correspondente ao HEAD deve ser confirmado antes de iniciar a Fase 17. Não declarar CI como OK sem run correspondente bem-sucedido.

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

## 5. Trabalho implementado e preservado
- AgentRuntime é o proprietário do ciclo `EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR`.
- ExecutionTrace transporta contexto estruturado sem inventar métricas.
- Orchestrator encaminha tarefas para AgentRuntime e ferramentas para Registry.
- Idempotência mínima está integrada ao caminho governado de ferramentas.
- Long-Term Autonomy da Fase 16 permanece concluída e não deve ser substituída.

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

## 7. Direção de desenvolvimento — Fase 17 em diante
A sequência oficial inicial está em `PROJECT_MEMORY/07_ROADMAP.md`:

1. **Fase 17 — Local Intelligence Foundation:** OllamaProvider e inteligência local.
2. **Fase 18 — Coding Workspace Agent:** ferramentas governadas para workspace real.
3. **Fase 19 — Dev Loop + Programming Experience:** código → teste → erro → correção → reteste → experiência.
4. **Fase 20 — Code Knowledge + RAG:** conhecimento recuperável sobre código e histórico.
5. **Fase 21 — Intelligent Model Routing:** seleção de modelo/provider por tarefa, custo, risco e contexto.
6. **Fase 22 — Hardware & NEXORA Setup:** instalação e configuração simples conforme o hardware.
7. **Fase 23 — NEXORA UI / Experience Layer:** UI extremamente tecnológica/futurista/inovadora, mas simples e intuitiva.
8. **Fase 24 — Autonomous Product Engine:** aproximação do loop econômico completo.
9. **Fase 25 — Continuous Evolution:** evolução contínua governada.

### Visão de Provider local
O hardware-alvo atualmente considerado para o desenvolvimento local é Ryzen 5 5600 + ~16 GB DDR4 + Radeon RX 6600 8 GB. Isso orienta a escolha inicial de perfil local, mas **não deve ser codificado como requisito fixo da NEXORA**.

O perfil inicial recomendado é um modelo de código local quantizado na classe Qwen2.5-Coder 7B Q4, executado por runtime local compatível. A arquitetura deve continuar agnóstica a modelo e preparada para perfis menores/maiores.

Ollama é uma integração planejada, não uma dependência arquitetural obrigatória da NEXORA.

## 8. UI — requisito de produto
A UI final da NEXORA deve transmitir:
- tecnologia;
- futuro;
- inovação;
- inteligência;
- sensação de sistema vivo;

sem transformar isso em complexidade de uso.

**Regra de UX:** a complexidade deve ficar na arquitetura interna; a interface principal deve ser limpa, intuitiva e visualmente impactante.

A estética poderá usar elementos futuristas, estados de execução em tempo real, visualização de atividades, animações discretas e identidade premium, sempre subordinados à legibilidade e à facilidade de uso.

## 9. Testes — regra permanente
Para cada funcionalidade nova:
1. implementar;
2. criar/atualizar testes;
3. executar os testes relevantes;
4. adicionar integração quando houver cruzamento de componentes;
5. validar CI correspondente ao HEAD;
6. atualizar PROJECT_MEMORY;
7. registrar commit/handoff.

**Nunca confundir teste escrito com teste aprovado.**

## 10. Limites reais
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

## 11. O que NÃO fazer
- Não criar outra NEXORA.
- Não criar outro repositório.
- Não criar outro Runtime de execução.
- Não duplicar Permission, Policy, Checkpoint ou Tool Registry.
- Não apagar Long-Term Autonomy.
- Não transformar NEXORA em wrapper de Ollama/Aider/Continue/OpenHands ou outro produto externo.
- Não tratar sandbox como isolamento OS forte.
- Não tratar auditoria como histórico criptograficamente inviolável.
- Não chamar infraestrutura de autonomia completa antes de fechar o loop real do North Star.
- Não introduzir retry de efeito externo sem idempotência, autorização, precondições e verificação.
- Não preencher métricas com valores inventados.
- Não remover `core/ciclo.py` apenas porque a busca interna não encontrou consumidores adicionais.
- Não transformar a UI em um painel complexo apenas para parecer tecnológico.

## 12. Regra operacional
A cada avanço significativo:
`AUDITAR → DECIDIR → IMPLEMENTAR → TESTAR → ATUALIZAR PROJECT_MEMORY → COMMIT → PUSH → VERIFICAR CI → HANDOFF`.

O repositório deve permanecer sempre em estado reproduzível e documentado. O North Star é a direção; testes, arquitetura e GitHub são as evidências do estado real.
