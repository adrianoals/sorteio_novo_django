from ventura.models import Bloco, Vaga

# Buscar o bloco "Torre 2 - Conquista"
bloco = Bloco.objects.get(nome="Torre 2 - Conquista")

# Listas de vagas por subsolo
vagas_subsolo_1 = [
    "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "61", "62", "63", "64", "65", "66", "67", 
    "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "81", "82", "83", "84", "85", "86", "87", "DF2"
]

vagas_subsolo_2 = [
    "12", "13", "163", "164", "165", "166", "167", "168", "169", "170", "171", "172", "184", "185", "186", "188", 
    "189", "190", "191", "192", "193", "194", "195", "196", "197", "198", "199", "200", "201", "203", "204", "205", 
    "206", "207", "208", "209", "210", "211", "212"
]

vagas_subsolo_3 = [
    "283", "284", "285", "286", "287", "288", "289", "311", "312", "313", "314", "315", "316", "317", "318", "319", 
    "320", "321", "322", "323", "324", "325", "326", "331", "332", "333", "334", "335", "336", "337", "338", "343", 
    "344", "345", "346", "347", "348", "349"
]

# Função para criar ou atualizar as vagas com o subsolo correto
def criar_vagas(vagas, subsolo):
    for vaga in vagas:
        Vaga.objects.get_or_create(vaga=vaga, bloco=bloco, defaults={"subsolo": subsolo})

# Criando as vagas nos respectivos subsolos
criar_vagas(vagas_subsolo_1, "1º Subsolo")
criar_vagas(vagas_subsolo_2, "2º Subsolo")
criar_vagas(vagas_subsolo_3, "3º Subsolo")

print("Vagas da Torre 2 - Conquista inseridas com sucesso!")
