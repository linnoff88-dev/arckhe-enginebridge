# Validação — 16/11/2026

- Instalação editável em .venv Python 3.12, PyYAML 6.0.3: passou.
- 20 testes sem rede: passaram (21 em 17/11, com a recusa real de cota do Claude). Cobrem resolução central/perfil, escolha global e etapa fixada, proibição de API, snapshot e bloqueio urgente, mudança de conta, suspensão persistente, cota compartilhada, erro incerto, validação, concorrência de quatro processos, recuperação e proprietário da concessão, consumidores Python/CLI, executável fictício e timeout real de processo.
- compileall: passou; CLI instalada informa 1.0.0.
- Simulação CLI Codex rejeitado por cota → Claude fictício respondeu: passou.
- Exemplos Python e shell resolveram a política sem inferência.
- Revisão independente final do guia: aprovado, nota 9/10, sem defeitos.
- Guias PT/EN/ES: 1440, 390 e 360 px, sem overflow, imagens ou âncoras quebradas e sem erros JS; tema claro/escuro passou.
- Detector estático visual apontou heurísticas do template (fontes, sombra, tamanhos) e hífens dos comandos; preservada a identidade INEMA e conferida a renderização real.
- Portal: 13 testes, build Next com Webpack e TypeScript passaram. Turbopack não aceitou dependências ligadas por symlink no worktree; limitação registrada no WiFi.
- Content-base: 41 testes passaram; base resultante 19.728 itens, incluindo EngineBridge, sem remover IDs anteriores.

Os adaptadores Claude/Codex foram testados com executáveis fictícios, não com chamadas reais às assinaturas. Não foi comprovado saldo, login, disponibilidade de modelo nem transferência real entre assinaturas. Nenhum sistema existente foi integrado ou reiniciado. Próxima rodada: docs/ADOCAO.md.

Capturas, saídas e logs locais: ~/projetos/output/enginebridge-2026-11-16/ (fora do repositório para não publicar dados operacionais).
