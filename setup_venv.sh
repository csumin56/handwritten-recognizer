#!/usr/bin/env bash
set -euo pipefail

target="${1:-desktop}"

case "$target" in
  desktop)
    requirements="desktop_version/requirements.txt"
    run_cmd="python3 desktop_version/handwritten_digit_recognizer.py"
    ;;
  web)
    requirements="web_version/requirements.txt"
    run_cmd="python3 web_version/app.py"
    ;;
  *)
    echo "Usage: $0 [desktop|web]" >&2
    exit 1
    ;;
esac

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r "$requirements"
echo "Setup complete. Run: source .venv/bin/activate && $run_cmd"
