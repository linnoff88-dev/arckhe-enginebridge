"""Build static guides from validated, persisted text translations."""
from pathlib import Path
import html,json,re
p=Path(__file__).resolve().parents[1]
css=(p/'scripts/guia-template.html').read_text().split('<style>')[1].split('</style>')[0]
css+='\n.grid>*{min-width:0} h1,h2,h3{overflow-wrap:anywhere} .techhead{padding:42px 0;background:var(--bg2);border-top:2px solid var(--amb)} .techzone{background:var(--bg2)} .wideimg{width:100%;display:block;border-radius:14px;margin-top:24px} a:focus-visible,button:focus-visible{outline:3px solid var(--sky);outline-offset:4px} body.light nav{background:rgba(246,247,249,.96)} @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}\n'
install='''git clone https://github.com/inematds/enginebridge.git
cd enginebridge
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
python3 -m enginebridge resolve --project demonstracao --stage roteiro'''
simulate="printf 'Escreva um roteiro.' | python3 -m enginebridge --state .state/demo.sqlite run --project demonstracao --stage roteiro --simulate --fail-first"
commands='''python3 -m enginebridge prefer claude
python3 -m enginebridge resolve --project demonstracao --stage padrao
python3 -m enginebridge prefer codex
python3 -m enginebridge resolve --project demonstracao --stage padrao
python3 -m enginebridge --state .state/demo.sqlite block --pool codex-principal
python3 -m enginebridge --state .state/demo.sqlite unblock --pool codex-principal'''
real="printf 'Responda com uma frase.' | python3 -m enginebridge run --project demonstracao --stage roteiro"
config='''perfis:
  codex-principal:
    motor: codex
    modelo: gpt-6.1-sol
    esforco: medium
  claude-alternativo:
    motor: claude
    modelo: claude-opus-5-5
    esforco: low
projetos:
  demonstracao:
    etapas:
      roteiro:
        perfil: codex-principal
        alternativa: claude-alternativo
      critica:
        perfil: claude-alternativo
        alternativa: codex-principal'''
