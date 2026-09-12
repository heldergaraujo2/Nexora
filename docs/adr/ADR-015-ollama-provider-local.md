# ADR-015 — Provider local Ollama

**Data:** 2026-09-12  
**Status:** Aprovada para implementação incremental

## Contexto

A NEXORA precisa utilizar inteligência local para reduzir custo, operar offline quando possível e preparar uma futura distribuição simples. O núcleo, entretanto, deve permanecer model-agnóstico e não pode depender de Ollama como runtime obrigatório.

O hardware de desenvolvimento considerado atualmente é Ryzen 5 5600 + aproximadamente 16 GB de RAM + Radeon RX 6600 8 GB. Isso orienta um perfil local inicial, mas não deve virar requisito fixo da arquitetura.

## Decisão

1. Criar `ProviderOllama` implementando o contrato `Provider` existente.
2. Usar HTTP via stdlib, sem adicionar dependências pip ao projeto.
3. Usar `http://localhost:11434` como endpoint padrão, com `NEXORA_OLLAMA_URL` para configuração.
4. Usar `NEXORA_OLLAMA_MODEL` para selecionar o modelo e manter um perfil padrão compatível com a estratégia local inicial.
5. O perfil padrão de desenvolvimento será `qwen2.5-coder:7b-instruct-q4_K_M`, mas o código não pode depender desse modelo específico.
6. O health check consultará o daemon local sem consumir uma geração.
7. Indisponibilidade HTTP/rede será convertida para `ProviderIndisponivel`.
8. O Provider local será registrado nas mesmas camadas `RegistryProviders` e `ProviderManager`; não haverá um caminho paralelo de execução.
9. Streaming e tool-calling não serão declarados como capacidades até haver implementação e testes específicos.
10. A futura detecção de hardware e escolha automática de perfil pertence à Fase 22, não a este primeiro incremento.

## Consequências

### Positivas

- inteligência local pode ser usada sem API paga;
- arquitetura permanece compatível com Groq e futuros Providers;
- instalação local pode ser automatizada posteriormente;
- testes não dependem de Ollama estar instalado na máquina do CI;
- o projeto continua sem dependências externas obrigatórias.

### Limites

- este incremento não instala Ollama;
- este incremento não baixa modelos;
- este incremento não garante aceleração específica da GPU;
- este incremento não implementa streaming;
- este incremento não habilita tool-calling local;
- health check confirma o daemon, não comprova desempenho do modelo.

## Testes

A implementação exige:

- testes unitários de configuração, payload, resposta e erros;
- teste de health check;
- teste de integração mockada atravessando Registry + ProviderManager;
- CI em Python 3.11–3.14.

## Próxima evolução

Depois da validação deste Provider, a Fase 17 deve avançar para descoberta/configuração de modelos locais e preparação do contrato de seleção de perfil, sempre mantendo o Provider agnóstico.
