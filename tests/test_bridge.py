import copy
import json
import multiprocessing
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import yaml
from enginebridge import Bridge, BridgeError
from enginebridge.adapters import clean_environment, command, parse_output, run_text
from enginebridge.state import State


ROOT = Path(__file__).resolve().parents[1]


def claim(path, queue):
    queue.put(State(path).acquire('shared', 10))


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.env = self.root / 'models.env'
        self.env.write_text('INEMA_CODEX_EXECUTOR=central-codex\nINEMA_CODEX_EXECUTOR_EFFORT=medium\nINEMA_CLAUDE_EXECUTOR=central-claude\nINEMA_CLAUDE_EXECUTOR_EFFORT=low\n')
        self.cfg = yaml.safe_load((ROOT / 'config/enginebridge.yaml').read_text())
        self.cfg['modelos_env'] = str(self.env)
        self.cfg['motores']['codex'].pop('conta_env')
        self.path = self.root / 'policy.yaml'
        self.db = self.root / 'state.sqlite'
        self.save()
        self.b = Bridge(self.path, self.db)

    def tearDown(self):
        self.tmp.cleanup()

    def save(self):
        self.path.write_text(yaml.safe_dump(self.cfg, sort_keys=False))

    def resolved(self):
        return self.b.resolve('consumidor-python', 'roteiro')

    def test_central_source_and_per_engine_effort(self):
        routes = self.resolved()['rotas']
        self.assertEqual([(r['modelo'], r['esforco']) for r in routes], [('central-codex', 'medium'), ('central-claude', 'low')])

    def test_profile_is_explicit_exception(self):
        r = self.b.resolve('demonstracao', 'roteiro')['rotas'][0]
        self.assertEqual(r['modelo'], 'gpt-6.1-sol')

    def test_global_switch_and_pin(self):
        self.cfg['global']['motor_preferido'] = 'claude'
        self.save()
        self.assertEqual(self.resolved()['rotas'][0]['motor'], 'claude')
        self.assertEqual(self.b.resolve('demonstracao', 'roteiro')['rotas'][0]['motor'], 'codex')
        with self.assertRaises(BridgeError):
            self.b.resolve('demonstracao', 'roteiro', motor='claude')

    def test_unknown_stage_and_profile_fail_closed(self):
        with self.assertRaises(BridgeError):
            self.b.resolve('unknown', 'script')
        self.cfg['projetos']['demonstracao']['etapas']['roteiro']['perfil'] = 'typo'
        self.save()
        with self.assertRaises(BridgeError):
            self.b.resolve('demonstracao', 'roteiro')

    def test_api_cannot_be_enabled_by_config(self):
        self.cfg['motores']['openrouter']['habilitado'] = True
        self.cfg['global'].update(motor_preferido='openrouter', alternativas=[])
        self.save()
        with self.assertRaises(BridgeError):
            self.resolved()

    def test_snapshot_keeps_model_but_honors_urgent_block(self):
        snapshot = self.resolved()
        self.env.write_text(self.env.read_text().replace('central-codex', 'new-model'))
        seen = []
        def run(r, p):
            seen.append(r['modelo'])
            return {'status': 'ok', 'texto': 'valid'}
        self.b.execute(snapshot, 'text', runner=run)
        self.assertEqual(seen, ['central-codex'])
        State(self.db).block('codex-principal')
        result = self.b.execute(snapshot, 'text', runner=run)
        self.assertEqual(result['rota']['motor'], 'claude')

    def test_disabled_route_applies_to_snapshot(self):
        snapshot = self.resolved()
        self.cfg['motores']['codex']['habilitado'] = False
        self.save()
        result = self.b.execute(snapshot, 'text', runner=lambda r, p: {'status': 'ok', 'texto': 'ok'})
        self.assertEqual(result['rota']['motor'], 'claude')

    def test_account_drift_refused(self):
        snap = self.resolved()
        env = self.root / 'account.env'
        env.write_text('CODEX_HOME=/another-account')
        self.cfg['motores']['codex']['conta_env'] = str(env)
        self.save()
        with self.assertRaisesRegex(BridgeError, 'Conta alterada'):
            self.b.execute(snap, 'text')

    def test_quota_fallback_persists_and_does_not_need_llm(self):
        calls = []
        def run(r, p):
            calls.append(r['motor'])
            return {'status': 'quota', 'sem_execucao': True} if r['motor'] == 'codex' else {'status': 'ok', 'texto': 'ok'}
        snap = self.resolved()
        self.b.execute(snap, 'same prompt', runner=run)
        Bridge(self.path, self.db).execute(snap, 'same prompt', runner=run)
        self.assertEqual(calls, ['codex', 'claude', 'claude'])

    def test_shared_pool_blocks_other_model(self):
        snap = self.resolved()
        snap['rotas'][1]['quota_pool'] = snap['rotas'][0]['quota_pool']
        calls = []
        def run(r, p):
            calls.append(r['modelo'])
            return {'status': 'quota', 'sem_execucao': True}
        # Same pool identity in live policy too.
        self.cfg['motores']['claude']['quota_pool'] = 'codex-principal'
        self.save()
        with self.assertRaises(BridgeError):
            self.b.execute(snap, 'text', runner=run)
        self.assertEqual(len(calls), 1)

    def test_uncertain_local_content_errors_do_not_fallback(self):
        for status in ['timeout-incerto', 'erro-local', 'erro-incerto', 'quota']:
            calls = []
            def run(r, p):
                calls.append(r['motor'])
                return {'status': status}
            with self.assertRaises(BridgeError):
                self.b.execute(self.resolved(), 'text', runner=run)
            self.assertEqual(len(calls), 1)

    def test_validator_refusal_no_retry(self):
        calls = []
        def run(r, p):
            calls.append(r['motor'])
            return {'status': 'ok', 'texto': 'wrong-format'}
        with self.assertRaises(BridgeError):
            self.b.execute(self.resolved(), 'text', runner=run, validator=lambda t: False)
        self.assertEqual(len(calls), 1)

    def test_pool_atomic_across_processes(self):
        State(self.db)
        queue = multiprocessing.Queue()
        workers = [multiprocessing.Process(target=claim, args=(self.db, queue)) for _ in range(4)]
        for w in workers:
            w.start()
        for w in workers:
            w.join(10)
            self.assertEqual(w.exitcode, 0)
        owners = [queue.get(timeout=2) for _ in workers]
        self.assertEqual(sum(x is not None for x in owners), 1)

    def test_expired_cooldown_recovery_and_owner_release(self):
        state = State(self.db)
        state.cooldown('pool', 10)
        self.assertIsNone(state.acquire('pool', 5))
        with state.connect() as db:
            db.execute('UPDATE pools SET until=0')
        owner = state.acquire('pool', 5)
        state.release('pool', 'wrong-owner')
        self.assertIsNone(state.acquire('pool', 5))
        state.release('pool', owner)
        self.assertIsNotNone(state.acquire('pool', 5))

    def test_cli_and_shell_consumer_use_same_resolution(self):
        env = dict(os.environ, ENGINEBRIDGE_CONFIG=str(self.path))
        p = subprocess.run([sys.executable, '-m', 'enginebridge', 'resolve', '--project', 'consumidor-python', '--stage', 'roteiro'], cwd=ROOT, env=env, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['rotas'], self.resolved()['rotas'])

    def test_fake_binary_integration(self):
        binary = self.root / 'fake-codex'
        binary.write_text('#!/usr/bin/env python3\nimport json,sys\np=sys.stdin.read()\nprint(json.dumps({"type":"item.completed","item":{"type":"agent_message","text":"reply:"+p}}))\nprint(json.dumps({"type":"turn.completed"}))\n')
        binary.chmod(0o700)
        route = self.resolved()['rotas'][0]
        route['binario'] = str(binary)
        self.assertEqual(run_text(route, 'nonce')['texto'], 'reply:nonce')

    def test_timeout_actual_process(self):
        binary = self.root / 'slow'
        binary.write_text('#!/usr/bin/env python3\nimport time\ntime.sleep(15)\n')
        binary.chmod(0o700)
        route = self.resolved()['rotas'][0]
        route.update(binario=str(binary), timeout=1)
        start = time.monotonic()
        self.assertEqual(run_text(route, 'text')['status'], 'timeout-incerto')
        self.assertLess(time.monotonic() - start, 4)

    def test_no_api_credentials_or_shell_substitution(self):
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-secret', 'OPENAI_BASE_URL': 'bad', 'CLAUDE_CODE_USE_BEDROCK': '1'}):
            env = clean_environment(self.resolved()['rotas'][0])
        self.assertNotIn('ANTHROPIC_API_KEY', env)
        self.assertNotIn('OPENAI_BASE_URL', env)
        self.assertNotIn('CLAUDE_CODE_USE_BEDROCK', env)
        self.assertIn('forced_login_method="chatgpt"', command(self.resolved()['rotas'][0]))

    def test_invalid_effort_refused_not_translated(self):
        self.cfg['perfis']['codex-principal']['esforco'] = 'max'
        self.save()
        with self.assertRaises(BridgeError):
            self.b.resolve('demonstracao', 'roteiro')

    def test_parser_does_not_treat_prose_as_quota(self):
        self.assertEqual(parse_output('codex', 'quota reached', 1)['status'], 'erro-incerto')
        data = json.dumps({'type': 'turn.failed', 'error': {'code': 'usage_limit_reached'}})
        self.assertEqual(parse_output('codex', data, 1)['status'], 'quota')
        prefix = json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'partial'}})
        self.assertEqual(parse_output('codex', prefix + '\n' + data, 1)['status'], 'erro-incerto')

    def test_real_claude_weekly_limit_is_quota(self):
        # Real Claude Code rejection, 16/11/2026 (r7ex critic); account ids removed.
        real = json.dumps({'type': 'result', 'subtype': 'success', 'is_error': True, 'api_error_status': 429,
                           'api_error_type': 'rate_limit_error', 'api_error_origin': 'first_party',
                           'api_error': 'usage_limit_reached', 'terminal_reason': 'api_error', 'num_turns': 1,
                           'result': "You've hit your weekly limit · resets 9pm (America/Sao_Paulo)"})
        self.assertEqual(parse_output('claude', real, 1)['status'], 'quota')
        ok = json.dumps({'type': 'result', 'is_error': False, 'result': "You've hit your weekly limit"})
        self.assertEqual(parse_output('claude', ok, 0)['status'], 'ok')


if __name__ == '__main__':
    unittest.main()
