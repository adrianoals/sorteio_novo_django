#!/bin/sh

# Espera o banco (opcional, pode remover se Supabase for confiável)
echo "Aguardando banco de dados Supabase ficar disponível..."

# Testa conexão com o host do Supabase (opcional)
nc -z -v -w30 $DB_HOST $DB_PORT
if [ $? -eq 0 ]; then
  echo "Banco disponível"
else
  echo "Não foi possível conectar no banco ($DB_HOST:$DB_PORT)"
  exit 1
fi

# Roda as migrations
echo "Executando migrate..."
python manage.py migrate --noinput

# Coleta arquivos estáticos (opcional)
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Executa o comando padrão (gunicorn)
exec "$@"
