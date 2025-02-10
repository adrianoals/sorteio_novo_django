from ventura.models import Bloco, Vaga

# Buscar o bloco "Torre 1 - Fortuna"
bloco = Bloco.objects.get(nome="Torre 1 - Fortuna")

# Listas de vagas por subsolo
vagas_subsolo_1 = [
    "9", "56", "57", "79", "80", "100", "101", "103", "105", "108", "109", "110", "111", "112", "113", "114", "115", 
    "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "131", "132", "133", 
    "134", "135", "187"
]

vagas_subsolo_2 = [
    "202", "213", "214", "215", "216", "220", "221", "222", "223", "224", "225", "226", "228", "229", "230", "231", 
    "232", "233", "234", "235", "236", "237", "238", "239", "240", "241", "242", "243", "244", "245", "246", "247", 
    "248", "251", "252", "253", "254", "255", "400", "DF3"
]

vagas_subsolo_3 = [
    "290", "291", "306", "307", "327", "328", "339", "340", "350", "351", "352", "353", "354", "355", "356", "357", 
    "358", "359", "360", "361", "362", "363", "364", "365", "366", "367", "368", "369", "370", "371", "372", "373", 
    "374", "375", "376", "377", "378", "381", "382", "383", "384", "385", "399", "DF4"
]

# Função para criar ou atualizar as vagas com o subsolo correto
def criar_vagas(vagas, subsolo):
    for vaga in vagas:
        Vaga.objects.get_or_create(vaga=vaga, bloco=bloco, defaults={"subsolo": subsolo})

# Criando as vagas nos respectivos subsolos
criar_vagas(vagas_subsolo_1, "1º Subsolo")
criar_vagas(vagas_subsolo_2, "2º Subsolo")
criar_vagas(vagas_subsolo_3, "3º Subsolo")

print("Vagas da Torre 1 - Fortuna inseridas com sucesso!")
