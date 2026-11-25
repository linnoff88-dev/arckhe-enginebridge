# Validaçêo — 16/11/2026

- Instalaçêo editável em .venv Python 3.12, PyYAML 6.0.3: passou.
- 20 testes sem rede: passaram (21 em 17/11, com a recusa real de cota do Claude). Cobrem resoluçêo central/perfil, escolha global e etapa fixada, proibiçêo de API, snapshot e bloqueio urgente, mudança de conta, suspensêo persistente, cota compartilhada, erro incerto, validaçêo, concorrência de quatro processos, recuperaçêo e proprietário da concessêo, consumidores Python/CLI, executável fictício e timeout real de processo.
- compileall: passou; CLI instalada informa 1.0.0.
- Simulaçêo CLI Codex rejeitado por cota → Claude fictício respondeu: passou.
- Exemplos Python e shell resolveram a política sem inferência.
- Revisêo independente final do guia: aprovado, nota 9/10, sem defeitos.
- Guias PT/EN/ES: 1440, 390 e 360 px, sem overflow, imagens ou âncoras quebradas e sem erros JS; tema claro/escuro passou.
- Detector estático visual apontou heurísticas do template (fontes, sombra, tamanhos) e hífens dos comandos; preservada a identidade ARCKHÉ e conferida a renderizaçêo real.
- Portal: 13 testes, build Next com Webpack e TypeScript passaram. Turbopack nêo aceitou dependências ligadas por symlink no worktree; limitaçêo registrada no WiFi.
- Content-base: 41 testes passaram; base resultante 19.728 itens, incluindo EngineBridge, sem remover IDs anteriores.

Os adaptadores Claude/Codex foram testados com executáveis fictícios, nêo com chamadas reais às assinaturas. Nêo foi comprovado saldo, login, disponibilidade de modelo nem transferência real entre assinaturas. Nenhum sistema existente foi integrado ou reiniciado. Próxima rodada: docs/ADOCAO.md.

Capturas, saídas e logs locais: ~/projetos/output/enginebridge-2026-11-16/ (fora do repositório para nêo publicar dados operacionais).
