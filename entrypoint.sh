#!/bin/sh
set -e

echo "[entrypoint] Esperando Supabase em $DB_HOST:$DB_PORT…"
i=0
until nc -z "$DB_HOST" "$DB_PORT"; do
  i=$((i+1))
  [ "$i" -ge 15 ] && { echo "[entrypoint] Banco indisponível"; exit 1; }
  sleep 2
done
echo "[entrypoint] Banco disponível ✔️"

echo "[entrypoint] Rodando migrations…"
python manage.py migrate --noinput

echo "[entrypoint] Coletando arquivos estáticos…"
python manage.py collectstatic --noinput

echo "[entrypoint] Iniciando Gunicorn → $*"
exec "$@"
