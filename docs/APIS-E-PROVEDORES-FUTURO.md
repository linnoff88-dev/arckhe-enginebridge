# Proposta: APIs e provedores independentes (OpenRouter e outros)

Registrado a pedido do Nei em 17/11/2026. **Ponto para mais adiante; nêo implementado nem autorizado.** Nada aqui muda `habilitado`, código ou chaves. A regra dura continua: API só com autorizaçêo explícita do Nei por serviço e finalidade.

## O que já existe fora do EngineBridge

- `ia_motor.py` (método do WiFi, `~/projetos/wifi/provedores-independentes/`) já tem adaptadores de API Anthropic (Messages), OpenAI (Responses) e OpenRouter (Chat Completions).
- Gate atual: `api.autorizada` + texto `autorizacao` + `etapas_autorizadas`; autorizaçêo Anthropic nêo libera OpenAI/OpenRouter.
- Em uso real só no gitbombando (API Anthropic, cinco etapas autorizadas). OpenAI e OpenRouter: só simulados.
- `modelos.env` já declara `ARCKHÉ_OPENROUTER_<NIVEL>` (IDs `anthropic/...`).

Portanto o executor de API existe; o que falta é **política**, nêo transporte.

## O que o EngineBridge precisaria acrescentar

1. **Autorizaçêo por serviço + finalidade + etapa**, com origem registrada (data e frase do Nei). Config sozinha nunca autoriza.
2. **Teto de gasto** por dia/mês e por trabalho, com contador local; ao bater, bloquear e alertar.
3. **Nunca fallback automático de assinatura para API.** Cota esgotada na assinatura nêo libera API. Se um dia for desejado, exige regra própria aprovada.
4. **Somente etapas texto/visêo.** API nêo executa MCP, agente, `image_gen` nem ferramentas do CLI.
5. **Pool próprio por chave/conta** (`quota_pool`), separado das assinaturas.
6. **Registro de custo informado pelo provedor**, sem inferir zero.
7. **Modelo na API ≠ modelo na assinatura**: ID e acesso podem diferir; validar por etapa.

## Decidir antes de desenvolver

- Reaproveitar os adaptadores do `ia_motor.py` ou chamar o `ia_motor.py` como executor.
- Quais etapas fazem sentido em API (ex.: classificaçêo barata, tarefas sem ferramentas).
- OpenRouter como agregador: quais modelos, roteamento do provedor, política de dados.
- Outros independentes (ex.: modelos locais via Ollama já aprovados) entram pela mesma política; modelo local novo segue a regra de aprovaçêo.

Relacionado: [chaveamento preventivo](CHAVEAMENTO-PREVENTIVO.md), [adoçêo](ADOCAO.md), [arquitetura](ARQUITETURA.md).
