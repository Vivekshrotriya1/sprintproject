#!/usr/bin/env bash
set -e

cd /home/site/wwwroot

if [ -d "/home/site/wwwroot/antenv/lib/python3.10/site-packages" ]; then
  export PYTHONPATH="/home/site/wwwroot/antenv/lib/python3.10/site-packages:${PYTHONPATH}"
fi

if [ -d "/home/site/wwwroot/.python_packages/lib/site-packages" ]; then
  export PYTHONPATH="/home/site/wwwroot/.python_packages/lib/site-packages:${PYTHONPATH}"
fi

export PYTHONPATH="/home/site/wwwroot:/home/site/wwwroot/api:${PYTHONPATH}"

mkdir -p /app
ln -sfn /home/site/wwwroot/models /app/models
ln -sfn /home/site/wwwroot/data /app/data

python -m uvicorn api.app:app --host 0.0.0.0 --port "${PORT:-8000}"
