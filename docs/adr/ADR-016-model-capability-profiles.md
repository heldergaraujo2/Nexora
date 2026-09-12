# ADR-016 — Perfis de capacidade de modelos locais

**Data:** 2026-09-12  
**Status:** Aprovada

## Contexto
A NEXORA precisa escolher modelos sem transformar o modelo atual do computador do criador em requisito arquitetural. A seleção deve partir de capacidades observáveis e critérios determinísticos, deixando benchmark e roteamento econômico para fases posteriores.

## Decisão
- Criar um perfil independente do Provider para representar categoria, parâmetros e contexto.
- Derivar apenas metadados observáveis; não declarar qualidade ou velocidade sem benchmark.
- Criar pontuação determinística inicial para preparar a seleção futura.
- Permitir limite máximo de parâmetros e requisito mínimo de contexto.
- Não escolher automaticamente Provider/modelo ainda: isso pertence à Fase 21 — Intelligent Model Routing.

## Consequências
A NEXORA já consegue raciocinar sobre capacidades sem hard-code de um único modelo. A pontuação é heurística e não deve ser apresentada como benchmark.

## Testes
Testes unitários cobrem parsing, perfil de coding/general e limite de parâmetros.
