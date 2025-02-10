from ventura.models import Bloco, Vaga

# Buscar o bloco "Torre 3 - Liberdade"
bloco = Bloco.objects.get(nome="Torre 3 - Liberdade")

# Listas de vagas por subsolo
vagas_subsolo_1 = [
    "1", "2", "3", "4", "5", "6", "7", "8", "10", "11", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", 
    "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "45", "46", "47", "48", "49", "50", "51", "52", "DF1"
]

vagas_subsolo_2 = [
    "136", "137", "138", "139", "140", "141", "142", "143", "144", "145", "146", "147", "148", "149", "150", "151", 
    "152", "153", "154", "155", "156", "157", "158", "159", "160", "161", "162", "173", "174", "175", "176", "177", 
    "178", "179", "180"
]

vagas_subsolo_3 = [
    "256", "257", "258", "259", "260", "261", "262", "263", "264", "265", "266", "267", "268", "269", "270", "271", 
    "272", "273", "274", "275", "276", "277", "278", "279", "280", "281", "282", "292", "293", "294", "295", "296", 
    "297", "298", "299", "300", "301", "302", "329", "330", "341", "342"
]

# Função para criar ou atualizar as vagas com o subsolo correto
def criar_vagas(vagas, subsolo):
    for vaga in vagas:
        Vaga.objects.get_or_create(vaga=vaga, bloco=bloco, defaults={"subsolo": subsolo})

# Criando as vagas nos respectivos subsolos
criar_vagas(vagas_subsolo_1, "1º Subsolo")
criar_vagas(vagas_subsolo_2, "2º Subsolo")
criar_vagas(vagas_subsolo_3, "3º Subsolo")

print("Vagas da Torre 3 - Liberdade inseridas com sucesso!")
