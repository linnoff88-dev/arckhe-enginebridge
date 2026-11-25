# EngineBridge

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![EngineBridge](guia/assets/banner.jpg)](https://linnoff88-dev.github.io/

**[PortuguêÂªs](README.md) êÂ· [English](README.en.md) êÂ· [EspaêÂ±ol](README.es.md)**

## O que êÂ©

Sua automaêÂ§êÂ£o pode parar quando uma assinatura atinge a cota, mesmo tendo outra disponêÂ­vel. O EngineBridge êÂ© uma ferramenta local para escolher qual motor de IA atende cada etapa e usar uma alternativa declarada quando isso for permitido. Serve para quem mantêÂ©m bots, scripts e rotinas com Claude Code e Codex. VocêÂª define perfis, modelos e esforêÂ§o; o programa resolve a escolha sem consultar uma IA. Para executar textos, precisa de Python e dos programas autenticados pela assinatura.

**VersêÂ£o 1.0.0 ê¢â¬â nêÂºcleo local funcional; integraêÂ§êÂ£o com os sistemas reais ainda pendente.**

[Guia completo](https://linnoff88-dev.github.io/ êÂ· [Arquitetura](docs/ARQUITETURA.md) êÂ· [Plano de adoêÂ§êÂ£o](docs/ADOCAO.md) êÂ· [ReferêÂªncias e revisêÂ£o Astra](docs/REFERENCIAS.md)

## Instalar e verificar

```bash
git clone https://github.com/linnoff88-dev/enginebridge.git
cd enginebridge
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
python3 -m enginebridge resolve --project demonstracao --stage roteiro
```

Requer Python 3.11+ e PyYAML 6. Os perfis de demonstraêÂ§êÂ£o usam modelos explêÂ­citos e podem ser resolvidos sem login. Os nêÂ­veis herdados usam `~/.config/ARCKHê/modelos.env`; em outra mêÂ¡quina, configure `modelos_env` e os caminhos dos executêÂ¡veis no YAML. A resoluêÂ§êÂ£o nêÂ£o verifica a existêÂªncia do modelo na assinatura.

## Simular a troca sem consumir modelos

```bash
printf 'Crie um roteiro curto.' | python3 -m enginebridge --state .state/demo.sqlite run --project demonstracao --stage roteiro --simulate --fail-first
python3 -m enginebridge --state .state/demo.sqlite status
```

A simulaêÂ§êÂ£o produz uma rejeiêÂ§êÂ£o de cota no Codex, registra uma suspensêÂ£o temporêÂ¡ria no SQLite e entrega o mesmo pedido ao executor fictêÂ­cio Claude. O campo `simulado` diferencia essa saêÂ­da de uma execuêÂ§êÂ£o real. NêÂ£o altera serviêÂ§os, nêÂ£o consulta saldo e nêÂ£o chama modelos.

## Preparar contas em uma mêÂ¡quina nova

Instale Claude Code e Codex, autentique pela assinatura no terminal e ajuste `binario` no YAML. Nunca use uma chave de API. O campo opcional `conta_env` aponta para um arquivo de dados com `CODEX_HOME=/caminho/da/conta`; sem esse arquivo, vale a conta padrêÂ£o do Codex.

```bash
codex login
claude auth login
mkdir -p ~/.config/ARCKHê
test -f ~/.config/ARCKHê/modelos.env || cp config/modelos.example.env ~/.config/ARCKHê/modelos.env
```

O exemplo de modelos sêÂ³ êÂ© copiado se nêÂ£o existir configuraêÂ§êÂ£o central. A etapa `demonstracao/padrao` herda o motor global e permite observar a troca com `prefer`; roteiro e crêÂ­tica continuam com perfis fixados.

## PreferêÂªncia global e exceêÂ§êÂµes

```bash
python3 -m enginebridge prefer claude
python3 -m enginebridge resolve --project demonstracao --stage padrao
python3 -m enginebridge prefer codex
python3 -m enginebridge resolve --project demonstracao --stage padrao
```

`prefer` modifica apenas este YAML e preserva comentêÂ¡rios. Etapas com `perfil` ou `motor` explêÂ­cito permanecem fixadas; a troca global afeta as etapas sem essa escolha. Modelo e esforêÂ§o herdados continuam na fonte central existente. EsforêÂ§o nêÂ£o mede equivalêÂªncia de qualidade entre famêÂ­lias de modelos.

```bash
python3 -m enginebridge --state .state/demo.sqlite block --pool codex-principal
python3 -m enginebridge --state .state/demo.sqlite unblock --pool codex-principal
```

Suspender uma conta impede novas admissêÂµes no EngineBridge, inclusive em trabalhos jêÂ¡ resolvidos. Retirar o bloqueio manual preserva eventual suspensêÂ£o temporêÂ¡ria por cota. O estado padrêÂ£o fica em `~/.local/state/enginebridge/state.sqlite`; todos os consumidores da mesma mêÂ¡quina devem compartilhar esse caminho e a configuraêÂ§êÂ£o. NêÂ£o coloque esse SQLite em rede.

## Executar um texto pela assinatura

```bash
printf 'Responda com uma frase sobre perfis por etapa.' | python3 -m enginebridge run --project demonstracao --stage roteiro
```

Este comando consome a assinatura escolhida. Usa Claude Code ou Codex em diretêÂ³rio temporêÂ¡rio, sem MCP pessoal, sem shell habilitado e sem sessêÂ£o nativa compartilhada. As credenciais de API sêÂ£o removidas do ambiente. NêÂ£o executa workflows de agente, publicaêÂ§êÂ£o, imagens ou traduêÂ§êÂ£o. Os binêÂ¡rios precisam aceitar os argumentos documentados pelo adaptador; os testes locais usam executêÂ¡veis fictêÂ­cios, sem comprovar login ou funcionamento real de ambos os CLIs.

## Contrato de continuidade

- SeleêÂ§êÂ£o por chamada, etapa, projeto e preferêÂªncia global, sempre sujeita êÂ s permissêÂµes e êÂ s etapas fixadas.
- Alternativa explêÂ­cita em etapas fixadas; em etapas livres, alternativas do projeto ou globais.
- Cota compartilhada por conta (`quota_pool`), independente do nome do modelo; uma execuêÂ§êÂ£o simultêÂ¢nea por pool neste nêÂºcleo.
- RejeiêÂ§êÂ£o estruturada de cota, sem resposta parcial nem ferramentas, permite tentar a alternativa e persistir a suspensêÂ£o temporêÂ¡ria.
- Erro local, timeout, mensagem de erro apenas em prosa ou resultado recusado pelo validador interrompem o trabalho, sem repetiêÂ§êÂ£o automêÂ¡tica.
- Cada trabalho guarda uma cêÂ³pia resolvida dos modelos; bloqueios urgentes e mudanêÂ§a da conta sêÂ£o conferidos antes de cada tentativa.

HêÂ¡ exemplos de consumo Python e CLI em `examples/`. NêÂ£o hêÂ¡ integraêÂ§êÂ£o ativada com OpenPCBotV3, Refazvideo ou crons. OpenRouter aparece desabilitado como extensêÂ£o futura; nêÂ£o existe adaptador de API nesta versêÂ£o, mesmo que alguêÂ©m altere `habilitado` no YAML.

## Desenvolvimento

```bash
python3 -m compileall -q enginebridge examples tests
python3 -m unittest discover -s tests -v
python3 -m enginebridge --version
```

[LicenêÂ§a MIT](LICENSE). O desenho reaproveita as referêÂªncias de provedores independentes do WiFi e a crêÂ­tica do Astra, preservadas em `docs/`.

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>