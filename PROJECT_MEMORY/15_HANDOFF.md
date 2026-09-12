# 15 — HANDOFF

> **ARQUIVO PRINCIPAL DE CONTINUIDADE DA NEXORA.** Um novo chat/agente deve começar por este arquivo, confirmar o HEAD real do `main`, verificar o CI correspondente e somente depois continuar o desenvolvimento. GitHub é a fonte de verdade.

## 1. Identidade imutável do projeto
- Nome: **NEXORA**.
- Slogan oficial: **“NEXORA — Encontre oportunidades. Crie valor. Gere recursos.”**
- North Star longa: “Construir uma inteligência artificial capaz de aprender continuamente sobre o mundo, identificar oportunidades, criar valor através de produtos, serviços, software e inovação, transformar esse valor em recursos de forma legal e sustentável, e utilizar esses recursos para ampliar continuamente sua própria capacidade de criar ainda mais valor para seu criador.”
- North Star curta: “Criar valor continuamente para ampliar continuamente a capacidade de criar valor.”
- NEXORA é uma plataforma, não apenas um modelo de IA.
- Loop central: `OBSERVAR → PESQUISAR → ENTENDER → IDENTIFICAR OPORTUNIDADE → PLANEJAR → CRIAR → TESTAR → VALIDAR → LANÇAR → MEDIR → APRENDER → MELHORAR → GERAR RECURSOS → AMPLIAR CAPACIDADE → NOVA OPORTUNIDADE`.