e=html.escape
for lang in ['pt','en','es']:
 file=p/f'i18n/{lang}.json'
 if not file.exists(): continue
 d=json.loads(file.read_text());prefix='' if lang=='pt' else '../';suffix='' if lang=='pt' else '-'+lang
 dest=p/'guia' if lang=='pt' else p/'guia'/lang;dest.mkdir(parents=True,exist_ok=True)
 languages=''.join(f'<a class="{"on" if l==lang else ""}" href="{("./" if l=="pt" else l+"/") if lang=="pt" else ("../" if l=="pt" else "./" if l==lang else "../"+l+"/")}">{l.upper()}</a>' for l in ['pt','en','es'])
 def section(id,title,text,extra=''):
  return f'<section id="{id}"><div class="wrap"><h2>{e(title)}</h2><p class="sub">{e(text)}</p>{extra}</div></section>'
 def pre(code):return '<pre><code>'+e(code)+'</code></pre>'
 repo='https://github.com/inematds/enginebridge'
 alternates=''.join(f'<link rel="alternate" hreflang="{l if l!="pt" else "pt-BR"}" href="https://inematds.github.io/enginebridge/guia/{l+"/" if l!="pt" else ""}">' for l in ['pt','en','es'])
 out=f'''<!doctype html><html lang="{'pt-BR' if lang=='pt' else lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EngineBridge — {e(d['tagline'])}</title><meta name="description" content="{e(d['portal_description'])}">{alternates}<link rel="canonical" href="https://inematds.github.io/enginebridge/guia/{lang+'/' if lang!='pt' else ''}"><link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"><style>{css}</style></head><body>
<nav><div class="wrap"><a class="brand" href="#top">EngineBridge</a><span class="sep">|</span><span class="clubpro"><a class="inema" href="https://inema.club">INEMA.CLUB</a><span class="sep">-</span><a class="pro" href="https://inema.pro">PRO</a></span><div class="links"><a class="sec" href="#fluxo">{e(d['understand'])}</a><a class="sec" href="#tecnico">{e(d['technical'])}</a><span class="lang">{languages}</span><button class="tgl" id="themeToggle" aria-label="{e(d['theme'])}">☀️</button><a class="btn" href="{repo}">GitHub</a></div></div></nav>
<header class="hero" id="top"><div class="glow"></div><div class="wrap"><div><h1>{e(d['hero'])}</h1><p class="lead">{e(d['lead'])}</p><div class="cta"><a class="btn" href="#fluxo">{e(d['understand'])}</a><a class="btn ghost" href="{repo}">{e(d['github'])}</a></div><p class="mut">{e(d['status'])}</p></div><figure><img src="{prefix}assets/banner{suffix}.jpg" alt="EngineBridge — {e(d['tagline'])}" width="1400" height="788"></figure></div></header>
<section id="resumo" class="resumo"><div class="wrap"><h2>{e(d['summary_title'])}</h2><p>{e(d['summary'])}</p><img class="wideimg" src="{prefix}assets/banner-grade{suffix}.jpg" alt="{e(d['mechanism'])}" width="1400" height="788" loading="lazy"></div></section>
<!-- VIDEO: entra o explicavideo do projeto quando publicado -->
'''
 flow='<div class="flow">'+'<span class="arr" aria-hidden="true">→</span>'.join('<span>'+e(x)+'</span>' for x in d['flow'])+'</div>'
 out+=section('fluxo',d['mechanism'],d['mechanism_text'],flow)
 cases='<div class="grid g3">'+''.join('<div class="card"><h3>'+e(t)+'</h3><p>'+e(v)+'</p></div>' for t,v in d['cases'])+'</div>'
 out+=section('continuidade',d['meaning_title'],d['meaning_text'],cases)
 out+=section('estado',d['limits_title'],d['limits_text'])
 out+=section('niveis',d['effort_title'],d['effort_text'])
 out+=f'<div class="techhead" id="tecnico"><div class="wrap"><h2>{e(d["technical_title"])}</h2><p>{e(d["technical_text"])}</p></div></div><div class="techzone">'
 out+=section('glossario',d['glossary_title'],d['glossary_text'])
 for id,title,text,code in [('guia','install_title','install_text',install),('simular','simulate_title','simulate_text',simulate),('config','config_title','config_text',config),('contas','auth_title','auth_text','codex login\nclaude auth login\nmkdir -p ~/.config/inema\ntest -f ~/.config/inema/modelos.env || cp config/modelos.example.env ~/.config/inema/modelos.env'),('comandos','commands_title','commands_text',commands),('executar','real_title','real_text',real)]:
  out+=section(id,d[title],d[text],pre(code))
 docs=''.join(f'<p><a href="{repo}/blob/main/docs/{f}">{e(d[k])}</a></p>' for k,f in [('docs','ARQUITETURA.md'),('plan','ADOCAO.md'),('references','REFERENCIAS.md')])
 out+=section('roadmap',d['adoption_title'],d['adoption_text'],docs)
 out+=f'''</div><footer><div class="wrap"><p>EngineBridge · {e(d['footer'])}</p><p><a href="{repo}">GitHub</a> · <a href="https://inema.club">INEMA.CLUB</a></p></div></footer><script>(function(){{var k='enginebridge-theme',b=document.body,t=document.getElementById('themeToggle');function paint(){{t.textContent=b.classList.contains('light')?'🌙':'☀️'}}try{{if(localStorage.getItem(k)==='light')b.classList.add('light')}}catch(e){{}}paint();t.addEventListener('click',function(){{b.classList.toggle('light');paint();try{{localStorage.setItem(k,b.classList.contains('light')?'light':'dark')}}catch(e){{}}}})}})();</script></body></html>'''
 (dest/'index.html').write_text(out)
 if lang!='pt': (p/f'README.{lang}.md').write_text(d['readme'].rstrip()+'\n')
print('Guias gerados')
