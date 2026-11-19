#!/usr/bin/env bash
set -euo pipefail
# Run from the repository root. Resolution only: zero inference.
python3 -m enginebridge resolve --project consumidor-cli --stage critica
