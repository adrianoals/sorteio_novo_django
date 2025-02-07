# python manage.py shell

from django.db import connection
from ventura.models import Sorteio, Apartamento, Vaga, Bloco

# Exclui os registros de Sorteio primeiro (pois depende de Apartamento e Vaga)
Sorteio.objects.all().delete()
print("Todos os registros da tabela Sorteio foram excluídos.")

# Exclui os registros de Apartamento e Vaga
Apartamento.objects.all().delete()
print("Todos os registros da tabela Apartamento foram excluídos.")

Vaga.objects.all().delete()
print("Todos os registros da tabela Vaga foram excluídos.")

# Exclui os registros de Bloco por último
Bloco.objects.all().delete()
print("Todos os registros da tabela Bloco foram excluídos.")


# Remover as Tabelas do Banco de Dados
with connection.cursor() as cursor:
    cursor.execute("DROP TABLE IF EXISTS ventura_sorteio;")
    cursor.execute("DROP TABLE IF EXISTS ventura_apartamento;")
    cursor.execute("DROP TABLE IF EXISTS ventura_vaga;")
    cursor.execute("DROP TABLE IF EXISTS ventura_bloco;")
    print("Tabelas do app 'ventura' removidas com sucesso!")
