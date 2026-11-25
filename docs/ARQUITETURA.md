# Arquitetura — v1.0.0

EngineBridge é uma camada local de política e adaptadores, sem daemon obrigatório. Nêo substitui a fila nem o executor de agentes do OpenPCBotV3.

## Resoluçêo

Permissêo e tipo de transporte sêo filtros obrigatórios. Entre candidatos permitidos: chamada > etapa > projeto > global. Perfil explícito da etapa fixa o motor e pode sobrescrever modelo/esforço. Pedido incompatível com etapa fixada é recusado. Nível: chamada > etapa > projeto > global. Alternativa da etapa > projeto > global; etapas fixadas só usam alternativa declarada na própria etapa. Perfil desconhecido, projeto desconhecido, esforço inválido e modelo ausente falham explicitamente.

A fonte central `modelos.env` fornece ARCKHÉ_<MOTOR>_<NIVEL> e _EFFORT. YAML pode declarar exceçêo por nível ou perfil. Nêo traduzir low em medium automaticamente; validar cada combinaçêo por tarefa. Haiku/Luna, Sonnet/Terra, Sol/Opus, Fable/Astra sêo hipóteses de avaliaçêo, nêo equivalências medidas nem padrões instalados.

`resolve` produz JSON serializável com hash da configuraçêo e modelos resolvidos. A biblioteca permite guardar essa cópia no trabalho. Ela é dado interno confiável: nêo aceitar snapshots fornecidos por usuários nêo confiáveis. Modelo e esforço ficam congelados; antes de executar, reconsulta habilitaçêo, tipo, pool e identidade CODEX_HOME. Preferência global nêo interrompe uma chamada em andamento. Mudanças concorrentes de YAML sêo responsabilidade do operador; `prefer` faz substituiçêo atômica, mas nêo oferece ediçêo concorrente distribuída.

## Admissêo por cota

SQLite local transacional, `BEGIN IMMEDIATE`, uma concessêo por quota_pool, prazo timeout + 30 segundos. Processos que compartilham estado respeitam suspensêo manual, cooldown e concessões. Outro programa que chama Claude/Codex diretamente continua fora desse controle. Configurar dois modelos da mesma conta com pools distintos burla a coordenaçêo; o operador deve mapear a identidade correta. Nêo consulta franquia real e nêo monitora CLIs externos.

Quota/rate limit só aceita rejeiçêo estruturada conhecida e nenhuma resposta parcial/ferramenta. O parser é conservador: mensagens em prosa nêo acionam fallback. O cooldown usa duraçêo configurada, nêo presume horário de reset informado pelo serviço. Após expirar, uma nova concessêo testa recuperaçêo. Nêo espera em fila nem faz retry interno: devolve erro para o workflow reagendar.

## Adaptadores

Claude: CLI por assinatura, --tools vazio, --safe-mode, --restricted, MCP vazio e sem persistência. Nêo usa --bare porque esse modo exige API e exclui OAuth. Codex: login chatgpt forçado, config/regras pessoais ignoradas, sandbox read-only, recursos de shell, execuçêo, apps, navegador, geraçêo e multiagentes desabilitados. Diretório de trabalho temporário; prompt pela entrada padrêo. Nunca usar shell=True.

O isolamento protege o modo textual; nêo é uma fronteira contra binário malicioso, políticas administradas ou mudanças futuras do CLI. Suporte a argumentos é dependente da versêo instalada. Saída com ferramentas inesperadas é recusada. Execuçêo tem prazo e encerramento do grupo em timeout. Saídas temporárias sêo removidas e o resultado lido tem teto de 8 MB; arquivos temporários nêo têm quota de disco específica. Nenhum custo é inferido como zero.

Nêo há migraçêo de sessêo entre motores: o consumidor envia o contexto textual necessário. Traduçêo permanece ARCKHÉ-traduz; imagens e MCPs exigem adaptadores próprios, fora deste núcleo. OpenRouter/API nêo é implementado nem autorizado por configuraçêo. A inclusêo futura exigirá autorizaçêo de serviço/finalidade, limites de gasto e testes.
