# 12 — TESTES

> Suite de testes unitários e evidência de CI do projeto.

## Como executar
- `python3 -m pytest tests/ -q`

## Estado verificado
- Último HEAD implementado: `8745681cb21a71690a2360f0b7851ca2d3e50027`.
- Não há workflow associado retornado para esse HEAD; portanto ele ainda não está marcado como validado por CI.
- Última matriz CI comprovadamente verde: workflow `34653209175`, Python 3.11, 3.12, 3.13 e 3.14, no HEAD histórico `dec0bbd4430bbe5883476112704ea78c97b90be3`.

## Cobertura dos componentes pós-release
- Context Engine: `tests/unit/test_contexto.py`.
- Knowledge Engine: `tests/unit/test_conhecimento.py`.
- World Model: `tests/unit/test_mundo.py`.
- Goal Engine: `tests/unit/test_objetivos.py`.
- Strategy Engine: `tests/unit/test_estrategias.py`.
- Communication Bus: `tests/unit/test_comunicacao.py`.
- Delegation: `tests/unit/test_delegacao.py`.
- Capability Delegation: `tests/unit/test_delegacao_capacidade.py`.
- Agent Registry: `tests/unit/test_registro_agentes.py`.
- Runtime ↔ Bus: `tests/unit/test_runtime_comunicacao.py`.
- Orchestrator ↔ Bus: `tests/unit/test_orquestrador_comunicacao.py`.
- Delegated Runtime: `tests/unit/test_delegacao_runtime.py`.
- Delegated Recovery: `tests/unit/test_delegacao_recovery.py`.
- Experience: `tests/unit/test_delegacao_experiencia.py`.
- Audit: `tests/unit/test_auditoria.py`.
- Policy: `tests/unit/test_policy.py`.
- Policy Loader: `tests/unit/test_policy_loader.py`.
- Permission boundary: `tests/unit/test_permissoes.py`.
- Policy lifecycle: `tests/unit/test_policy_manager.py`.
- Tool governance: `tests/unit/test_ferramentas_governanca.py`.
- Sandbox governance: `tests/unit/test_sandbox_governanca.py` — compatibilidade sem política, ALLOW, DENY sem subprocesso, precedência da allowlist e auditoria.

## Correções relevantes
- Runtime/orquestração seguem o contrato do CommunicationBus.
- O pacote `nexora.experiencia` foi corrigido após falha histórica de CI.
- Loader declarativo rejeita campos desconhecidos e tipos ambíguos.
- Schema de política versão 2 exige IDs únicos nas regras.
- Fingerprint de política usa SHA-256 canônico sobre a semântica, incluindo ordem e excluindo origem.
- `EstadoDelegacao.DENEGADA` separa negação de governança de falha de execução.
- `GerenciadorPermissoes` cria uma fronteira explícita de autorização sem executar ações.
- `GerenciadorPolitica` troca políticas atomicamente somente após validação bem-sucedida.
- Registry de ferramentas e Sandbox podem exigir permissão antes da execução, preservando compatibilidade quando o componente de governança não é configurado.
- Sandbox não coloca o comando completo no contexto de auditoria de permissão, reduzindo risco de exposição de argumentos sensíveis.

## Histórico
- Fase 16 / v1.0.0: 128 testes passando.
- O número atual é superior a 128; a contagem corrente deve ser obtida executando a suite, não inferida deste documento.
