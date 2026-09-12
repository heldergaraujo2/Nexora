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
- Branch de trabalho oficial: `main`.
- Release histórica: `v1.0.0` → `c49d3d2df314bb8c2d849c4466736f15841e8893`.
- Último HEAD antes do fechamento documental: `d69e7c9947dfc79fdd51f28dae66e97a0d3e75f4`.
- Run #147 (`34659962617`) validou esse HEAD com **SUCCESS em Python 3.11, 3.12, 3.13 e 3.14**.
- A partir dele foram feitas correções documentais e de qualidade sem mudança de arquitetura: `a608056d700519f2f62447f23c1148bd621c4be2`, `e16a2f7380782d7274b7db825445d2acd56f8985` e `8751c36369dab7982c5f877fb166c9d32e3ddcff`.
- **HEAD documental atual:** `8751c36369dab7982c5f877fb166c9d32e3ddcff`.
- O HEAD atual contém a correção dos warnings de regex e as atualizações de continuidade. O CI próprio do HEAD `8751c363...` deve ser confirmado antes de qualquer nova alteração de código.
- A versão do pacote permanece `1.0.0`; isso não significa que o código esteja parado na tag `v1.0.0`.

## 3. O que foi concluído nesta etapa
A etapa atual foi uma **reconciliação de consistência interna do Runtime dos agentes**. O objetivo foi corrigir a incompatibilidade entre o formato de observação produzido pelo runtime e o formato esperado pelo analisador, sem ainda fundir o Orchestrator ao Runtime.

### 3.1 Coding Agent
Arquivo: `src/nexora/agentes/coding.py`
- Usa `AgenteRuntime`.
- Usa `Observacao` estruturada no método `_analisar`.
- Guarda o último erro de validação em `_ultimo_erro`.
- Copia esse erro para `Observacao.erro` antes de chamar `AnalisadorFalhas`.
- Falhas de validação que o analisador classifica como irreversíveis são convertidas, dentro deste agente especializado, para `retry`, porque sintaxe/saída vazia são problemas potencialmente corrigíveis por nova tentativa.
- Mantém verificação de saída não vazia e compilação para respostas que aparentam ser Python.

### 3.2 Research Agent
Arquivo: `src/nexora/agentes/pesquisa.py`
- Usa `AgenteRuntime`.
- Usa `Observacao` estruturada no método `_analisar`.
- Guarda o último erro de validação em `_ultimo_erro`.
- Copia esse erro para `Observacao.erro` antes de chamar `AnalisadorFalhas`.
- Falhas de validação, como saída vazia ou ausência de citação, são mantidas como retentáveis neste agente especializado.
- Mantém planejamento de consultas, coleta via ferramenta `buscar`, montagem de prompt baseada nas fontes e verificação mínima de citação.

### 3.3 Resultado da reconciliação
O ciclo interno do `AgenteRuntime` continua:

`EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR`

Não foi criada uma terceira camada de execução e não foi removido nenhum contrato existente.

## 4. Governança e execução de ferramentas — estado consolidado
O Registry de ferramentas implementa:

`Pedido → Permission → Policy → Checkpoint → Tool → Observation → Verification → Audit → Result`

E o caminho já integrado ao Orchestrator é:

`Goal/Plan/Task → Orchestrator → Registry → Permission/Policy → Checkpoint → Tool → Observation → Verification → Audit → Result → Orchestrator`

Contratos importantes:
- autorização ocorre antes da ação;
- Policy tem ALLOW/DENY e default DENY;
- decisão de política é auditável;
- fingerprint da política é SHA-256 canônico da semântica;
- `DENEGADA` não é tratada como `FALHOU`;
- `GerenciadorPermissoes` nunca executa a ação, apenas autoriza/nega;
- checkpoint é criado depois da autorização e imediatamente antes da ferramenta;
- falha de criação de checkpoint fecha a operação antes da execução;
- `RegistryFerramentas` pode observar/verificar e gerar `ResultadoFerramenta`;
- auditoria do Registry não copia parâmetros nem resultado bruto potencialmente sensível;
- tarefas sem ferramenta preservam o caminho existente de Provider;
- Sandbox mantém allowlist e pode exigir Policy antes de `subprocess.run`.

