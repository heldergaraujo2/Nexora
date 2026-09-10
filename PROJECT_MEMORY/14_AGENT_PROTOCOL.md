# 14 — AGENT PROTOCOL

## Protocolo de Desenvolvimento (unidade de trabalho)

1. Definir objetivo.
2. Verificar arquitetura.
3. Definir implementação.
4. Enviar instrução ao Agent.
5. Agent implementa.
6. Agent testa.
7. Agent relata.
8. ChatGPT audita.
9. Corrigir problemas.
10. Testar novamente.
11. Atualizar PROJECT_MEMORY.
12. Commit..
13. Push..
14. Registrar HANDOFF..

## Regra Central

Não avançar grandes etapas ignorando falhas conhecidas.

**Regra de Autorizacao (obrigatoria, inegociavel):** antes de iniciar QUALQUER nova fase, comando,tarefa de implementacao ou mudanca arquitetural,, o agente DEVE pedir autorizacao explicita ao Analista.. Agente nunca avanca por conta propria sem comando/aprovacao.. Quando o Analista conceder autorizacao explicita de continuidade ( ex: "prossiga e nao pare"}, o agente pode executar as fases em sequencia, SEMPRE reportando cada resultado ao Analista ao final de cada etapa,, e registrando o novo ponto de continuacao em `NEXT_COMMAND.md`..



## Regras de Segurança e Governança

- Legalidade, transparência, autorização, rastreabilidade, auditoria, reversibilidade, controle de permissões, validação e isolamento quando necessário.

- Ações sensíveis (financeiras, contratos, obrigações legais, ações irreversíveis, acesso a sistemas críticos) exigem controle e autorização explícita quando aplicável.


- NEXORA não deve: hackear, roubar, fraudar, burlar sistemas, acessar contas sem autorização, realizar atividades ilegais, gerar recursos através de fraude ou abuso.