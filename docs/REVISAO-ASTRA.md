**Recomendo uma camada leve de política e adaptação, aproveitando os executores existentes.** A hipótese revisada melhora substancialmente a original: permite mudar preferências globalmente sem apagar especializações. Ainda faltam contratos precisos para identidade de conta, cotas compartilhadas, admissão concorrente e continuidade. Sem eles, o EngineBridge pode centralizar configuração e continuar distribuindo decisões incompatíveis.

A evidência local comprova componentes úteis e integrações testadas; não comprova uma política global. Os 384 testes e o smoke do openpcbotv3 sustentam aquele sistema, não os demais consumidores.

**Oito lacunas prioritárias e a menor correção:**

1. **Crítica — precedência confundida com permissão.** “Pedido > etapa > perfil > padrão” permite interpretar um override como autorização. Correção: primeiro calcular as rotas permitidas; depois aplicar preferências dentro desse conjunto. Pedido comum nunca libera API.

2. **Crítica — conta não representa necessariamente a cota.** Modelos, aliases e perfis podem consumir o mesmo limite; uma conta também pode ter limites distintos. Correção: identificar conta e conjuntos de cota compartilhada explicitamente, com origem da informação. Identidade desconhecida deve aparecer como limitação, não como independência presumida.

3. **Crítica — fallback pode repetir efeitos.** Um timeout não prova que publicação, HeyGen ou ferramenta falhou antes de agir. Correção: resultado `efeito_incerto` impede repetição automática e exige reconciliação pelo workflow. Trocar o motor não resolve essa ambiguidade.

4. **Alta — snapshot pode perpetuar uma rota revogada.** Correção: congelar seleção e contexto do job, mas consultar bloqueios obrigatórios imediatamente antes da admissão de cada chamada. Registrar a versão do snapshot e a revisão da política aplicada; alternativa só quando previamente permitida.

5. **Alta — cobertura global presumida.** Trocar o motor do bot não alcança seus subprocessos. Correção: inventário por ponto de chamada, distinguindo integrado, legado e verificado. “Global” significa todos os consumidores integrados; os 43 alvos não equivalem a 43 timers nem a cobertura completa.

6. **Alta — capacidade e qualidade confundidas.** “Texto”, “visão” ou “MCP” não demonstram equivalência entre modelos. Correção: requisitos por etapa, rotas qualificadas e esforço próprio por rota. Verificar ferramentas no transporte e versão efetivamente usados. Não transportar `effort` cegamente entre motores.

7. **Alta — concorrência e retentativas sem proprietário.** Vários processos podem descobrir a mesma cota esgotada simultaneamente; o CLI pode ter retries internos. Correção: estado compartilhado persistente, admissão coordenada, prazo e orçamento de tentativas. Documentar o que o adaptador controla e o que permanece interno ao CLI.

8. **Média — núcleo universal antes de provar a fronteira.** `refazvideo` é playbook; `explicavideos` produz. Correção: começar por uma chamada textual isolada, como a crítica, tornando modelo/esforço explícitos. Validar em um segundo consumidor antes de generalizar o executor.

**O modelo recomendado separa restrições, seleção e execução.**

`MODELOS.md` e `modelos.env` continuam como referências existentes para níveis e modelos. EngineBridge acrescenta vínculos entre roles e esses níveis, restrições e identidade operacional; não mantém outra tabela concorrente de modelos. Tradução permanece delegada ao `ARCKHÉ-traduz`.

A resolução proposta é:

- **Política obrigatória:** autorizações por serviço/finalidade, transportes permitidos, restrições do projeto, capacidades exigidas, bloqueios e limites.
- **Seleção:** pedido explícito > etapa > projeto > preferência global > padrão existente, sempre respeitando fixações.
- **Role:** planejador, crítico, executor ou classificação escolhe candidatos próprios. Visão, imagem e MCP também expressam requisitos de capacidade; não precisam virar modelos intercambiáveis.
- **Execução:** adaptador invoca o CLI oficial com argumentos explícitos e perfil de conta permitido. Não extrai OAuth nem injeta chaves.

