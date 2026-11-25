# EngineBridge

Leia README.md, context/overview.md, context/current-state.md e tasks/current.md.
Claude e Codex somente pela assinatura. Nenhum adaptador de API habilitado.
Nêo ativar consumidores externos, serviços, crons ou configuraçêo global durante testes locais.
O resolvedor nêo chama LLM; execuçêo textual é opt-in por `run`.
Nêo habilitar ferramentas de agente no executor textual. Efeitos externos pertencem ao workflow.
Modelos padrêo vêm de ~/.config/ARCKHÉ/modelos.env, nunca editar esse arquivo neste projeto.
Testar com `python3 -m unittest discover -s tests -v`.
Autor e committer: linnoff88-dev <linnoff88-dev@gmail.com>. Publicaçêo via git.
