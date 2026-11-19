"""Subscription CLIs only. No SDK, HTTP endpoint or API-key discovery."""
import json
import os
import signal
import subprocess
import tempfile
from pathlib import Path

from .core import env_file


def clean_environment(route):
    env = {k: v for k, v in os.environ.items() if not any(s in k.upper() for s in
           ('API_KEY', 'AUTH_TOKEN', 'BASE_URL', 'OPENAI_', 'ANTHROPIC_', 'OPENROUTER_', 'CLAUDE_CODE_', 'CLAUDECODE', 'MODEL_PROVIDER', 'CODEX_HOME'))}
    if route.get('codex_home'):
        env['CODEX_HOME'] = route['codex_home']
    return env


def command(route):
    if route['motor'] == 'codex':
        args = [route['binario'], 'exec', '--ephemeral', '--ignore-user-config', '--ignore-rules',
                '--skip-git-repo-check', '--json', '-s', 'read-only', '-m', route['modelo'],
                '-c', 'approval_policy="never"', '-c', 'forced_login_method="chatgpt"', '-c', 'model_provider="openai"']
        for feature in ('shell_tool', 'unified_exec', 'code_mode', 'code_mode_host', 'apps', 'browser_use', 'computer_use', 'image_generation', 'multi_agent', 'multi_agent_v2'):
            args.extend(['--disable', feature])
        if route['esforco']:
            args.extend(['-c', 'model_reasoning_effort=' + json.dumps(route['esforco'])])
        return args + ['-']
    args = [route['binario'], '-p', '--output-format', 'json', '--model', route['modelo'], '--tools', '',
            '--safe-mode', '--restricted', '--strict-mcp-config', '--mcp-config', '{"mcpServers":{}}',
            '--setting-sources', '', '--no-session-persistence']
    if route['esforco']:
        args += ['--effort', route['esforco']]
    return args


def parse_output(engine, raw, returncode):
    try:
        if engine == 'claude':
            data = json.loads(raw)
            if returncode == 0 and data.get('type') == 'result' and not data.get('is_error'):
                return {'status': 'ok', 'texto': data.get('result', '')}
            # Only an explicit machine-readable rejection allows fallback.
            # Real Claude Code format (16/11/2026): top-level api_error* fields, result carries the
            # human message ("You've hit your weekly limit · resets ..."), terminal_reason api_error.
            if data.get('is_error') is True and data.get('terminal_reason') == 'api_error':
                if data.get('api_error') == 'usage_limit_reached':
                    return {'status': 'quota', 'sem_execucao': True}
                if data.get('api_error_status') == 429 or data.get('api_error_type') == 'rate_limit_error':
                    return {'status': 'rate_limit', 'sem_execucao': True}
            code = data.get('error', {}).get('type') if isinstance(data.get('error'), dict) else None
            if code in {'rate_limit_error', 'usage_limit_reached'} and not data.get('result'):
                return {'status': 'rate_limit' if code == 'rate_limit_error' else 'quota', 'sem_execucao': True}
        else:
            events = [json.loads(line) for line in raw.splitlines() if line.strip()]
            texts, completed, effect = [], False, False
            failure = None
            for event in events:
                item = event.get('item', {})
                if item.get('type') in {'command_execution', 'mcp_tool_call', 'file_change', 'web_search'}:
                    effect = True
                if event.get('type') == 'item.completed' and item.get('type') == 'agent_message':
                    texts.append(item.get('text', ''))
                if event.get('type') == 'turn.completed':
                    completed = True
                if event.get('type') == 'turn.failed':
                    failure = event.get('error', {})
            if effect:
                return {'status': 'ferramenta-inesperada'}
            if returncode == 0 and completed and failure is None:
                return {'status': 'ok', 'texto': '\n'.join(texts)}
            code = failure.get('code') if isinstance(failure, dict) else None
            if code in {'usage_limit_reached', 'rate_limit_exceeded'} and not texts and not completed:
                return {'status': 'quota' if code == 'usage_limit_reached' else 'rate_limit', 'sem_execucao': True}
    except (ValueError, AttributeError, TypeError):
        pass
    # Human error messages are deliberately not classified by substring.
    return {'status': 'erro-incerto'}


def run_text(route, prompt):
    if not Path(route['binario']).is_file():
        return {'status': 'binario-ausente'}
    with tempfile.TemporaryDirectory(prefix='enginebridge-') as cwd:
        # Temporary files bound memory use; bounded prompt and result protect callers.
        if len(prompt.encode()) > 1_000_000:
            return {'status': 'entrada-excessiva'}
        try:
            with tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as errors:
                proc = subprocess.Popen(command(route), stdin=subprocess.PIPE, stdout=output, stderr=errors,
                                        cwd=cwd, env=clean_environment(route), start_new_session=True)
                try:
                    proc.communicate(prompt.encode(), timeout=route['timeout'])
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.communicate()
                    return {'status': 'timeout-incerto'}
                output.seek(0, 2)
                if output.tell() > 8_000_000:
                    return {'status': 'saida-excessiva'}
                output.seek(0)
                return parse_output(route['motor'], output.read().decode('utf-8', errors='replace'), proc.returncode)
        except OSError:
            return {'status': 'erro-local'}