Uma fixação só pode ser removida por alteração explícita autorizada. Se ficar proibida, o job bloqueia ou segue uma alternativa já declarada; nunca é “desfixado” silenciosamente. Política desconhecida ou inválida não abre caminhos.

Por exemplo, o comando conceitual `preferir-Claude` muda a ordem dos candidatos de crítico, planejador e executor não fixados, preservando modelos adequados a cada role. Imagem continua no caminho específico Codex `image_gen`; tradução continua no `ARCKHÉ-traduz`; uma etapa fixada em Codex permanece fixada. Se a conta Codex for suspensa, essas etapas bloqueiam quando não houver alternativa expressamente permitida.

Para jobs existentes, a preferência global passa a valer no próximo job; migração de job ativo exige operação explícita. Bloqueios urgentes valem na próxima admissão, inclusive para chamadas enfileiradas, sem cancelar ações já admitidas. Essa fronteira precisa ser documentada.

Cada decisão produz explicação: candidatos, exclusões, origem da escolha, conta, grupos de cota e versões. O hash identifica a configuração, mas não substitui essa explicação.

**O reaproveitamento deve ser seletivo.**

Nos trechos fornecidos, **Hermes** demonstra cadeias auxiliares, tratamento de fixações, cooldown informado pelo reset e esforço resolvido para o destino. São bons padrões. Entretanto, preservar histórico dentro do Hermes não prova retomada entre Claude Code e Codex. Seus caminhos OAuth descritos não atendem à regra local de uso exclusivo pelos CLIs oficiais. A própria documentação fornecida deixa incerto o consumo da assinatura Codex e descreve cobrança extra no caminho Anthropic.

**OpenClaw** oferece boas distinções entre falha local, saturação, erro de modelo e falha do provedor, além de contabilizar candidatos descartados e preservar trabalho parcial. Não copiaria rotação de credenciais para contornar limites. Seu gate documentado é local ao processo e não coordena outros gateways nem transportes nativos: insuficiente para a coordenação global proposta. Instruir o agente a conferir ações interrompidas também não garante reconciliação.

**LiteLLM** oferece separação clara entre [retry, fallback e cooldown](https://docs.litellm.ai/docs/router/learn/reliability). A documentação de [subscriptions](https://docs.litellm.ai/docs/subscriptions) impede classificá-lo como “somente APIs”. Contudo, transporte, consumo e isolamento desses caminhos permanecem **não verificados nesta análise**. Não há base para recomendar adoção direta sob as restrições locais.

Localmente, reaproveitaria `ia_motor.py`, YAML por etapa, validação e bloqueio de APIs; do openpcbotv3, snapshots e sessões por motor. Preservaria as evidências de testes por consumidor, sem promover adaptações distintas a equivalência comprovada.

**O menor MVP útil** entrega resolução explicável, preferência global manual, suspensão compartilhada, snapshot e dois consumidores textuais integrados. Um modo de simulação mostra escolhas sem inferência. Adiaria failover automático de agentes, APIs com ferramentas e repetição de publicação.

Aceite mínimo:

- Overrides não atravessam bloqueios; pins, imagem e tradução preservam suas regras.
- Processos concorrentes observam atualização atômica; aliases e modelos da mesma cota compartilham bloqueio, sem bloquear contas independentes.
- Reinício preserva cooldown; vencimento permite tentativa controlada, sem disparada coletiva.
- Mudança de contexto preserva instruções e resultados ou declara incompatibilidade; não promete transferir sessões nativas.
- Timeout após possível efeito externo bloqueia replay até reconciliação.
- Erro local não troca provedor; retries têm teto; CLI interno e cobertura legada ficam visíveis.

Detecção por regras dispensa inferência; tentativas, resumos e contexto reenviado podem consumir cota. Não sondar saldo gerando chamadas.

**A decisão recomendada é a camada leve**, versionada e testável. Os sistemas citados fornecem padrões úteis; os trechos não demonstram substituto compatível com todas as restrições. Um executor universal só se justificaria depois que pilotos comprovassem repetição suficiente para extraí-lo.