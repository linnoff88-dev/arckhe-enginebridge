# Proposta: chaveamento preventivo por consumo de cota

Registrado a pedido do Nei em 16/11/2026. **Ideia para discutir; não implementada nem ativada.** Os percentuais abaixo representam cota consumida, não cota restante. Nenhuma mudança em serviços, configuração global ou assinaturas foi autorizada por esta anotação.

## Faixas propostas pelo Nei

| Consumo da cota | Comportamento a discutir |
|---|---|
| Abaixo de 90% | Manter a política normal de perfis e etapas. |
| A partir de 90% e abaixo de 98% | Analisar a situação e emitir alerta de atenção. Aplicar a política do usuário para execuções longas: permitir, impedir novos trabalhos longos, deixar só trabalhos curtos ou encaminhar os longos para o próximo provedor autorizado. |
| A partir de 98% | Chavear todos os novos trabalhos compatíveis para o próximo provedor autorizado. Se não houver alternativa apta, deixar pendente e alertar. |

O usuário deve poder definir o que pode ou não executar de forma longa após 90%, por sistema, etapa ou perfil. Antecipar o envio de trabalhos longos ao próximo provedor é uma opção configurável; não precisa esperar esgotar a conta. A intenção é preservar uma reserva para tarefas curtas e evitar que um trabalho longo pare no meio.

## Pontos a decidir antes de desenvolver

- Como obter o percentual com fonte confiável: assinatura, conta, janela de uso e horário de renovação. Algumas contas têm limites compartilhados entre modelos e várias janelas; definir qual janela governa a política. Se não houver leitura disponível, registrar estado desconhecido ou uma estimativa identificada, sem inventar um percentual exato.
- O que caracteriza trabalho curto ou longo: estimativa de tokens, quantidade de etapas, tempo e histórico. Duração sozinha pode não prever consumo. O usuário poderá definir exceções e prioridades.
- Quais políticas ficam disponíveis em 90%: permitir longos, pausar longos, manter apenas curtos ou encaminhar longos. Definir precedência entre regra global e exceções por sistema/etapa/perfil.
- Como selecionar e conferir o destino: login, cota própria, capacidade, modelo/esforço, ferramentas exigidas e autorização. Mesmo provedor/modelo diferente pode compartilhar a mesma cota; não tratar isso como uma reserva independente.
- O alcance de “todos em 98%”: a intenção é encaminhar todos os novos trabalhos, mas etapas fixadas, capacidades exclusivas e permissões precisam de regra explícita. Não substituir uma ferramenta incompatível nem habilitar API por causa do limiar.
- O que fazer com execuções em andamento e trabalhos já na fila: por padrão da proposta, não matar nem repetir uma ação iniciada. Discutir pontos seguros de parada/retomada e rever admissão antes da próxima etapa. Efeitos externos precisam de reconciliação para evitar duplicação.
- Canal e frequência do alerta: destino definido pelo usuário, mensagem com conta/janela, consumo, renovação e ação tomada; evitar alertas repetidos em cada chamada.
- Como voltar ao provedor original após renovação: conferir recuperação, evitar alternância constante perto dos limites e definir retorno automático ou manual.
- Como considerar o consumo ainda em andamento, concorrência e dados antigos, para evitar admitir vários trabalhos longos imediatamente antes do limiar.

## Princípios a preservar

A comparação com os limiares, a admissão e a troca devem funcionar em código local, sem precisar de tokens da conta esgotada para decidir. A execução no destino consome a cota do destino. Uma análise adicional por IA pode ser opcional, sem se tornar dependência do mecanismo de troca.

Manter Claude/Codex pela assinatura. Esta proposta não autoriza consultas por APIs não autorizadas nem a ativação do OpenRouter. Aplicar somente aos consumidores integrados ao EngineBridge; chamadas diretas fora dele não mudam automaticamente.

## Próxima conversa

Escolher a fonte de medição, definir curto/longo e as opções de política, desenhar exemplos de 90% e 98% e só depois aprovar implementação e testes. Relacionado: [plano de adoção](ADOCAO.md) e [arquitetura atual](ARQUITETURA.md).
