**Recomendo uma camada leve de política e adaptaçêo, aproveitando os executores existentes.** A hipótese revisada melhora substancialmente a original: permite mudar preferências globalmente sem apagar especializações. Ainda faltam contratos precisos para identidade de conta, cotas compartilhadas, admissêo concorrente e continuidade. Sem eles, o EngineBridge pode centralizar configuraçêo e continuar distribuindo decisões incompatíveis.

A evidência local comprova componentes úteis e integrações testadas; nêo comprova uma política global. Os 384 testes e o smoke do openpcbotv3 sustentam aquele sistema, nêo os demais consumidores.

**Oito lacunas prioritárias e a menor correçêo:**

1. **Crítica — precedência confundida com permissêo.** “Pedido > etapa > perfil > padrêo” permite interpretar um override como autorizaçêo. Correçêo: primeiro calcular as rotas permitidas; depois aplicar preferências dentro desse conjunto. Pedido comum nunca libera API.

2. **Crítica — conta nêo representa necessariamente a cota.** Modelos, aliases e perfis podem consumir o mesmo limite; uma conta também pode ter limites distintos. Correçêo: identificar conta e conjuntos de cota compartilhada explicitamente, com origem da informaçêo. Identidade desconhecida deve aparecer como limitaçêo, nêo como independência presumida.

3. **Crítica — fallback pode repetir efeitos.** Um timeout nêo prova que publicaçêo, HeyGen ou ferramenta falhou antes de agir. Correçêo: resultado `efeito_incerto` impede repetiçêo automática e exige reconciliaçêo pelo workflow. Trocar o motor nêo resolve essa ambiguidade.

4. **Alta — snapshot pode perpetuar uma rota revogada.** Correçêo: congelar seleçêo e contexto do job, mas consultar bloqueios obrigatórios imediatamente antes da admissêo de cada chamada. Registrar a versêo do snapshot e a revisêo da política aplicada; alternativa só quando previamente permitida.

5. **Alta — cobertura global presumida.** Trocar o motor do bot nêo alcança seus subprocessos. Correçêo: inventário por ponto de chamada, distinguindo integrado, legado e verificado. “Global” significa todos os consumidores integrados; os 43 alvos nêo equivalem a 43 timers nem a cobertura completa.

6. **Alta — capacidade e qualidade confundidas.** “Texto”, “visêo” ou “MCP” nêo demonstram equivalência entre modelos. Correçêo: requisitos por etapa, rotas qualificadas e esforço próprio por rota. Verificar ferramentas no transporte e versêo efetivamente usados. Nêo transportar `effort` cegamente entre motores.

7. **Alta — concorrência e retentativas sem proprietário.** Vários processos podem descobrir a mesma cota esgotada simultaneamente; o CLI pode ter retries internos. Correçêo: estado compartilhado persistente, admissêo coordenada, prazo e orçamento de tentativas. Documentar o que o adaptador controla e o que permanece interno ao CLI.

8. **Média — núcleo universal antes de provar a fronteira.** `refazvideo` é playbook; `explicavideos` produz. Correçêo: começar por uma chamada textual isolada, como a crítica, tornando modelo/esforço explícitos. Validar em um segundo consumidor antes de generalizar o executor.

**O modelo recomendado separa restrições, seleçêo e execuçêo.**

`MODELOS.md` e `modelos.env` continuam como referências existentes para níveis e modelos. EngineBridge acrescenta vínculos entre roles e esses níveis, restrições e identidade operacional; nêo mantém outra tabela concorrente de modelos. Traduçêo permanece delegada ao `ARCKHÉ-traduz`.

A resoluçêo proposta é:

- **Política obrigatória:** autorizações por serviço/finalidade, transportes permitidos, restrições do projeto, capacidades exigidas, bloqueios e limites.
- **Seleçêo:** pedido explícito > etapa > projeto > preferência global > padrêo existente, sempre respeitando fixações.
- **Role:** planejador, crítico, executor ou classificaçêo escolhe candidatos próprios. Visêo, imagem e MCP também expressam requisitos de capacidade; nêo precisam virar modelos intercambiáveis.
- **Execuçêo:** adaptador invoca o CLI oficial com argumentos explícitos e perfil de conta permitido. Nêo extrai OAuth nem injeta chaves.

