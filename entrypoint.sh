#!/bin/sh

# Aguarda o PostgreSQL estar disponível
if [ "$DATABASE" = "postgres" ]; then
    echo "Aguardando o Postgres..."
    while ! nc -z db 5432; do
      sleep 0.1
    done
    echo "Postgres pronto!"
fi

# Aplica migrações
python manage.py migrate --noinput

# Executa o comando padrão
exec "$@"