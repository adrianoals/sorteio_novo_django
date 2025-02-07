# python manage.py shell

# Excluir todos os registros da tabela Sorteio
from ventura.models import Sorteio

Sorteio.objects.all().delete()
print("Todos os registros de Sorteio foram excluídos!")


# Excluir todos os registros da tabela Vaga
from ventura.models import Vaga

Vaga.objects.all().delete()
print("Todos os registros de Vaga foram excluídos!")


# Remover a tabela Vaga manualmente
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DROP TABLE ventura_vaga;")
    print("Tabela Vaga foi excluída com sucesso!")
