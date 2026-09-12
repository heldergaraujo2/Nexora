# 12 — TESTES

> Suite de testes unitários e evidência de CI da NEXORA.

## Como executar
- `python3 -m pytest tests/ -q`

## Estado atual
- HEAD implementado desta etapa: `51e052d4e276bff41c27b772a6ccaa5918c000d1`.
- O status GitHub do HEAD está `pending` sem statuses concluídos; portanto **não declarar CI verde** para este checkpoint.
- O ambiente desta sessão não conseguiu clonar o repositório externamente para executar a suite localmente; a validação executável permanece pendente do CI/ambiente local.
- Última matriz CI comprovadamente verde permanece a matriz histórica já registrada no changelog.

## Cobertura dos componentes
- Context Engine: `tests/unit/test_contexto.py`.
- Knowledge Engine: `tests/unit/test_conhecimento.py`.
- World Model: `tests/unit/test_mundo.py`.
- Goal Engine: `tests/unit/test_objetivos.py`.
- Strategy Engine: `tests/unit/test_estrategias.py`.
- Communication Bus: `tests/unit/test_comunicacao.py`.
- Delegation / capability / runtime / recovery / experience.
- Agent Registry e Orchestrator.
- Audit: `tests/unit/test_auditoria.py`.
- Policy / loader / permission boundary / lifecycle.
- Tool governance: `tests/unit/test_tools_governanca.py` e `tests/unit/test_tools_registry.py`.
- Sandbox governance: `tests/unit/test_sandbox_governanca.py`.
- Checkpoint Engine: `tests/unit/test_checkpoint.py` — isolamento do snapshot, recuperação sem mutação, filtro por execução, auditoria e validações.
- Idempotência: `tests/unit/test_idempotencia.py` e cenários integrados em `tests/unit/test_tools_registry.py`.
- Orchestrator + idempotência + ferramenta: `tests/integration/test_orquestrador_ferramentas.py`.
- Plano/Tarefa com chave explícita: `tests/unit/test_plano.py`.

## Regras de validação
- Testes de governança devem provar que DENY ocorre antes da execução real.
- Checkpoint não executa ferramentas nem desfaz efeitos externos; ele captura e recupera estado lógico isolado.
- Idempotência deve provar que a mesma chave/fingerprint não executa a ferramenta novamente.
- Fingerprint diferente para a mesma chave deve ser conflito.
- `IN_PROGRESS` e `FAILED` não podem provocar retry automático.
- A contagem corrente de testes deve ser obtida executando a suite, não inferida deste documento.
- CI só pode ser marcado como verde quando houver execução correspondente ao HEAD atual.