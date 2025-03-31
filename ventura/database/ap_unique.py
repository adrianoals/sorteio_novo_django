from ventura.models import Bloco, Apartamento

# Buscar o bloco "Torre 1 - Fortuna"
bloco, created = Bloco.objects.get_or_create(nome="-")

# Lista de apartamentos
apartamentos_t1 = [
    "101", "102", "104", "106", "108", "109", "110", "111", "201", "202", "204", "206", "208", "210", "211", "301", "302", "303", "304", "306", "308", "310", "311", "401", "402", "404", "406", "408", "409", "410", "411", "501", "502", "504", "506", "508", "509", "510", "511"
]

# Criando os apartamentos associados ao bloco
for numero in apartamentos_t1:
    Apartamento.objects.get_or_create(numero_apartamento=numero, bloco=bloco)

print("Apartamentos Torre -  Fortuna inseridos com sucesso!")
