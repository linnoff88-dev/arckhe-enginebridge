# EngineBridge

Leia README.md, context/overview.md, context/current-state.md e tasks/current.md.
Claude e Codex somente pela assinatura. Nenhum adaptador de API habilitado.
Não ativar consumidores externos, serviços, crons ou configuração global durante testes locais.
O resolvedor não chama LLM; execução textual é opt-in por `run`.
Não habilitar ferramentas de agente no executor textual. Efeitos externos pertencem ao workflow.
Modelos padrão vêm de ~/.config/inema/modelos.env, nunca editar esse arquivo neste projeto.
Testar com `python3 -m unittest discover -s tests -v`.
Autor e committer: inematds <inematds@gmail.com>. Publicação via git.
