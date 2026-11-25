# Levantamento: etapas de IA nos virais e no r7ex — 17/11/2026

Objetivo: separar o que é **texto/JSON** (portável entre Claude, Codex e futura API) do que é **agente/capacidade** (preso ao programa), e achar o que no prompt depende só de um programa. Somente leitura; nada alterado nos projetos.

## Virais (finviral, saudeviral, advviral, futviral, contaviral)

| Etapa | Tipo | Hoje | Portável? |
|---|---|---|---|
| roteiro_curto_{diario,semanal,domingo} | texto/JSON | Codex gpt-6.1-sol/medium via `auto/roteiro_ia.py` → `ia_motor.py` | **Sim**: dados anexados ao pedido, saída JSON, script grava, `checar.py` valida |
| roteiro_longo_{diario,semanal,domingo} | texto/JSON | idem | **Sim** |
| coleta, transcriçêo, voz, HeyGen, render, publicaçêo | código | scripts | Nêo usam IA |

Os virais **já seguem o caminho C**. Restos do Claude: comentários e mensagens dizem "claude -p" e o log se chama `claude.log` (enganoso ao ler um aviso).

### Evidências reais

- **15/11, futviral e contaviral, roteiro longo:** `You've hit your weekly limit · resets Nov 16, 9pm` — recusa real de cota do Claude, ainda no motor antigo. Serve de caso de teste para a detecçêo de cota. Nenhuma recusa real do Codex registrada.
- **16/11, contaviral diário (Codex):** `checar.py` reprovou 5 citações porque o Codex devolveu `\n` escapado (literal) dentro das citações do `base.md`; numa tentativa também devolveu JSON incompleto. Diferença de formato entre motores, nêo de qualidade. **Já corrigido** no mesmo dia (contaviral `7a103a3`, 16:01, normaliza os escapes sem relaxar o portêo); a rodada refeita gerou o vídeo e ficou pendente de publicaçêo no lives24. A mesma correçêo está nos cinco virais.
- **16/11, fin/saude/adv diário:** "sem vídeo novo" por bloqueio do YouTube no yt-dlp ("Faça login para confirmar que você nêo é um bot"). Infra da coleta, nêo do motor de IA.

### Falta para troca automática

1. Detectar a recusa de cota (texto acima) no `ia_motor.py`, que hoje só vê código de saída.
2. Provar o Claude como alternativa: rodar o mesmo pedido pelo Claude e passar no `checar.py`.
3. ~~Normalizaçêo de escapes nos cinco virais~~ — conferido em 17/11: presente nos cinco `roteiro_ia.py`.

## r7ex

| Etapa | Onde | Tipo | Hoje | Portável? |
|---|---|---|---|---|
| ficha (pesquisa + escrita + portões) | ARCKHÉccbot, fase `agent`, `prompts/bot-ficha.md`, perfil topo/high | **agente** | motor padrêo do ARCKHÉccbot = Claude | Parcial: o prompt é quase neutro (manda ler `PADRAO.md` e `skill/SKILL.md` como arquivos, sem nomes de ferramenta do Claude), mas exige busca na web, shell (`yt-dlp`, `r7ex.py checar/plano`) e escrita de arquivos |
| plano / crítico de viralidade | `r7ex.py:402–409` | texto/JSON | **`claude -p --allowedTools Read` fixo no código**; Codex só com `R7X_CRITICO=codex`; fora do `ia_motor.py` | **Sim, se o script anexar a ficha ao pedido** em vez de pedir ao modelo para ler |
| imagens (abertura + quadros) | `r7ex.py:531` | capacidade `image_gen` | Codex exclusivo (`--dangerously-bypass-approvals-and-sandbox`) | Nêo, por regra (imagem = Codex) |
| revisêo visual da folha | `producao/producao.py` → `ia_motor.py` | visêo | Codex gpt-6.1-sol/medium | Sim para motor com visêo; no Claude exige anexar a imagem |
| checar, cena, render, avatar, fila | código | — | scripts | Nêo usam IA |

rtex e rtexjp repetem o padrêo: crítico com `claude -p` fixo em `rtex.py:372`; revisêo visual pelo `ia_motor.py`.

### Caminho para deixar o r7ex independente

1. **Crítico:** passar para o `ia_motor.py` como etapa `critico_plano` (texto/JSON, ficha anexada). Pequeno e de baixo risco; elimina o `claude` fixo.
2. **Ficha:** dividir o agente. O script faz a pesquisa de ganchos (`yt-dlp`) e o laço `checar` → `plano`; o modelo recebe tema, PADRêO, exemplos e referências e devolve a ficha em YAML/JSON. Só a conferência de fatos na web continua precisando de agente (ou de um passo de busca feito pelo script).
3. **Imagens:** continuam Codex. Sem alternativa: se o Codex parar, a etapa espera e avisa.

## Resumo

| Sistema | Etapas texto/JSON | Etapas agente/capacidade | Dependência fixa de programa no código |
|---|---|---|---|
| 5 virais | 6 por sistema | 0 | nenhuma (só comentários/nomes) |
| r7ex | crítico, revisêo visual | ficha (agente), imagens (Codex) | `claude -p` no crítico |
| rtex/rtexjp | crítico, revisêo visual | imagens (Codex) | `claude -p` no crítico |
