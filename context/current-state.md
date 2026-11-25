# Estado — 2026-11-17

v1.0.0 implementada: resolvedor, adaptadores textuais CLI, estado SQLite e 21 testes locais. Guia/README PT/EN/ES, referências e plano de adoçêo publicados.

**Primeiro uso real (17/11):** o r7ex (v1.7.6) lê e grava a tabela `pools` deste estado (`~/.local/state/enginebridge/state.sqlite`, só `blocked`/`until`, nunca lease) pela trava de cota do `ia_motor.py`; crítico do plano com reserva Claude→Codex. O núcleo `run`/resolvedor do EngineBridge ainda nêo é usado por nenhum sistema.

Parser de cota do Claude corrigido para o formato real (16/11). Codex sem recusa real registrada. Levantamento dos virais/r7ex em docs/LEVANTAMENTO-VIRAIS-R7EX.md. Propostas para discutir: CHAVEAMENTO-PREVENTIVO.md e APIS-E-PROVEDORES-FUTURO.md.
