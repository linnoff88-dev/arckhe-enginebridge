# Adoção incremental

## Já entregue

Resolvedor Python e CLI; preferência global local; perfis e níveis; modelos herdados; explicação JSON; suspensão por conta; cooldown persistente; admissão concorrente; execução textual por CLIs; simulação e testes sem rede; dois exemplos de consumidores textuais.

## Próxima rodada com Nei

1. Testar login e texto curto em cada assinatura, isoladamente, com arquivos de configuração/estado de laboratório. Os testes desta entrega não consumiram modelos pelos adaptadores reais.
2. Adaptar um ponto textual do Refazvideo/Explicavideos e um consumidor independente de cron. Preservar o validador do projeto. Não migrar publicação, imagem, tradução ou ferramentas na primeira rodada.
3. Comparar saída e tempo por tarefa: correção, formato, criticidade, consumo informado pelo provedor e disponibilidade. Só então ajustar as associações dos níveis. Criar conjunto de avaliação com respostas/validadores independentes.
4. OpenPCBotV3: usar resolve para escolher candidatos, guardar snapshot no job e integrar a admissão com os runners existentes. Preservar sessões por motor; não encaminhar agentes com efeitos externos ao executor textual.
5. Na indisponibilidade com publicação ou alteração externa possivelmente iniciada: reconciliar recibo/status no workflow antes de repetir. EngineBridge não decide idempotência de efeitos.
6. Expandir por consumidor integrado, com inventário e rollback. VPS requer distribuição versionada de configuração e identidade de conta; coordenação entre máquinas ainda não existe.

## Critérios para ativar um consumidor

Comando de resolução previsível, entrada/saída validada pelo projeto, modelo/esforço explícitos no resultado, suspensão respeitada, falha incerta sem repetição, registro do motor usado, retorno ao executor antigo documentado. Não basta haver um arquivo YAML: cada chamada aninhada precisa usar o contrato.

## Fora desta versão

APIs de modelos, OpenRouter, daemon remoto, sincronização VPS, agente universal, equivalência automática de modelos, replay de ferramentas, leitura de saldo e alteração automática dos sistemas existentes.

## Proposta futura para discutir

[Chaveamento preventivo por cota](CHAVEAMENTO-PREVENTIVO.md): alerta e política configurável para trabalhos longos a partir de 90% de consumo; encaminhamento dos novos trabalhos compatíveis a partir de 98%. Somente anotado, sem implementação ou ativação.
