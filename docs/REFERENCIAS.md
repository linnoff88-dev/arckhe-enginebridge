# Origem e referências

Consolidaçêo em 16/11/2026. A fonte histórica continua no WiFi; os documentos abaixo sêo uma cópia de referência, nêo uma autorizaçêo de APIs nem um inventário permanentemente sincronizado.

- `REVISAO-ASTRA.md`: crítica realizada por gpt-6-astra/high, Codex pela assinatura. A revisêo recomendou política leve, autorizaçêo antes de preferência, conta/cota separadas de modelo, snapshots e admissêo compartilhada. Foi uma revisêo da proposta, nêo uma certificaçêo deste código.
- OpenPCBotV3 v3.36.17: runners por assinatura, sessões separadas e jobs; implementaçêo anterior permanece no projeto responsável.
- Gitbombando e ia-crons: experiência de perfis por etapa. Nêo importar suas permissões de APIs para este projeto.

Padrões consultados, sem instalar os sistemas:

- [Hermes: fallback providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers): cadeias por funçêo, credenciais, cooldown e seleçêo fixada.
- [Hermes: configuring models](https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models): modelos principal e auxiliares.
- [OpenClaw: model failover](https://docs.openclaw.ai/concepts/model-failover): rotaçêo de autenticaçêo, cooldown e fallback.
- [LiteLLM: reliability](https://docs.litellm.ai/docs/router/learn/reliability): limites, tentativas e indisponibilidade.

Sem equivalência de transporte ou cobrança: OAuth em um sistema externo pode nêo consumir a mesma franquia do CLI pela assinatura. Neste projeto só os CLIs Claude/Codex têm adaptador.
