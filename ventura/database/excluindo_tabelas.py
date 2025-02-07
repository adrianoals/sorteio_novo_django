import os
from django.core.management import call_command
from django.db import connection

app_name = "ventura"

# 1. Exclui as tabelas do app 'ventura' do banco de dados (removendo CASCADE)
with connection.cursor() as cursor:
    cursor.execute("DROP TABLE IF EXISTS ventura_sorteio;")
    cursor.execute("DROP TABLE IF EXISTS ventura_apartamento;")
    cursor.execute("DROP TABLE IF EXISTS ventura_vaga;")
    cursor.execute("DROP TABLE IF EXISTS ventura_bloco;")

print("✅ Todas as tabelas do app 'ventura' foram excluídas!")

# 2. Exclui todas as migrações do app 'ventura', exceto __init__.py
migrations_path = os.path.join("ventura", "migrations")
if os.path.exists(migrations_path):
    for file in os.listdir(migrations_path):
        if file.endswith(".py") and file != "__init__.py":
            os.remove(os.path.join(migrations_path, file))
    print("✅ Todas as migrações do app 'ventura' foram excluídas!")
