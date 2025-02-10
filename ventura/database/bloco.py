# python manage.py shell

from ventura.models import Bloco  # Importe o modelo

# Lista de blocos a serem inseridos
blocos = [
    "Torre 1 - Fortuna",
    "Torre 2 - Conquista",
    "Torre 3 - Liberdade"
]

# Inserindo os blocos no banco de dados
for nome in blocos:
    Bloco.objects.get_or_create(nome=nome)

print("Blocos inseridos com sucesso!")