## 2. Fonte de verdade e estado do Git
- Repositório: `heldergaraujo2/Nexora`.
- Branch oficial: `main`.
- Release histórica: `v1.0.0` → `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- Último HEAD de código executável validado: `d69e7c9947dfc79fdd51f28dae66e97a0d3e75f4`.
- Run #147 (`34659962617`) validou esse HEAD com **SUCCESS em Python 3.11, 3.12, 3.13 e 3.14**.
- Depois do Run #147 foram feitas apenas correções de qualidade e documentação: correção de warnings em `a608056d700519f2f62447f23c1148bd621c4be2` e atualizações dos arquivos de continuidade.
- **HEAD atual do repositório:** `51ac60e4b11b54d44148c3169d9470a72084dd06`.
- O HEAD atual não contém nova lógica de produção depois do `d69e7c...`; as mudanças posteriores são de qualidade/documentação.
- A versão do pacote permanece `1.0.0`; isso não significa que o código esteja parado na tag `v1.0.0`.

## 3. Etapa encerrada neste checkpoint
A etapa foi uma **reconciliação de consistência interna do Runtime dos agentes**. O objetivo foi corrigir a incompatibilidade entre o formato de observação produzido pelo runtime e o formato esperado pelo analisador, sem ainda fundir o Orchestrator ao Runtime.

### 3.1 Coding Agent
Arquivo: `src/nexora/agentes/coding.py`
- Usa `AgenteRuntime`.
- Usa `Observacao` estruturada no caminho de análise.
- Guarda o último erro de validação em `_ultimo_erro`.
- Transporta esse erro para `Observacao.erro` antes de `AnalisadorFalhas`.
- Se uma falha de validação for classificada como irreversível pelo analisador, o agente especializado a converte para `retry`, pois o problema pode ser corrigível por nova tentativa.
- Mantém verificação de saída não vazia e compilação de respostas que aparentam ser Python.

### 3.2 Research Agent
Arquivo: `src/nexora/agentes/pesquisa.py`
- Usa `AgenteRuntime`.
- Usa `Observacao` estruturada no caminho de análise.
- Guarda o último erro de validação em `_ultimo_erro`.
- Transporta esse erro para `Observacao.erro` antes de `AnalisadorFalhas`.
- Falhas de validação como saída vazia ou ausência de citação permanecem retentáveis no agente especializado.
- Mantém planejamento de consultas, coleta via ferramenta `buscar`, síntese baseada nas fontes e verificação mínima de citação.

### 3.3 Resultado
O ciclo interno do `AgenteRuntime` permanece:

`EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR`

Não foi criada uma terceira camada de execução e nenhum contrato validado foi removido.

## 4. Governança e execução de ferramentas — estado consolidado
O Registry de ferramentas implementa:

`Pedido → Permission → Policy → Checkpoint → Tool → Observation → Verification → Audit → Result`

Integração já validada com Orchestrator:

`Goal/Plan/Task → Orchestrator → Registry → Permission/Policy → Checkpoint → Tool → Observation → Verification → Audit → Result → Orchestrator`

Contratos importantes:
- autorização antes da ação;
- Policy com ALLOW/DENY e default DENY;
- decisão de política auditável;
- fingerprint SHA-256 canônico da semântica da política;
- `DENEGADA` distinta de `FALHOU`;
- `GerenciadorPermissoes` nunca executa a ação;
- checkpoint depois da autorização e imediatamente antes da ferramenta;
- falha de checkpoint impede a execução;
- Registry pode observar/verificar e produzir `ResultadoFerramenta`;
- auditoria do Registry não copia parâmetros nem resultado bruto potencialmente sensível;
- tarefas sem ferramenta continuam usando Provider;
- Sandbox mantém allowlist e pode exigir Policy antes de `subprocess.run`.

## 5. Policy / Governance
Arquivos:
- `src/nexora/governanca/policy.py`
- `src/nexora/governanca/policy_loader.py`
- `src/nexora/governanca/policy_manager.py`
- `src/nexora/governanca/permissoes.py`

Estado:
- `PolicyEngine` determinístico; primeira regra correspondente vence.
- Default DENY.
- Loader TOML versão 2, declarativo, estrito, com validação de campos, tipos e IDs únicos.
- Fingerprint canônico SHA-256.
- `GerenciadorPolitica` com reload validado e troca atômica; policy anterior é preservada se a nova for rejeitada.
- `PedidoPermissao` + `GerenciadorPermissoes` formam a fronteira de autorização.
- YAML ainda não implementado.

## 6. Checkpoint Engine
Arquivo: `src/nexora/runtime/checkpoint.py`
- `Checkpoint` identifica execução, estado lógico, motivo e timestamp UTC.
- Snapshot usa cópia profunda.
- Recuperação devolve nova cópia isolada.
- Listagem pode filtrar por `execucao_id`.
- Auditoria opcional via `RegistroAuditoria`.
- Não executa ferramentas.
- Não desfaz efeitos externos.
- Persistência durável e rollback externo ainda não fazem parte do MVP.

## 7. Comunicação, delegação e agentes
Arquivos principais:
- `src/nexora/comunicacao/bus.py`
- `src/nexora/comunicacao/delegacao.py`
- `src/nexora/agentes/registro.py`

Estado:
- CommunicationBus é transporte em memória.
- Delegação possui `SOLICITADA`, `ACEITA`, `CONCLUIDA`, `FALHOU`, `CANCELADA`, `DENEGADA`.
- `ExecutorDelegacoes` é síncrono/in-memory.
- Integração opcional com `AgenteRuntime` preserva o ciclo avançado.
- Recovery de delegação possui `max_tentativas`.
- Resultados terminais podem gerar experiência.
- Aceite, conclusão e falha podem ser auditados.
- Registry de agentes permite descoberta/seleção por capacidade.

## 8. Experiência, auditoria e continuidade
- `src/nexora/experiencia/registro.py`: experiências de resultados terminais.
- `src/nexora/auditoria/registro.py`: log append-only JSONL.
- `PROJECT_MEMORY/08_CURRENT_STATE.md`: estado operacional.
- `PROJECT_MEMORY/13_CHANGELOG.md`: histórico.
- `PROJECT_MEMORY/14_AGENT_PROTOCOL.md`: protocolo.
- `PROJECT_MEMORY/15_HANDOFF.md`: este checkpoint principal.
- `PROJECT_MEMORY/NEXT_COMMAND.md` e `NEXT_COMMAND.md`: orientação para a próxima sessão.

## 9. Long-Term Autonomy — NÃO QUEBRAR
A Fase 16 — Long-Term Autonomy está concluída e preservada.

Arquivo principal:
- `src/nexora/autonomia/registro.py`

Contratos preservados:
- `MetaLongoPrazo`.
- `RegistroAutonomia`.
- Persistência JSONL append-only.
- CLI `nexora autonomia definir|atualizar|listar|resumir`.

Não substituir a camada de autonomia para integrar componentes novos.

## 10. Validação
Run #147 (`34659962617`) no HEAD `d69e7c...`:
- Python 3.11 — SUCCESS.
- Python 3.12 — SUCCESS.
- Python 3.13 — SUCCESS.
- Python 3.14 — SUCCESS.
- Python 3.14: **232 passed, 2 warnings**.

Os 2 warnings eram `SyntaxWarning` nos testes do Policy Loader. Foram corrigidos em `a608056d700519f2f62447f23c1148bd621c4be2` usando regex raw. Os commits posteriores não alteraram código de produção.

O HEAD atual é documental/qualitativo em relação ao último código validado; o novo agente deve sempre verificar o CI do HEAD atual antes de começar código.

## 11. Lacunas reais
1. **Orchestrator ainda não usa `AgenteRuntime` como executor/verificador único.** Hoje existem os caminhos `Orquestrador → ExecutorCiclo → VerificadorCiclo` e `AgenteRuntime → EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR`. A integração final ainda precisa ser projetada para evitar duplicação.
2. `core/ciclo.py` permanece como caminho legado; existe uma anotação de `Callable` que merece revisão cuidadosa, sem mudança comportamental por suposição.
3. Checkpoints são em memória.
4. Não existe rollback de efeitos externos.
5. Registry/capabilities são em memória.
6. `ExecutorDelegacoes` é síncrono/in-memory.
7. YAML de políticas não existe.
8. O ciclo autônomo completo de planejamento multi-agente + economia + evolução ainda não está fechado.

## 12. Problema conhecido do tooling
`src/nexora/runtime/analise.py` apresenta uma anomalia registrada durante a auditoria: o SHA exposto pelo Git tree aparece com 39 caracteres (`285bc4258ce5966742130670c46cb8c8d3fe893b`), apesar de SHA-1 Git normalmente possuir 40. Uma tentativa de update com esse valor produziu conflito.

Regra:
- não inventar SHA;
- não repetir update cego nesse arquivo;
- se for necessário alterá-lo, confirmar primeiro a identidade do blob por Git Data/tree ou outra leitura confiável;
- enquanto isso, os agentes especializados já fazem a ponte necessária por `Observacao.erro`.

## 13. O que NÃO fazer
- Não criar uma segunda NEXORA.
- Não criar outro repositório.
- Não apagar/substituir Long-Term Autonomy.
- Não criar nova fase automaticamente.
- Não duplicar Permission/Policy/Checkpoint/Tool Registry/Runtime.
- Não transformar CheckpointEngine em executor.
- Não mover execução de ferramenta para PolicyEngine.
- Não acoplar Orchestrator, Provider e Tool em objeto monolítico.
- Não remover compatibilidade do caminho Provider para tarefas sem ferramenta.

## 14. Próximo trabalho arquitetural recomendado
**Reconciliar Orquestrador e Agent Runtime.**

Ordem obrigatória:
1. confirmar HEAD real do `main`;
2. verificar CI do HEAD;
3. ler este HANDOFF, `08_CURRENT_STATE.md` e `13_CHANGELOG.md`;
4. ler `src/nexora/orquestracao/orquestrador.py`, `src/nexora/core/ciclo.py`, `src/nexora/runtime/agente.py` e testes correspondentes;
5. mapear quem deve possuir execução, verificação, análise, correção, reteste e lifecycle;
6. preservar Registry como fronteira governada de ferramentas;
7. desenhar integração mínima, evitando dois ciclos de verificação sobre a mesma tarefa;
8. adicionar regressão + integração;
9. validar em Python 3.11–3.14;
10. atualizar continuidade somente depois da validação.

Arquitetura-alvo conceitual:

`Objetivo → Orchestrator → Plano/Tarefas → AgentRuntime → Permission/Policy/Checkpoint → Tool/Provider → Observation → Verification → Analysis → Correction/Recovery → Retest → Audit/Experience → Resultado`

Isso é direção arquitetural, não autorização para criar componentes redundantes.

## 15. Regra operacional para o novo chat
O novo chat deve assumir que:
- o projeto está além da tag `v1.0.0`;
- o estado real está no `main`;
- PROJECT_MEMORY faz parte da continuidade do sistema;
- o GitHub é mais confiável que qualquer resumo de conversa;
- o primeiro passo é sincronizar HEAD + CI;
- a próxima lacuna está explicitamente registrada neste arquivo;
- não é necessário criar uma nova fase para continuar.

**CHECKPOINT FINAL DESTA SESSÃO:** Runtime interno reconciliado; Coding Agent corrigido; Research Agent corrigido; governança de ferramentas fechada; Permission/Policy/Checkpoint/Observation/Verification/Audit/Result integrados no Registry; Orchestrator → Registry validado; warnings do Policy Loader corrigidos; Long-Term Autonomy preservada; documentação de continuidade atualizada; próximo trabalho definido como reconciliação Orchestrator ↔ AgentRuntime.
