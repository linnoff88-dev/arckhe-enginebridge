import hashlib
import json
import os
from pathlib import Path

import yaml

from .state import State


class BridgeError(Exception):
    pass


def env_file(path):
    """Read data; never source a shell or expand substitutions."""
    p = Path(path).expanduser()
    if not p.exists():
        return {}
    result = {}
    for line in p.read_text().splitlines():
        if line.strip() and not line.lstrip().startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            result[key.strip()] = value.strip().strip('"').strip("'")
    return result


class Bridge:
    def __init__(self, config, state=None):
        self.config_path = Path(config).expanduser().resolve()
        self.state_path = Path(state or os.environ.get('ENGINEBRIDGE_STATE', '~/.local/state/enginebridge/state.sqlite')).expanduser()

    def load(self):
        try:
            d = yaml.safe_load(self.config_path.read_text())
        except (OSError, yaml.YAMLError) as e:
            raise BridgeError('Configuração indisponível ou YAML inválido') from e
        if not isinstance(d, dict) or d.get('version') != 1:
            raise BridgeError('Configuração exige version: 1')
        if not isinstance(d.get('motores'), dict) or not isinstance(d.get('global'), dict):
            raise BridgeError('Configuração exige global e motores')
        return d

    def resolve(self, project, stage, motor=None, nivel=None):
        d = self.load()
        try:
            project_cfg = d['projetos'][project]
            step = project_cfg['etapas'][stage]
        except (KeyError, TypeError) as e:
            raise BridgeError('Projeto ou etapa desconhecidos; não usar padrão silencioso') from e
        global_cfg = d['global']
        profiles = d.get('perfis', {})
        chosen_profile = profiles.get(step.get('perfil')) if step.get('perfil') else None
        if step.get('perfil') and chosen_profile is None:
            raise BridgeError('Perfil inexistente')
        if motor and (step.get('motor') or chosen_profile) and motor != (chosen_profile or step).get('motor'):
            raise BridgeError('Etapa fixada; altere a política para trocar seu motor')
        level = nivel or step.get('nivel') or project_cfg.get('nivel') or global_cfg.get('nivel_padrao', 'executor')
        if level not in {'menor', 'executor', 'topo', 'super'}:
            raise BridgeError('Nível inválido')
        first = motor or (chosen_profile or {}).get('motor') or step.get('motor') or project_cfg.get('motor') or global_cfg.get('motor_preferido')
        explicit = step.get('alternativa')
        alternatives = [explicit] if isinstance(explicit, str) else explicit
        if alternatives is None:
            alternatives = [] if (chosen_profile or step.get('motor')) else project_cfg.get('alternativas', global_cfg.get('alternativas', []))
        if not isinstance(alternatives, list) or any(not isinstance(x, str) for x in alternatives):
            raise BridgeError('Alternativas devem ser nomes de motores ou perfis')
        candidates = [(first, chosen_profile)]
        for alt in alternatives:
            profile = profiles.get(alt)
            candidates.append(((profile or {}).get('motor', alt), profile))
        central = env_file(d.get('modelos_env', '~/.config/inema/modelos.env'))
        routes, excluded, seen = [], [], set()
        timeout = global_cfg.get('timeout', 180)
        cooldown = global_cfg.get('cooldown', 300)
        if type(timeout) is not int or not 1 <= timeout <= 1800 or type(cooldown) is not int or not 1 <= cooldown <= 86400:
            raise BridgeError('Timeout 1–1800s e cooldown 1–86400s obrigatórios')
        for engine, profile in candidates:
            cfg = d['motores'].get(engine)
            if cfg is None:
                raise BridgeError(f'Motor inexistente: {engine}')
            # Permission/capability gates precede preferences, even for pinned routes.
            if cfg.get('habilitado') is not True or cfg.get('tipo') != 'assinatura' or engine not in {'codex', 'claude'}:
                excluded.append({'motor': engine, 'motivo': 'desabilitado ou adaptador não autorizado/implementado'})
                continue
            values = dict(cfg.get('niveis', {}).get(level, {}))
            values.update({k: v for k, v in (profile or {}).items() if k in {'modelo', 'esforco'}})
            key = f'INEMA_{engine.upper()}_{level.upper()}'
            model = values.get('modelo', central.get(key))
            effort = values.get('esforco', central.get(key + '_EFFORT', ''))
            if not model or not isinstance(model, str) or not isinstance(effort, str):
                raise BridgeError(f'Modelo/esforço inválidos ou ausentes: {engine}/{level}')
            allowed = {'', 'low', 'medium', 'high', 'xhigh'} if engine == 'codex' else {'', 'low', 'medium', 'high', 'max'}
            if effort not in allowed:
                raise BridgeError(f'Esforço não suportado pelo adaptador {engine}: {effort}')
            pool = cfg.get('quota_pool')
            if not isinstance(pool, str) or not pool:
                raise BridgeError('quota_pool explícito obrigatório; modelos da mesma conta compartilham cota')
            route = {'motor': engine, 'tipo': 'assinatura', 'modelo': model, 'esforco': effort, 'quota_pool': pool, 'timeout': timeout,
                     'binario': str(Path(cfg.get('binario', engine)).expanduser()), 'conta_env': cfg.get('conta_env')}
            route['codex_home'] = env_file(cfg['conta_env']).get('CODEX_HOME') if cfg.get('conta_env') else None
            identity = (engine, model, effort, pool)
            if identity not in seen:
                routes.append(route)
                seen.add(identity)
        if not routes:
            raise BridgeError('Nenhuma rota permitida para esta etapa')
        source = json.dumps(d, sort_keys=True) + json.dumps(central, sort_keys=True)
        return {'version': 1, 'policy_hash': hashlib.sha256(source.encode()).hexdigest(), 'projeto': project, 'etapa': stage, 'nivel': level,
                'modo': 'texto-sem-ferramentas', 'rotas': routes, 'excluidos': excluded, 'cooldown': cooldown,
                'origem_modelos': d.get('modelos_env'), 'aviso': 'Resolução local; não verifica saldo, login ou disponibilidade do modelo.'}

    def execute(self, snapshot, prompt, runner=None, validator=None):
        from .adapters import run_text
        if snapshot.get('modo') != 'texto-sem-ferramentas':
            raise BridgeError('Somente texto sem ferramentas; efeitos externos exigem integração própria')
        runner = runner or run_text
        state = State(self.state_path)
        attempts = []
        for route in snapshot['rotas']:
            current = self.load()['motores'].get(route['motor'], {})
            # Frozen model selection, but urgent policy/account blocks apply at admission.
            if current.get('habilitado') is not True or current.get('tipo') != 'assinatura' or current.get('quota_pool') != route['quota_pool']:
                attempts.append({'motor': route['motor'], 'status': 'politica-bloqueou'})
                continue
            current_home = env_file(current['conta_env']).get('CODEX_HOME') if current.get('conta_env') else None
            if current_home != route.get('codex_home'):
                raise BridgeError('Conta alterada desde a resolução; resolva um novo trabalho')
            owner = state.acquire(route['quota_pool'], route['timeout'] + 30)
            if owner is None:
                attempts.append({'motor': route['motor'], 'status': 'pool-indisponivel'})
                continue
            try:
                result = runner(route, prompt)
                code = result.get('status')
                attempts.append({'motor': route['motor'], 'status': code})
                if code == 'ok':
                    if not isinstance(result.get('texto'), str) or not result['texto'].strip():
                        raise BridgeError('Resposta vazia; sem fallback por erro de conteúdo')
                    if validator and not validator(result['texto']):
                        raise BridgeError('Validador do consumidor recusou; sem fallback automático')
                    return {'status': 'ok', 'texto': result['texto'], 'rota': route, 'tentativas': attempts, 'policy_hash': snapshot['policy_hash']}
                if code in {'quota', 'rate_limit'} and result.get('sem_execucao') is True:
                    state.cooldown(route['quota_pool'], snapshot['cooldown'])
                    continue
                raise BridgeError(f'Execução interrompida ({code}); resultado incerto ou erro local, sem repetição automática')
            finally:
                state.release(route['quota_pool'], owner)
        raise BridgeError('Rotas esgotadas ou suspensas; aguarde ou ajuste a política')
