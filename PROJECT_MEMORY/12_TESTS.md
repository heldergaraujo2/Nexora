# 12 — TESTS

## Política de Testes

- Testar antes de concluir qualquer tarefa.
- Registrar o último teste e seu resultado no PROJECT_MEMORY.



## Estado dos Testes

| Teste | Escopo | Resultado |
|--------|--------|-----------|
| Verificação de integridade dos arquivos PROJECT_MEMORY | Ausência de caracteres corrompidos(zero-width spaces,,lixo binário,chineses) | Aprovado( 00–15 + README + NEXT_COMMAND)
| Verificação de consistência de numeração | Referências cruzadas entre arquivos e nomes canônicos | Aprovado( nenhuma referência antiga restante)



## Último Teste

- **Data:**620 2026-09-10
- **Escopo:** Verificação byte-a-byte dos arquivos 00–15 do PROJECT_MEMORY + README + NEXT_COMMAND
- **Resultado:** Zero-width spaces encontrados e corrigidos;reverificação pendente após correção.



## Regra

Não avançar para a próxima fase sem testes passando.