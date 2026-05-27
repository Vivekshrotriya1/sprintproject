#!/usr/bin/env bash
set -e

cd /home/site/wwwroot

APP_PYTHON="/opt/python/3.10.20/bin/python"

if [ ! -x "$APP_PYTHON" ]; then
  APP_PYTHON="python"
fi

export PYTHONPATH="/home/site/wwwroot:/home/site/wwwroot/api:${PYTHONPATH}"

if ! "$APP_PYTHON" -c "import uvicorn" >/dev/null 2>&1; then
  echo "Python packages not found. Installing app dependencies..."
  rm -rf /tmp/app_packages
  mkdir -p /tmp/app_packages
  "$APP_PYTHON" -m pip install --upgrade pip
  "$APP_PYTHON" -m pip install -r requirements.txt --target="/tmp/app_packages"
  export PYTHONPATH="/tmp/app_packages:${PYTHONPATH}"
fi

mkdir -p /app
ln -sfn /home/site/wwwroot/models /app/models
ln -sfn /home/site/wwwroot/data /app/data

"$APP_PYTHON" -m uvicorn api.app:app --host 0.0.0.0 --port "${PORT:-8000}"
