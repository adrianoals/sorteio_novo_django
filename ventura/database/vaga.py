from ventura.models import Vaga

# Número total de vagas
total_vagas = 362
# Metade das vagas para cada subsolo
metade_vagas = total_vagas // 2

# Criando as vagas para Subsolo 1
for i in range(1, metade_vagas + 1):
    Vaga.objects.get_or_create(vaga=str(i), subsolo="Subsolo 1")

# Criando as vagas para Subsolo 2
for i in range(metade_vagas + 1, total_vagas + 1):
    Vaga.objects.get_or_create(vaga=str(i), subsolo="Subsolo 2")

print("Vagas criadas com sucesso!")
