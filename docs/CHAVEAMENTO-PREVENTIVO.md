# Proposta: chaveamento preventivo por consumo de cota

Registrado a pedido do Nei em 16/11/2026. **Ideia para discutir; nêo implementada nem ativada.** Os percentuais abaixo representam cota consumida, nêo cota restante. Nenhuma mudança em serviços, configuraçêo global ou assinaturas foi autorizada por esta anotaçêo.

## Faixas propostas pelo Nei

| Consumo da cota | Comportamento a discutir |
|---|---|
| Abaixo de 90% | Manter a política normal de perfis e etapas. |
| A partir de 90% e abaixo de 98% | Analisar a situaçêo e emitir alerta de atençêo. Aplicar a política do usuário para execuções longas: permitir, impedir novos trabalhos longos, deixar só trabalhos curtos ou encaminhar os longos para o próximo provedor autorizado. |
| A partir de 98% | Chavear todos os novos trabalhos compatíveis para o próximo provedor autorizado. Se nêo houver alternativa apta, deixar pendente e alertar. |

O usuário deve poder definir o que pode ou nêo executar de forma longa após 90%, por sistema, etapa ou perfil. Antecipar o envio de trabalhos longos ao próximo provedor é uma opçêo configurável; nêo precisa esperar esgotar a conta. A intençêo é preservar uma reserva para tarefas curtas e evitar que um trabalho longo pare no meio.

## Pontos a decidir antes de desenvolver

- Como obter o percentual com fonte confiável: assinatura, conta, janela de uso e horário de renovaçêo. Algumas contas têm limites compartilhados entre modelos e várias janelas; definir qual janela governa a política. Se nêo houver leitura disponível, registrar estado desconhecido ou uma estimativa identificada, sem inventar um percentual exato.
- O que caracteriza trabalho curto ou longo: estimativa de tokens, quantidade de etapas, tempo e histórico. Duraçêo sozinha pode nêo prever consumo. O usuário poderá definir exceções e prioridades.
- Quais políticas ficam disponíveis em 90%: permitir longos, pausar longos, manter apenas curtos ou encaminhar longos. Definir precedência entre regra global e exceções por sistema/etapa/perfil.
- Como selecionar e conferir o destino: login, cota própria, capacidade, modelo/esforço, ferramentas exigidas e autorizaçêo. Mesmo provedor/modelo diferente pode compartilhar a mesma cota; nêo tratar isso como uma reserva independente.
- O alcance de “todos em 98%”: a intençêo é encaminhar todos os novos trabalhos, mas etapas fixadas, capacidades exclusivas e permissões precisam de regra explícita. Nêo substituir uma ferramenta incompatível nem habilitar API por causa do limiar.
- O que fazer com execuções em andamento e trabalhos já na fila: por padrêo da proposta, nêo matar nem repetir uma açêo iniciada. Discutir pontos seguros de parada/retomada e rever admissêo antes da próxima etapa. Efeitos externos precisam de reconciliaçêo para evitar duplicaçêo.
- Canal e frequência do alerta: destino definido pelo usuário, mensagem com conta/janela, consumo, renovaçêo e açêo tomada; evitar alertas repetidos em cada chamada.
- Como voltar ao provedor original após renovaçêo: conferir recuperaçêo, evitar alternância constante perto dos limites e definir retorno automático ou manual.
- Como considerar o consumo ainda em andamento, concorrência e dados antigos, para evitar admitir vários trabalhos longos imediatamente antes do limiar.

## Princípios a preservar

A comparaçêo com os limiares, a admissêo e a troca devem funcionar em código local, sem precisar de tokens da conta esgotada para decidir. A execuçêo no destino consome a cota do destino. Uma análise adicional por IA pode ser opcional, sem se tornar dependência do mecanismo de troca.

Manter Claude/Codex pela assinatura. Esta proposta nêo autoriza consultas por APIs nêo autorizadas nem a ativaçêo do OpenRouter. Aplicar somente aos consumidores integrados ao EngineBridge; chamadas diretas fora dele nêo mudam automaticamente.

## Próxima conversa

Escolher a fonte de mediçêo, definir curto/longo e as opções de política, desenhar exemplos de 90% e 98% e só depois aprovar implementaçêo e testes. Relacionado: [plano de adoçêo](ADOCAO.md) e [arquitetura atual](ARQUITETURA.md).
