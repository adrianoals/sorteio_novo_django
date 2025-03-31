from ventura.models import Bloco, Vaga

# Buscar o bloco "Torre 1 - Fortuna"
bloco = Bloco.objects.get(nome="-")

# Listas de vagas por subsolo
vagas_subsolo_1 = [
     "01-S1", "02-S1", "03-S1", "04-S1", "05-S1", "06-S1", "7 - (PCD) - S1", "10-S1", "11-S1", "12-S1", "13-S1", "14-S1", "15-S1", "16-S1", "17-S1", "18-S1", "19-S1"
]

vagas_subsolo_2 = [
    "06-S2", "07-S2", "08-S2", "09-S2", "10-S2", "11-S2", "13-S2", "14-S2", "15-S2", "16-S2", "17-S2", "18-S2", "19-S2", "20-S2", "21-S2", "22-S2", "23-S2", "24-S2", "25-S2", "26-S2", "27-S2", "28-S2"
]


# Função para criar ou atualizar as vagas com o subsolo correto
def criar_vagas(vagas, subsolo):
    for vaga in vagas:
        Vaga.objects.get_or_create(vaga=vaga, bloco=bloco, defaults={"subsolo": subsolo})


# Criando as vagas nos respectivos subsolos
criar_vagas(vagas_subsolo_1, "1º Subsolo")
criar_vagas(vagas_subsolo_2, "2º Subsolo")


print("Vagas da Torre - Fortuna inseridas com sucesso!")
