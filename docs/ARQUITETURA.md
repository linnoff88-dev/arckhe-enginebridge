# Arquitetura — v1.0.0

EngineBridge é uma camada local de política e adaptadores, sem daemon obrigatório. Não substitui a fila nem o executor de agentes do OpenPCBotV3.

## Resolução

Permissão e tipo de transporte são filtros obrigatórios. Entre candidatos permitidos: chamada > etapa > projeto > global. Perfil explícito da etapa fixa o motor e pode sobrescrever modelo/esforço. Pedido incompatível com etapa fixada é recusado. Nível: chamada > etapa > projeto > global. Alternativa da etapa > projeto > global; etapas fixadas só usam alternativa declarada na própria etapa. Perfil desconhecido, projeto desconhecido, esforço inválido e modelo ausente falham explicitamente.

A fonte central `modelos.env` fornece INEMA_<MOTOR>_<NIVEL> e _EFFORT. YAML pode declarar exceção por nível ou perfil. Não traduzir low em medium automaticamente; validar cada combinação por tarefa. Haiku/Luna, Sonnet/Terra, Sol/Opus, Fable/Astra são hipóteses de avaliação, não equivalências medidas nem padrões instalados.

`resolve` produz JSON serializável com hash da configuração e modelos resolvidos. A biblioteca permite guardar essa cópia no trabalho. Ela é dado interno confiável: não aceitar snapshots fornecidos por usuários não confiáveis. Modelo e esforço ficam congelados; antes de executar, reconsulta habilitação, tipo, pool e identidade CODEX_HOME. Preferência global não interrompe uma chamada em andamento. Mudanças concorrentes de YAML são responsabilidade do operador; `prefer` faz substituição atômica, mas não oferece edição concorrente distribuída.

## Admissão por cota

SQLite local transacional, `BEGIN IMMEDIATE`, uma concessão por quota_pool, prazo timeout + 30 segundos. Processos que compartilham estado respeitam suspensão manual, cooldown e concessões. Outro programa que chama Claude/Codex diretamente continua fora desse controle. Configurar dois modelos da mesma conta com pools distintos burla a coordenação; o operador deve mapear a identidade correta. Não consulta franquia real e não monitora CLIs externos.

Quota/rate limit só aceita rejeição estruturada conhecida e nenhuma resposta parcial/ferramenta. O parser é conservador: mensagens em prosa não acionam fallback. O cooldown usa duração configurada, não presume horário de reset informado pelo serviço. Após expirar, uma nova concessão testa recuperação. Não espera em fila nem faz retry interno: devolve erro para o workflow reagendar.

## Adaptadores

Claude: CLI por assinatura, --tools vazio, --safe-mode, --restricted, MCP vazio e sem persistência. Não usa --bare porque esse modo exige API e exclui OAuth. Codex: login chatgpt forçado, config/regras pessoais ignoradas, sandbox read-only, recursos de shell, execução, apps, navegador, geração e multiagentes desabilitados. Diretório de trabalho temporário; prompt pela entrada padrão. Nunca usar shell=True.

O isolamento protege o modo textual; não é uma fronteira contra binário malicioso, políticas administradas ou mudanças futuras do CLI. Suporte a argumentos é dependente da versão instalada. Saída com ferramentas inesperadas é recusada. Execução tem prazo e encerramento do grupo em timeout. Saídas temporárias são removidas e o resultado lido tem teto de 8 MB; arquivos temporários não têm quota de disco específica. Nenhum custo é inferido como zero.

Não há migração de sessão entre motores: o consumidor envia o contexto textual necessário. Tradução permanece inema-traduz; imagens e MCPs exigem adaptadores próprios, fora deste núcleo. OpenRouter/API não é implementado nem autorizado por configuração. A inclusão futura exigirá autorização de serviço/finalidade, limites de gasto e testes.
