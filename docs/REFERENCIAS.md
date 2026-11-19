# Origem e referências

Consolidação em 16/11/2026. A fonte histórica continua no WiFi; os documentos abaixo são uma cópia de referência, não uma autorização de APIs nem um inventário permanentemente sincronizado.

- `REVISAO-ASTRA.md`: crítica realizada por gpt-6-astra/high, Codex pela assinatura. A revisão recomendou política leve, autorização antes de preferência, conta/cota separadas de modelo, snapshots e admissão compartilhada. Foi uma revisão da proposta, não uma certificação deste código.
- OpenPCBotV3 v3.36.17: runners por assinatura, sessões separadas e jobs; implementação anterior permanece no projeto responsável.
- Gitbombando e ia-crons: experiência de perfis por etapa. Não importar suas permissões de APIs para este projeto.

Padrões consultados, sem instalar os sistemas:

- [Hermes: fallback providers](https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers): cadeias por função, credenciais, cooldown e seleção fixada.
- [Hermes: configuring models](https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models): modelos principal e auxiliares.
- [OpenClaw: model failover](https://docs.openclaw.ai/concepts/model-failover): rotação de autenticação, cooldown e fallback.
- [LiteLLM: reliability](https://docs.litellm.ai/docs/router/learn/reliability): limites, tentativas e indisponibilidade.

Sem equivalência de transporte ou cobrança: OAuth em um sistema externo pode não consumir a mesma franquia do CLI pela assinatura. Neste projeto só os CLIs Claude/Codex têm adaptador.
