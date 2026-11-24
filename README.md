# EngineBridge

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![EngineBridge](guia/assets/banner.jpg)](https://linnoff88-dev.github.io/

**[PortuguÃªs](README.md) Â· [English](README.en.md) Â· [EspaÃ±ol](README.es.md)**

## O que Ã©

Sua automaÃ§Ã£o pode parar quando uma assinatura atinge a cota, mesmo tendo outra disponÃ­vel. O EngineBridge Ã© uma ferramenta local para escolher qual motor de IA atende cada etapa e usar uma alternativa declarada quando isso for permitido. Serve para quem mantÃ©m bots, scripts e rotinas com Claude Code e Codex. VocÃª define perfis, modelos e esforÃ§o; o programa resolve a escolha sem consultar uma IA. Para executar textos, precisa de Python e dos programas autenticados pela assinatura.

**VersÃ£o 1.0.0 â€” nÃºcleo local funcional; integraÃ§Ã£o com os sistemas reais ainda pendente.**

[Guia completo](https://linnoff88-dev.github.io/ Â· [Arquitetura](docs/ARQUITETURA.md) Â· [Plano de adoÃ§Ã£o](docs/ADOCAO.md) Â· [ReferÃªncias e revisÃ£o Astra](docs/REFERENCIAS.md)

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

Requer Python 3.11+ e PyYAML 6. Os perfis de demonstraÃ§Ã£o usam modelos explÃ­citos e podem ser resolvidos sem login. Os nÃ­veis herdados usam `~/.config/ARCKHÉ/modelos.env`; em outra mÃ¡quina, configure `modelos_env` e os caminhos dos executÃ¡veis no YAML. A resoluÃ§Ã£o nÃ£o verifica a existÃªncia do modelo na assinatura.

## Simular a troca sem consumir modelos

```bash
printf 'Crie um roteiro curto.' | python3 -m enginebridge --state .state/demo.sqlite run --project demonstracao --stage roteiro --simulate --fail-first
python3 -m enginebridge --state .state/demo.sqlite status
```

A simulaÃ§Ã£o produz uma rejeiÃ§Ã£o de cota no Codex, registra uma suspensÃ£o temporÃ¡ria no SQLite e entrega o mesmo pedido ao executor fictÃ­cio Claude. O campo `simulado` diferencia essa saÃ­da de uma execuÃ§Ã£o real. NÃ£o altera serviÃ§os, nÃ£o consulta saldo e nÃ£o chama modelos.

## Preparar contas em uma mÃ¡quina nova

Instale Claude Code e Codex, autentique pela assinatura no terminal e ajuste `binario` no YAML. Nunca use uma chave de API. O campo opcional `conta_env` aponta para um arquivo de dados com `CODEX_HOME=/caminho/da/conta`; sem esse arquivo, vale a conta padrÃ£o do Codex.

```bash
codex login
claude auth login
mkdir -p ~/.config/ARCKHÉ
test -f ~/.config/ARCKHÉ/modelos.env || cp config/modelos.example.env ~/.config/ARCKHÉ/modelos.env
```

O exemplo de modelos sÃ³ Ã© copiado se nÃ£o existir configuraÃ§Ã£o central. A etapa `demonstracao/padrao` herda o motor global e permite observar a troca com `prefer`; roteiro e crÃ­tica continuam com perfis fixados.

## PreferÃªncia global e exceÃ§Ãµes

```bash
python3 -m enginebridge prefer claude
python3 -m enginebridge resolve --project demonstracao --stage padrao
python3 -m enginebridge prefer codex
python3 -m enginebridge resolve --project demonstracao --stage padrao
```

`prefer` modifica apenas este YAML e preserva comentÃ¡rios. Etapas com `perfil` ou `motor` explÃ­cito permanecem fixadas; a troca global afeta as etapas sem essa escolha. Modelo e esforÃ§o herdados continuam na fonte central existente. EsforÃ§o nÃ£o mede equivalÃªncia de qualidade entre famÃ­lias de modelos.

```bash
python3 -m enginebridge --state .state/demo.sqlite block --pool codex-principal
python3 -m enginebridge --state .state/demo.sqlite unblock --pool codex-principal
```

Suspender uma conta impede novas admissÃµes no EngineBridge, inclusive em trabalhos jÃ¡ resolvidos. Retirar o bloqueio manual preserva eventual suspensÃ£o temporÃ¡ria por cota. O estado padrÃ£o fica em `~/.local/state/enginebridge/state.sqlite`; todos os consumidores da mesma mÃ¡quina devem compartilhar esse caminho e a configuraÃ§Ã£o. NÃ£o coloque esse SQLite em rede.

## Executar um texto pela assinatura

```bash
printf 'Responda com uma frase sobre perfis por etapa.' | python3 -m enginebridge run --project demonstracao --stage roteiro
```

Este comando consome a assinatura escolhida. Usa Claude Code ou Codex em diretÃ³rio temporÃ¡rio, sem MCP pessoal, sem shell habilitado e sem sessÃ£o nativa compartilhada. As credenciais de API sÃ£o removidas do ambiente. NÃ£o executa workflows de agente, publicaÃ§Ã£o, imagens ou traduÃ§Ã£o. Os binÃ¡rios precisam aceitar os argumentos documentados pelo adaptador; os testes locais usam executÃ¡veis fictÃ­cios, sem comprovar login ou funcionamento real de ambos os CLIs.

## Contrato de continuidade

- SeleÃ§Ã£o por chamada, etapa, projeto e preferÃªncia global, sempre sujeita Ã s permissÃµes e Ã s etapas fixadas.
- Alternativa explÃ­cita em etapas fixadas; em etapas livres, alternativas do projeto ou globais.
- Cota compartilhada por conta (`quota_pool`), independente do nome do modelo; uma execuÃ§Ã£o simultÃ¢nea por pool neste nÃºcleo.
- RejeiÃ§Ã£o estruturada de cota, sem resposta parcial nem ferramentas, permite tentar a alternativa e persistir a suspensÃ£o temporÃ¡ria.
- Erro local, timeout, mensagem de erro apenas em prosa ou resultado recusado pelo validador interrompem o trabalho, sem repetiÃ§Ã£o automÃ¡tica.
- Cada trabalho guarda uma cÃ³pia resolvida dos modelos; bloqueios urgentes e mudanÃ§a da conta sÃ£o conferidos antes de cada tentativa.

HÃ¡ exemplos de consumo Python e CLI em `examples/`. NÃ£o hÃ¡ integraÃ§Ã£o ativada com OpenPCBotV3, Refazvideo ou crons. OpenRouter aparece desabilitado como extensÃ£o futura; nÃ£o existe adaptador de API nesta versÃ£o, mesmo que alguÃ©m altere `habilitado` no YAML.

## Desenvolvimento

```bash
python3 -m compileall -q enginebridge examples tests
python3 -m unittest discover -s tests -v
python3 -m enginebridge --version
```

[LicenÃ§a MIT](LICENSE). O desenho reaproveita as referÃªncias de provedores independentes do WiFi e a crÃ­tica do Astra, preservadas em `docs/`.

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>