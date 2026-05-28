#!/usr/bin/env bash
set -e

APP_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_ROOT"

APP_PYTHON="/opt/python/3.10.20/bin/python"

if [ ! -x "$APP_PYTHON" ]; then
  APP_PYTHON="python"
fi

export PYTHONPATH="${APP_ROOT}:${APP_ROOT}/api:${PYTHONPATH}"

if [ -d "${APP_ROOT}/.python_packages/lib/site-packages" ]; then
  export PYTHONPATH="${APP_ROOT}/.python_packages/lib/site-packages:${PYTHONPATH}"
fi

if ! "$APP_PYTHON" -c "import uvicorn" >/dev/null 2>&1; then
  echo "Python packages not found. Installing app dependencies..."
  rm -rf /tmp/app_packages
  mkdir -p /tmp/app_packages
  "$APP_PYTHON" -m pip install --upgrade pip
  "$APP_PYTHON" -m pip install -r requirements.txt --target="/tmp/app_packages"
  export PYTHONPATH="/tmp/app_packages:${PYTHONPATH}"
fi

mkdir -p /app
ln -sfn "${APP_ROOT}/models" /app/models
ln -sfn "${APP_ROOT}/data" /app/data

"$APP_PYTHON" -m uvicorn api.app:app --host 0.0.0.0 --port "${PORT:-8000}"
