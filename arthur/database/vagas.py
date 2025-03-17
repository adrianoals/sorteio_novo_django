# python manage.py shell

from arthur.models import Vaga

# Criar vagas de 1 a 100
vagas = [Vaga(vaga=str(i)) for i in range(1, 101)]
Vaga.objects.bulk_create(vagas)

print("100 vagas criadas com sucesso!")
