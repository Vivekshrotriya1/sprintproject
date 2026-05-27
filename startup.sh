#!/usr/bin/env bash
set -e

cd /home/site/wwwroot

export PYTHONPATH="/home/site/wwwroot/.python_packages/lib/site-packages:/home/site/wwwroot:/home/site/wwwroot/api:${PYTHONPATH}"

mkdir -p /app
ln -sfn /home/site/wwwroot/models /app/models

python -m uvicorn api.app:app --host 0.0.0.0 --port "${PORT:-8000}"
