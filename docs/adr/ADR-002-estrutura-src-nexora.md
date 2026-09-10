# ADR-002 — Estrutura e namespace: src/nexora/

- Status: Aprovada (Fase 0.5)
- Data: 2026-09-10
- Decisao de origem: P2 (PROJECT_MEMORY/09_DECISIONS.md)
- Relacionamentos: ADR-001 (Python),ADR-009 (politica declarativa)

## Contexto

O repositorio precisa separar codigo de producao de configuracao,testes,documentacao e ferramentas de apoio,alem de permitir instalacao empacotada( via pyproject.toml ) sem poluir o namespace raiz. O layout `src/` e padrao moderno em projetos Python( evita import acidental de codigo nao empacotado e facilita testes com pytest)。

## Decisao

Adotar o layout **`src/nexora/`** como namespace de codigo de producao, com:

- `src/nexora/` para o pacote principal;
- `tests/` para testes( pytest );
- `docs/` para ADRs,contratos e design;
- `PROJECT_MEMORY/` para a memoria persistente do projeto( ja existente );
- `pyproject.toml` na raiz para metadados e dependencias;
 
## Consequencias

- Positivas: separacao limpa codigo/config; instalacao/testes confiaveis( import via pacote instalado,; escalabilidade futura para multiplos modulos;
- Negativas: convencao exige que o ambiente de dev use instalacao editavel( `pip install -e .` ou `uv sync` )para importar o codigo;
- Neutras: namespaces internos dos modulos( core,config,providers,tools,runtime...) serao definidos no design doc( docs/design/repositorio.md ),nao neste ADR。