## 5. Policy / Governance
Arquivos principais:
- `src/nexora/governanca/policy.py`
- `src/nexora/governanca/policy_loader.py`
- `src/nexora/governanca/policy_manager.py`
- `src/nexora/governanca/permissoes.py`

Estado:
- `PolicyEngine` mínimo e determinístico.
- Regras ordenadas; primeira regra correspondente vence.
- Default DENY.
- Loader TOML versão 2 com schema estrito, campos conhecidos, IDs únicos e validação de tipos.
- Fingerprint canônico SHA-256 independente da origem textual.
- `GerenciadorPolitica` permite reload validado e troca atômica; policy anterior permanece ativa quando a nova é rejeitada.
- `PedidoPermissao` + `GerenciadorPermissoes` formam a fronteira de autorização.
- YAML ainda não implementado.

## 6. Checkpoint Engine
Arquivo: `src/nexora/runtime/checkpoint.py`
- `Checkpoint` identifica execução, estado lógico, motivo e timestamp UTC.
- Snapshot usa cópia profunda.
- Recuperação devolve nova cópia isolada.
- Listagem pode filtrar por `execucao_id`.
- Auditoria opcional usa `RegistroAuditoria`.
- Não executa ferramenta.
- Não desfaz efeitos externos.
- Persistência durável ainda não implementada.
- Rollback externo ainda não implementado.
- O componente é deliberadamente um MVP em memória.

## 7. Comunicação e delegação
Arquivos:
- `src/nexora/comunicacao/bus.py`
- `src/nexora/comunicacao/delegacao.py`
- `src/nexora/agentes/registro.py`

Estado:
- CommunicationBus fornece transporte em memória.
- Delegação possui estados `SOLICITADA`, `ACEITA`, `CONCLUIDA`, `FALHOU`, `CANCELADA`, `DENEGADA`.
- `ExecutorDelegacoes` executa delegações recebidas de forma síncrona/in-memory.
- Integração opcional com `AgenteRuntime` preserva verificação, análise, correção e reteste.
- Recovery de delegação possui `max_tentativas`.
- Resultados terminais podem ser registrados em experiência.
- Auditoria registra aceite, conclusão e falha.
- Registry de agentes permite descoberta/seleção por capacidade.

## 8. Experiência, auditoria e continuidade
- `src/nexora/experiencia/registro.py`: experiências de resultados terminais.
- `src/nexora/auditoria/registro.py`: log append-only JSONL.
- `PROJECT_MEMORY/08_CURRENT_STATE.md`: estado operacional detalhado.
- `PROJECT_MEMORY/13_CHANGELOG.md`: histórico das mudanças arquiteturais.
- `PROJECT_MEMORY/14_AGENT_PROTOCOL.md`: protocolo de agente.
- `PROJECT_MEMORY/15_HANDOFF.md`: este checkpoint principal.
- `PROJECT_MEMORY/NEXT_COMMAND.md` e `NEXT_COMMAND.md`: orientação de continuidade.

## 9. Long-Term Autonomy — NÃO QUEBRAR
A Fase 16 — Long-Term Autonomy está concluída e deve ser preservada.

Arquivo principal:
- `src/nexora/autonomia/registro.py`

Contratos preservados:
- `MetaLongoPrazo`.
- `RegistroAutonomia`.
- Persistência JSONL append-only.
- CLI `nexora autonomia definir|atualizar|listar|resumir`.

Não substituir a camada de autonomia por uma implementação nova apenas para integrar novos componentes.

## 10. Validação atual
Run #147 (`34659962617`) no HEAD `d69e7c9947dfc79fdd51f28dae66e97a0d3e75f4`:
- Python 3.11 — SUCCESS.
- Python 3.12 — SUCCESS.
- Python 3.13 — SUCCESS.
- Python 3.14 — SUCCESS.
- Python 3.14 executou **232 passed, 2 warnings**.

Os dois warnings eram `SyntaxWarning` nos testes do Policy Loader por escapes inválidos em regex. O commit `a608056d700519f2f62447f23c1148bd621c4be2` substituiu as expressões por regex raw. Os commits seguintes atualizaram apenas documentação de continuidade. Portanto, o próximo agente deve verificar o CI do HEAD documental atual antes de concluir que o checkpoint está verde.

