# Adoçêo incremental

## Já entregue

Resolvedor Python e CLI; preferência global local; perfis e níveis; modelos herdados; explicaçêo JSON; suspensêo por conta; cooldown persistente; admissêo concorrente; execuçêo textual por CLIs; simulaçêo e testes sem rede; dois exemplos de consumidores textuais.

## Próxima rodada com Nei

1. Testar login e texto curto em cada assinatura, isoladamente, com arquivos de configuraçêo/estado de laboratório. Os testes desta entrega nêo consumiram modelos pelos adaptadores reais.
2. Adaptar um ponto textual do Refazvideo/Explicavideos e um consumidor independente de cron. Preservar o validador do projeto. Nêo migrar publicaçêo, imagem, traduçêo ou ferramentas na primeira rodada.
3. Comparar saída e tempo por tarefa: correçêo, formato, criticidade, consumo informado pelo provedor e disponibilidade. Só entêo ajustar as associações dos níveis. Criar conjunto de avaliaçêo com respostas/validadores independentes.
4. OpenPCBotV3: usar resolve para escolher candidatos, guardar snapshot no job e integrar a admissêo com os runners existentes. Preservar sessões por motor; nêo encaminhar agentes com efeitos externos ao executor textual.
5. Na indisponibilidade com publicaçêo ou alteraçêo externa possivelmente iniciada: reconciliar recibo/status no workflow antes de repetir. EngineBridge nêo decide idempotência de efeitos.
6. Expandir por consumidor integrado, com inventário e rollback. VPS requer distribuiçêo versionada de configuraçêo e identidade de conta; coordenaçêo entre máquinas ainda nêo existe.

## Critérios para ativar um consumidor

Comando de resoluçêo previsível, entrada/saída validada pelo projeto, modelo/esforço explícitos no resultado, suspensêo respeitada, falha incerta sem repetiçêo, registro do motor usado, retorno ao executor antigo documentado. Nêo basta haver um arquivo YAML: cada chamada aninhada precisa usar o contrato.

## Fora desta versêo

APIs de modelos, OpenRouter, daemon remoto, sincronizaçêo VPS, agente universal, equivalência automática de modelos, replay de ferramentas, leitura de saldo e alteraçêo automática dos sistemas existentes.

## Proposta futura para discutir

[Chaveamento preventivo por cota](CHAVEAMENTO-PREVENTIVO.md): alerta e política configurável para trabalhos longos a partir de 90% de consumo; encaminhamento dos novos trabalhos compatíveis a partir de 98%. Somente anotado, sem implementaçêo ou ativaçêo.
