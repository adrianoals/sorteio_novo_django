#!/bin/sh

echo "Aguardando banco de dados Supabase ficar disponível..."

nc -z -v -w30 "$DB_HOST" "$DB_PORT"
if [ $? -eq 0 ]; then
  echo "Banco disponível"
else
  echo "Não foi possível conectar no banco ($DB_HOST:$DB_PORT)"
  exit 1
fi

echo "Executando migrate..."
python manage.py migrate --noinput

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

exec "$@"
