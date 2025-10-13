#!/usr/bin/env bash
#curl -LsSf https://astral.sh/uv/install.sh | sh
#source $HOME/.local/bin/env
#make install && psql -a -d "$DATABASE_URL" -f database.sql


set -o errexit  # аварийно выйти при ошибке
set -o nounset  # ошибка, если переменная не определена
set -o pipefail # если команда в пайпе упала — тоже ошибка

echo "==== Render build environment (safe view) ===="
env | grep -E 'RENDER|DATABASE|PORT|PYTHON' || true
echo "============================================="

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make install

echo "Running migrations..."
psql -a -d "$DATABASE_URL" -f database.sql