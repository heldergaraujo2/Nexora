# 12 — TESTES

> Suite de testes unitários e evidência de CI da NEXORA.

## Como executar
- `python3 -m pytest tests/ -q`

## Estado atual
- Último HEAD implementado: `5e022a6a2b9d6df031deb17fd4983b8d5860ee90`.
- Não há CI confirmado para os commits desta etapa; portanto **não declarar CI verde** para o HEAD atual.
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
- Tool governance: `tests/unit/test_ferramentas_governanca.py`.
- Sandbox governance: `tests/unit/test_sandbox_governanca.py`.
- Checkpoint Engine: `tests/unit/test_checkpoint.py` — isolamento do snapshot, recuperação sem mutação, filtro por execução, auditoria e validações.

## Regras de validação
- Testes de governança devem provar que DENY ocorre antes da execução real.
- Checkpoint não executa ferramentas nem desfaz efeitos externos; ele captura e recupera estado lógico isolado.
- A contagem corrente de testes deve ser obtida executando a suite, não inferida deste documento.
