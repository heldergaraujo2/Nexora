# 12 — TESTES

> Suite de testes unitários e evidência de CI do projeto.

## Como executar
- `python3 -m pytest tests/ -q`

## Estado verificado
- HEAD de código atualmente validado: `68c93b0dc6710fc375fcff237f38737467f245a5`.
- Última evidência CI verde: workflow `34647078404`.
- Matriz validada: Python 3.11, 3.12, 3.13 e 3.14 — todos os jobs em **success**.
- A versão da release v1.0.0 tinha 128 testes; o estado atual é superior e não deve usar 128 como contagem corrente.

## Cobertura dos componentes pós-release
- Context Engine: `tests/unit/test_contexto.py` — 4 testes.
- Knowledge Engine: `tests/unit/test_conhecimento.py` — 5 testes.
- World Model: `tests/unit/test_mundo.py` — 5 testes.
- Goal Engine: `tests/unit/test_objetivos.py` — 3 testes.
- Strategy Engine: `tests/unit/test_estrategias.py` — 3 testes.
- Communication Bus: `tests/unit/test_comunicacao.py` — 5 testes.
- Delegation: `tests/unit/test_delegacao.py` — cobertura do fluxo básico.
- Capability Delegation: `tests/unit/test_delegacao_capacidade.py` — cobertura de seleção por capacidade.
- Agent Registry: `tests/unit/test_registro_agentes.py` — 4 testes.
- Runtime ↔ Bus: `tests/unit/test_runtime_comunicacao.py` — 2 testes.
- Orchestrator ↔ Bus: `tests/unit/test_orquestrador_comunicacao.py` — 1 teste.
- Delegated Runtime: `tests/unit/test_delegacao_runtime.py` — integração do executor com `AgenteRuntime`.
- Delegated Recovery: `tests/unit/test_delegacao_recovery.py` — retry transitório, falha permanente e validação de tentativas.
- Experience: `tests/unit/test_delegacao_experiencia.py` — registro do resultado terminal.
- Audit: `tests/unit/test_auditoria.py` — persistência/filtros e auditoria de sucesso/falha de delegação.
- Policy: `tests/unit/test_policy.py` — ALLOW, DENY por padrão, integração ALLOW e DENY com auditoria.

## Correções relevantes
- Os testes de runtime e orquestração foram alinhados ao contrato do CommunicationBus: sem assinantes, mensagens permanecem `PENDENTE`; `ENTREGUE` ocorre quando há entrega observada.
- A primeira execução CI da etapa de Policy falhou por ausência de `src/nexora/experiencia/__init__.py`; o pacote foi corrigido e a execução seguinte ficou totalmente verde.

## Histórico
- Fase 16 / v1.0.0: 128 testes passando.
- O número atual é superior a 128; a evidência principal de qualidade é a matriz CI verde em Python 3.11–3.14.