Uma fixaçêo só pode ser removida por alteraçêo explícita autorizada. Se ficar proibida, o job bloqueia ou segue uma alternativa já declarada; nunca é “desfixado” silenciosamente. Política desconhecida ou inválida nêo abre caminhos.

Por exemplo, o comando conceitual `preferir-Claude` muda a ordem dos candidatos de crítico, planejador e executor nêo fixados, preservando modelos adequados a cada role. Imagem continua no caminho específico Codex `image_gen`; traduçêo continua no `ARCKHÉ-traduz`; uma etapa fixada em Codex permanece fixada. Se a conta Codex for suspensa, essas etapas bloqueiam quando nêo houver alternativa expressamente permitida.

Para jobs existentes, a preferência global passa a valer no próximo job; migraçêo de job ativo exige operaçêo explícita. Bloqueios urgentes valem na próxima admissêo, inclusive para chamadas enfileiradas, sem cancelar ações já admitidas. Essa fronteira precisa ser documentada.

Cada decisêo produz explicaçêo: candidatos, exclusões, origem da escolha, conta, grupos de cota e versões. O hash identifica a configuraçêo, mas nêo substitui essa explicaçêo.

**O reaproveitamento deve ser seletivo.**

Nos trechos fornecidos, **Hermes** demonstra cadeias auxiliares, tratamento de fixações, cooldown informado pelo reset e esforço resolvido para o destino. Sêo bons padrões. Entretanto, preservar histórico dentro do Hermes nêo prova retomada entre Claude Code e Codex. Seus caminhos OAuth descritos nêo atendem à regra local de uso exclusivo pelos CLIs oficiais. A própria documentaçêo fornecida deixa incerto o consumo da assinatura Codex e descreve cobrança extra no caminho Anthropic.

**OpenClaw** oferece boas distinções entre falha local, saturaçêo, erro de modelo e falha do provedor, além de contabilizar candidatos descartados e preservar trabalho parcial. Nêo copiaria rotaçêo de credenciais para contornar limites. Seu gate documentado é local ao processo e nêo coordena outros gateways nem transportes nativos: insuficiente para a coordenaçêo global proposta. Instruir o agente a conferir ações interrompidas também nêo garante reconciliaçêo.

**LiteLLM** oferece separaçêo clara entre [retry, fallback e cooldown](https://docs.litellm.ai/docs/router/learn/reliability). A documentaçêo de [subscriptions](https://docs.litellm.ai/docs/subscriptions) impede classificá-lo como “somente APIs”. Contudo, transporte, consumo e isolamento desses caminhos permanecem **nêo verificados nesta análise**. Nêo há base para recomendar adoçêo direta sob as restrições locais.

Localmente, reaproveitaria `ia_motor.py`, YAML por etapa, validaçêo e bloqueio de APIs; do openpcbotv3, snapshots e sessões por motor. Preservaria as evidências de testes por consumidor, sem promover adaptações distintas a equivalência comprovada.

**O menor MVP útil** entrega resoluçêo explicável, preferência global manual, suspensêo compartilhada, snapshot e dois consumidores textuais integrados. Um modo de simulaçêo mostra escolhas sem inferência. Adiaria failover automático de agentes, APIs com ferramentas e repetiçêo de publicaçêo.

Aceite mínimo:

- Overrides nêo atravessam bloqueios; pins, imagem e traduçêo preservam suas regras.
- Processos concorrentes observam atualizaçêo atômica; aliases e modelos da mesma cota compartilham bloqueio, sem bloquear contas independentes.
- Reinício preserva cooldown; vencimento permite tentativa controlada, sem disparada coletiva.
- Mudança de contexto preserva instruções e resultados ou declara incompatibilidade; nêo promete transferir sessões nativas.
- Timeout após possível efeito externo bloqueia replay até reconciliaçêo.
- Erro local nêo troca provedor; retries têm teto; CLI interno e cobertura legada ficam visíveis.

Detecçêo por regras dispensa inferência; tentativas, resumos e contexto reenviado podem consumir cota. Nêo sondar saldo gerando chamadas.

**A decisêo recomendada é a camada leve**, versionada e testável. Os sistemas citados fornecem padrões úteis; os trechos nêo demonstram substituto compatível com todas as restrições. Um executor universal só se justificaria depois que pilotos comprovassem repetiçêo suficiente para extraí-lo.