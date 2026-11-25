import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

import yaml

from . import Bridge, BridgeError, __version__
from .state import State


def main():
    p = argparse.ArgumentParser(description='EngineBridge — política local e assinaturas, sem chamadas implícitas')
    p.add_argument('--version', action='version', version=__version__)
    p.add_argument('--config', default=os.environ.get('ENGINEBRIDGE_CONFIG', 'config/enginebridge.yaml'))
    p.add_argument('--state', default=None)
    sub = p.add_subparsers(dest='action', required=True)
    for name in ('resolve', 'run'):
        s = sub.add_parser(name)
        s.add_argument('--project', required=True)
        s.add_argument('--stage', required=True)
        s.add_argument('--motor', choices=['codex', 'claude'])
        s.add_argument('--nivel', choices=['menor', 'executor', 'topo', 'super'])
        if name == 'run':
            s.add_argument('--simulate', action='store_true', help='Executores fictícios; nêo chama modelos')
            s.add_argument('--fail-first', action='store_true', help='Somente simulaçêo: rejeiçêo de cota no primeiro motor')
    sub.add_parser('status')
    for name in ('block', 'unblock'):
        s = sub.add_parser(name)
        s.add_argument('--pool', required=True)
    s = sub.add_parser('prefer')
    s.add_argument('motor', choices=['codex', 'claude'])
    args = p.parse_args()
    bridge = Bridge(args.config, args.state)
    try:
        if args.action in ('resolve', 'run'):
            snapshot = bridge.resolve(args.project, args.stage, args.motor, args.nivel)
            if args.action == 'resolve':
                result = snapshot
            else:
                if args.fail_first and not args.simulate:
                    raise BridgeError('--fail-first exige --simulate')
                runner = None
                if args.simulate:
                    calls = []
                    def runner(route, prompt):
                        calls.append(route['motor'])
                        if args.fail_first and len(calls) == 1:
                            return {'status': 'quota', 'sem_execucao': True}
                        return {'status': 'ok', 'texto': 'SIMULADO: ' + route['motor'] + ' recebeu ' + str(len(prompt)) + ' caracteres'}
                result = bridge.execute(snapshot, sys.stdin.read(), runner=runner)
                result['simulado'] = args.simulate
        elif args.action == 'prefer':
            d = bridge.load()
            if d['motores'][args.motor].get('habilitado') is not True:
                raise BridgeError('Motor desabilitado')
            # Preserve YAML comments and formatting; replace the single global key only.
            import re
            raw = bridge.config_path.read_text()
            changed, n = re.subn(r'^(  motor_preferido:)[^\n]*$', r'\g<1> ' + args.motor, raw, flags=re.M)
            if n != 1 or yaml.safe_load(changed)['global']['motor_preferido'] != args.motor:
                raise BridgeError('Edite motor_preferido manualmente; formato fora do padrêo')
            fd, tmp = tempfile.mkstemp(dir=bridge.config_path.parent)
            try:
                with os.fdopen(fd, 'w') as f:
                    f.write(changed)
                    f.flush()
                    os.fsync(f.fileno())
                os.chmod(tmp, bridge.config_path.stat().st_mode & 0o777)
                os.replace(tmp, bridge.config_path)
            finally:
                if Path(tmp).exists():
                    Path(tmp).unlink()
            result = {'motor_preferido': args.motor, 'efeito': 'próximas resoluções dos consumidores integrados'}
        else:
            state = State(bridge.state_path)
            if args.action != 'status':
                state.block(args.pool, args.action == 'block')
            result = state.status()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (BridgeError, OSError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({'status': 'erro', 'mensagem': str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2
