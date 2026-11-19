# EngineBridge

[![EngineBridge](guia/assets/banner-es.jpg)](https://inematds.github.io/enginebridge/guia/es/)

**[Português](README.md) · [English](README.en.md) · [Español](README.es.md)**

## Qué es

Tu automatización puede detenerse cuando una suscripción alcanza su cuota, aunque haya otra disponible. EngineBridge es una herramienta local para elegir qué motor de IA atiende cada etapa y usar una alternativa declarada cuando esté permitido. Está pensada para quienes mantienen bots, scripts y rutinas con Claude Code y Codex. Tú defines los perfiles, modelos y esfuerzo; el programa resuelve la elección sin consultar a una IA. Para ejecutar textos, se necesitan Python y los programas autenticados mediante suscripción.

**Versión 1.0.0 — núcleo local funcional; la integración con los sistemas reales aún está pendiente.**

[Guía completa](https://inematds.github.io/enginebridge/guia/es/) · [Arquitectura](docs/ARQUITETURA.md) · [Plan de adopción](docs/ADOCAO.md) · [Referencias y revisión de Astra](docs/REFERENCIAS.md)

> Los documentos técnicos enlazados están en portugués.

## Instalar y verificar

```bash
git clone https://github.com/inematds/enginebridge.git
cd enginebridge
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
python3 -m enginebridge resolve --project demonstracao --stage roteiro
```

Requiere Python 3.11+ y PyYAML 6. Los perfiles de demostración usan modelos explícitos y se pueden resolver sin iniciar sesión. Los niveles heredados usan `~/.config/inema/modelos.env`; en otra máquina, configura `modelos_env` y las rutas de los ejecutables en el YAML. La resolución no comprueba si el modelo está disponible en la suscripción.

## Simular el cambio sin consumir modelos

```bash
printf 'Crie um roteiro curto.' | python3 -m enginebridge --state .state/demo.sqlite run --project demonstracao --stage roteiro --simulate --fail-first
python3 -m enginebridge --state .state/demo.sqlite status
```

La simulación provoca un rechazo por cuota en Codex, registra una suspensión temporal en SQLite y entrega la misma solicitud al ejecutor ficticio Claude. El campo `simulado` distingue esta salida de una ejecución real. No modifica servicios, no consulta el saldo ni llama a modelos.

## Preparar cuentas en una máquina nueva

Instala Claude Code y Codex, inicia sesión con tu suscripción desde la terminal y ajusta `binario` en el YAML. Nunca uses una clave de API. El campo opcional `conta_env` apunta a un archivo de datos con `CODEX_HOME=/caminho/da/conta`; sin ese archivo, se usa la cuenta predeterminada de Codex.

```bash
codex login
claude auth login
mkdir -p ~/.config/inema
test -f ~/.config/inema/modelos.env || cp config/modelos.example.env ~/.config/inema/modelos.env
```

El ejemplo de modelos solo se copia si no existe una configuración central. La etapa `demonstracao/padrao` hereda el motor global y permite observar el cambio con `prefer`; roteiro y crítica siguen usando perfiles fijados.

## Preferencia global y excepciones

```bash
python3 -m enginebridge prefer claude
python3 -m enginebridge resolve --project demonstracao --stage padrao
python3 -m enginebridge prefer codex
python3 -m enginebridge resolve --project demonstracao --stage padrao
```

`prefer` modifica solo este YAML y conserva los comentarios. Las etapas con `perfil` o `motor` explícito permanecen fijadas; el cambio global afecta a las etapas sin esa selección. El modelo y el esfuerzo heredados siguen obteniéndose de la fuente central existente. El esfuerzo no mide la equivalencia de calidad entre familias de modelos.

```bash
python3 -m enginebridge --state .state/demo.sqlite block --pool codex-principal
python3 -m enginebridge --state .state/demo.sqlite unblock --pool codex-principal
```

Suspender una cuenta impide nuevas admisiones en EngineBridge, incluso en trabajos ya resueltos. Quitar el bloqueo manual mantiene cualquier suspensión temporal por cuota. El estado predeterminado se guarda en `~/.local/state/enginebridge/state.sqlite`; todos los consumidores de la misma máquina deben compartir esta ruta y la configuración. No pongas este SQLite en una red.

## Ejecutar un texto con la suscripción

```bash
printf 'Responda com uma frase sobre perfis por etapa.' | python3 -m enginebridge run --project demonstracao --stage roteiro
```

Este comando consume la suscripción seleccionada. Usa Claude Code o Codex en un directorio temporal, sin MCP personal, shell habilitado ni sesión nativa compartida. Se eliminan del entorno las credenciales de API. No ejecuta workflows de agente, publicación, imágenes ni traducción. Los binarios deben aceptar los argumentos documentados por el adaptador; las pruebas locales usan ejecutables ficticios y no comprueban el inicio de sesión ni el funcionamiento real de ninguna de las dos CLI.

## Contrato de continuidad

- Selección por llamada, etapa, proyecto y preferencia global, siempre sujeta a los permisos y las etapas fijadas.
- Alternativa explícita en las etapas fijadas; en las etapas libres, alternativas del proyecto o globales.
- Cuota compartida por cuenta (`quota_pool`), independiente del nombre del modelo; en este núcleo, una ejecución simultánea por pool.
- Un rechazo estructurado por cuota, sin respuesta parcial ni herramientas, permite probar la alternativa y guardar la suspensión temporal.
- Un error local, timeout, un mensaje de error solo en prosa o un resultado rechazado por el validador interrumpen el trabajo, sin reintentos automáticos.
- Cada trabajo guarda una copia resuelta de los modelos; los bloqueos urgentes y los cambios de cuenta se comprueban antes de cada intento.

Hay ejemplos de uso con Python y CLI en `examples/`. No hay integración activada con OpenPCBotV3, Refazvideo ni crons. OpenRouter aparece deshabilitado como una posible extensión futura; esta versión no incluye ningún adaptador de API, aunque alguien cambie `habilitado` en el YAML.

## Desarrollo

```bash
python3 -m compileall -q enginebridge examples tests
python3 -m unittest discover -s tests -v
python3 -m enginebridge --version
```

[Licencia MIT](LICENSE). El diseño reutiliza las referencias de proveedores independientes de WiFi y la crítica de Astra, conservadas en `docs/`.