## 11. Lacunas reais — NÃO CONFUNDIR COM BUGS JÁ CORRIGIDOS
1. **Orchestrator ainda não usa `AgenteRuntime` como executor/verificador único.**
   - Hoje há `Orquestrador → ExecutorCiclo → VerificadorCiclo`.
   - Separadamente existe `AgenteRuntime → EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR`.
   - A integração final ainda deve ser projetada e testada.
2. `core/ciclo.py` permanece como caminho legado e tem uma anotação de `Callable` suspeita que deve ser revisada com cuidado, sem alterar comportamento por suposição.
3. Checkpoints são apenas em memória.
4. Não existe rollback de efeitos externos.
5. Registry/capabilities são em memória.
6. ExecutorDelegacoes é síncrono/in-memory.
7. YAML de políticas não existe.
8. O ciclo autônomo completo de planejamento multi-agente + economia + evolução ainda não está fechado.

## 12. Problema conhecido de ferramenta de desenvolvimento
Durante a auditoria foi observado que o SHA retornado pelo conector para `src/nexora/runtime/analise.py` aparece como `285bc4258ce5966742130670c46cb8c8d3fe893b`, com 39 caracteres, apesar do Git tree também refletir esse valor. Isso é anômalo para SHA-1 Git.

Regra para o próximo agente:
- não inventar SHA;
- não repetir updates cegos nesse arquivo;
- se for necessário alterá-lo, primeiro resolver/confirmar a identidade do blob por Git Data/tree ou outra leitura confiável;
- enquanto isso, os agentes especializados já fazem a ponte correta por `Observacao.erro` e não exigem alteração desse arquivo.

## 13. O que NÃO fazer no próximo passo
- Não criar uma segunda NEXORA.
- Não criar outro repositório.
- Não apagar ou substituir Long-Term Autonomy.
- Não criar uma nova fase apenas para organizar a integração.
- Não duplicar Permission/Policy/Checkpoint/Tool Registry.
- Não transformar CheckpointEngine em executor.
- Não mover execução de ferramenta para o PolicyEngine.
- Não acoplar diretamente Orchestrator, Provider e Tool em um objeto monolítico.
- Não remover compatibilidade do caminho Provider para tarefas sem ferramenta.

## 14. Próximo trabalho arquitetural recomendado
**Reconciliar Orchestrator e Agent Runtime.**

Antes de implementar:
1. confirmar `main` e HEAD;
2. verificar CI do HEAD;
3. ler `src/nexora/orquestracao/orquestrador.py`, `src/nexora/core/ciclo.py`, `src/nexora/runtime/agente.py` e testes correspondentes;
4. mapear exatamente quem deve possuir execução, verificação, análise, correção, reteste e lifecycle;
5. preservar o Registry como fronteira de ferramenta governada;
6. desenhar uma integração mínima, evitando dois ciclos de verificação sobre a mesma tarefa;
7. adicionar testes de regressão e integração;
8. rodar CI em Python 3.11–3.14;
9. atualizar este HANDOFF, `08_CURRENT_STATE.md` e `13_CHANGELOG.md` somente após a validação.

Arquitetura-alvo conceitual:

`Objetivo → Orchestrator → Plano/Tarefas → AgentRuntime → Permission/Policy/Checkpoint → Tool/Provider → Observation → Verification → Analysis → Correction/Recovery → Retest → Audit/Experience → Resultado`

Isso é uma direção arquitetural, não autorização para introduzir componentes redundantes.

## 15. Regra operacional para novo chat/agente
O novo chat deve assumir que:
- o projeto já está implementado além da tag `v1.0.0`;
- o código atual é o `main` e deve ser lido do GitHub;
- os documentos deste diretório são parte do sistema de continuidade;
- nenhum detalhe desta mensagem deve ser tratado como mais confiável que o estado real do GitHub;
- o primeiro passo é sincronizar mentalmente com o HEAD e CI atuais;
- depois deve continuar exatamente da lacuna arquitetural registrada acima.

**Checkpoint:** Runtime interno reconciliado; governança de ferramentas fechada e validada; Coding/Research Agent corrigidos; warnings do Policy Loader corrigidos; documentação de continuidade atualizada; integração final Orchestrator ↔ AgentRuntime permanece como próximo trabalho.
