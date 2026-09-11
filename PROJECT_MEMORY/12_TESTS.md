# 12 — TESTES

> Suite de testes unitários e evidência de CI do projeto.

## Como executar
- `python3 -m pytest tests/ -q`

## Estado verificado
- No HEAD `fc77446...`: CI executou **163 passed, 2 failed**.
- As duas falhas foram diagnosticadas como expectativas incorretas nos testes de integração do CommunicationBus: eles esperavam `ENTREGUE` sem assinantes.
- Correção mínima aplicada em `tests/unit/test_runtime_comunicacao.py` e `tests/unit/test_orquestrador_comunicacao.py`: os testes agora esperam `PENDENTE`, conforme o contrato atual do Bus.
- O workflow é executado automaticamente no push para `main` em Python 3.11, 3.12, 3.13 e 3.14.
- O resultado do CI disparado pelos commits de reconciliação deve ser registrado no Handoff após a conclusão.

## Testes dos novos componentes
- Context Engine: `tests/unit/test_contexto.py` — 4 testes.
- Knowledge Engine: `tests/unit/test_conhecimento.py` — 5 testes.
- World Model: `tests/unit/test_mundo.py` — 5 testes.
- Goal Engine: `tests/unit/test_objetivos.py` — 3 testes.
- Strategy Engine: `tests/unit/test_estrategias.py` — 3 testes.
- Communication Bus: `tests/unit/test_comunicacao.py` — 5 testes.
- Delegation: `tests/unit/test_delegacao.py` — 2 testes.
- Capability Delegation: `tests/unit/test_delegacao_capacidade.py` — 2 testes.
- Agent Registry: `tests/unit/test_registro_agentes.py` — 4 testes.
- Runtime ↔ Bus: `tests/unit/test_runtime_comunicacao.py` — 2 testes.
- Orchestrator ↔ Bus: `tests/unit/test_orquestrador_comunicacao.py` — 1 teste.

## Histórico
- Fase 16: 128 testes no ponto da release v1.0.0.
- O número atual é superior a 128; não usar o número da release como estado atual.
