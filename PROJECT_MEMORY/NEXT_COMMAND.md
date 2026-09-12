# NEXT COMMAND — EVIDÊNCIA DE PESQUISA RECONCILIADA

> Canal de continuidade da coordenação da NEXORA. A release `v1.0.0` continua válida como marco histórico; o código avançou depois dela.

## Estado atual — 2026-09-12

- O HEAD real deve ser obtido diretamente do `main` no início de cada sessão.
- `AgentRuntime` permanece o único proprietário do ciclo avançado.
- `core/ciclo.py` permanece legado/compatibilidade e não deve ser removido prematuramente.
- Quality Routing foi validado pelo CI em Python 3.11–3.14, incluindo testes adversariais e cenário de desempate por qualidade.
- Research Agent agora possui contrato estruturado `claim → evidence → source`.
- Evidências preservam título, URL, trecho, consulta e confiança explícita quando disponível.
- Citações para fontes inexistentes não criam evidência.
- `source_id` ordinal mantém compatibilidade com `[fonte:N]`.
- `source_ref` é um fingerprint SHA-256 determinístico da proveniência material e não representa prova de veracidade.
- Evidências são propagadas para `ResultadoAgente`, métricas e `ExecutionTrace.metadata`.

## CI fechado

- Run #344 (`34721678128`) — SUCCESS — Python 3.11/3.12/3.13/3.14.
- Run #345 (`34721984271`) — SUCCESS — Python 3.11/3.12/3.13/3.14.
- Run #351 (`34722084768`) — SUCCESS — Python 3.11/3.12/3.13/3.14.
- Run #352 (`34722089714`) — SUCCESS — Python 3.11/3.12/3.13/3.14.

## Próximo trabalho obrigatório

**Verificação de adequação da evidência.**

Objetivo: impedir que uma citação válida seja confundida com sustentação válida.

Contrato pretendido:

```text
Claim
  ↓
Citation
  ↓
Source exists?
  ├── não → sem evidência
  └── sim
       ↓
Evidence adequacy
       ├── sustentada
       ├── insuficiente
       └── indeterminada
```

Restrições:
- começar por sinais determinísticos e auditáveis;
- não inventar confiança probabilística;
- não tratar URL/fingerprint como prova de verdade;
- preservar compatibilidade com o formato atual;
- adicionar testes unitários e integração;
- CI verde antes de marcar o incremento como OK.

## Protocolo

`AUDITAR → DECIDIR → IMPLEMENTAR → TESTAR → ATUALIZAR PROJECT_MEMORY → COMMIT → PUSH → VERIFICAR CI → HANDOFF`

GitHub é a fonte de verdade.
