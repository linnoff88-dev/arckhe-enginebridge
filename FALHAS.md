| data | o que quebrou | menor correçêo | prompt ou infra |
|---|---|---|---|
| 2026-11-17 | parser de cota do Claude esperava error.type; a recusa real usa api_error no topo e traz texto em result, entêo nunca seria reconhecida | aceitar o formato real (is_error + terminal_reason api_error + api_error) com teste da recusa de 16/11 | prompt |
| 2026-11-16 | guia resolvia nível herdado antes de preparar configuraçêo central em máquina nova | mover preparaçêo da conta/modelos antes do exemplo global | prompt |
| 2026-11-16 | busca de ID ignorou objetos JSON e escolheria identificador existente no portal | considerar id com e sem aspas antes de inserir | prompt |
| 2026-11-16 | regeneraçêo do PRO com fontes de conteúdo antigas no worktree retiraria 30 itens | usar snapshot completo das fontes atuais e comparar IDs antes de publicar | infra |
| 2026-11-16 | helper de catálogo nêo reconheceu declaraçêo TypeScript com tipo | aceitar anotaçêo antes do sinal de igual na busca | prompt |
