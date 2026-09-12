# ADR-012 — Orchestrator como coordenador e AgentRuntime como limite de execução

**Data:** 2026-09-12  
**Status:** Aprovada para implementação incremental

## Contexto

A NEXORA atualmente possui dois caminhos de execução:

```text
Orquestrador → ExecutorCiclo → VerificadorCiclo
```

e

```text
AgenteRuntime → EXECUTAR → VERIFICAR → ANALISAR → CORRIGIR → RETESTAR
```

Os dois caminhos são válidos isoladamente e possuem testes, mas representam responsabilidades sobrepostas. O Orchestrator deve coordenar objetivos, planos, tarefas, roteamento e resultados; o ciclo avançado de execução de um agente deve possuir um único proprietário.

A integração não pode criar um terceiro ciclo, nem pode executar novamente uma ferramenta externa durante uma recuperação sem passar novamente pelas fronteiras de autorização, política, checkpoint e demais controles.

## Decisão

1. `Orquestrador` será o coordenador de alto nível.
2. `AgenteRuntime` será o limite canônico do ciclo de execução de um agente quando a tarefa for delegada a um agente com ciclo avançado.
3. `core/ciclo.py` permanecerá como contrato de compatibilidade durante a migração; não será removido nem alterado por suposição.
4. A migração será incremental e orientada por testes: primeiro contratos e adaptadores, depois integração do Orchestrator.
5. Uma tarefa não poderá ser executada duas vezes por camadas concorrentes de execução/verificação.
6. Tarefas com ferramentas e efeitos externos manterão a fronteira `Permission → Policy → Checkpoint → Tool → Observation → Verification → Audit → Result`.
7. Recovery/retry de efeitos externos não poderá reutilizar automaticamente uma ação sem considerar idempotência e autorização. O primeiro passo da integração não introduzirá retry externo implícito.
8. O resultado produzido pelo runtime deverá ser adaptável ao contrato de resultado do Orchestrator sem duplicar execução.

## Arquitetura-alvo

```text
Objetivo
   ↓
Orchestrator
   ↓
Plano / Tarefas
   ↓
Seleção do executor/agente
   ↓
AgentRuntime   ← único ciclo de execução do agente
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
Resultado
   ↓
Orchestrator
```

## Estratégia de implementação

### Etapa 1 — contratos

- Mapear os contratos atuais de `Orquestrador`, `Executor`, `Verificador`, `AgenteRuntime`, `ResultadoCiclo` e `ResultadoAgente`.
- Definir o menor adaptador necessário para permitir que o Orchestrator consuma um runtime sem conhecer seus detalhes internos.
- Preservar compatibilidade dos contratos públicos existentes.

### Etapa 2 — integração sem efeitos externos

- Integrar primeiro tarefas executadas por Provider/agente sem ferramenta externa.
- Garantir que execução, verificação, análise, correção e reteste pertençam ao `AgentRuntime`.
- O Orchestrator apenas coordena e consolida o resultado.

### Etapa 3 — ferramentas governadas

- Integrar tarefas com `RegistryFerramentas` sem mover a responsabilidade de autorização.
- Garantir que cada execução de ferramenta passe pelas fronteiras de governança existentes.
- Não adicionar retry automático de ferramenta nesta etapa.

### Etapa 4 — aposentadoria gradual do ciclo duplicado

- Após cobertura de integração e compatibilidade, reduzir o uso de `ExecutorCiclo`/`VerificadorCiclo` pelo Orchestrator.
- Manter `core/ciclo.py` enquanto houver consumidores/testes legítimos.
- Só remover ou simplificar contratos após evidência de que não há dependências.

## Não objetivos desta ADR

- Não implementar persistência de checkpoint.
- Não implementar rollback de efeitos externos.
- Não implementar fila distribuída.
- Não implementar autonomia econômica completa.
- Não substituir Long-Term Autonomy.
- Não introduzir um terceiro runtime de execução.

## Consequências

### Positivas

- Um único proprietário do ciclo avançado de execução.
- Menor risco de verificações ou execuções duplicadas.
- Base clara para delegação multiagente futura.
- Governança permanece transversal e não é contornada pela integração.
- Migração pode ocorrer sem quebrar os contratos existentes.

### Custos

- Será necessário criar adaptadores e testes de integração.
- `core/ciclo.py` continuará temporariamente como compatibilidade.
- O resultado do runtime precisará ser normalizado para o contrato de orquestração.

## Critério de conclusão

A integração desta ADR só será considerada concluída quando testes demonstrarem que:

1. o Orchestrator consegue selecionar e executar um AgentRuntime;
2. cada tarefa é executada uma única vez pelo caminho escolhido;
3. falhas passam pelo ciclo avançado quando aplicável;
4. resultados são devolvidos ao Orchestrator sem perda de contexto;
5. ferramentas continuam sujeitas a Permission/Policy/Checkpoint;
6. nenhum caminho de retry externo contorna governança;
7. o caminho legado permanece compatível até sua migração segura;
8. CI permanece verde em Python 3.11–3.14.
