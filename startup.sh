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

if ! python -c "import uvicorn" >/dev/null 2>&1; then
  echo "Python packages not found. Installing app dependencies..."
  python -m pip install --upgrade pip
  python -m pip install -r requirements.txt --target="/home/site/wwwroot/.python_packages/lib/site-packages"
  export PYTHONPATH="/home/site/wwwroot/.python_packages/lib/site-packages:${PYTHONPATH}"
fi

mkdir -p /app
ln -sfn /home/site/wwwroot/models /app/models
ln -sfn /home/site/wwwroot/data /app/data

python -m uvicorn api.app:app --host 0.0.0.0 --port "${PORT:-8000}"
