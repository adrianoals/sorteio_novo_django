from ventura.models import Vaga

# Listas de vagas duplas por subsolo
vagas_duplas_subsolo1 = [
    ("53", "58"),
    ("54", "59"),
    ("55", "60")
]

vagas_duplas_subsolo2 = [
    ("129", "130"),
    ("181", "217"),
    ("182", "218"),
    ("183", "219"),
    ("249", "250")
]

vagas_duplas_subsolo3 = [
    ("303", "308"),
    ("304", "309"),
    ("305", "310"),
    ("379", "380")
]

# Função para criar as vagas duplas como uma única vaga
def criar_vagas_duplas(vagas, subsolo):
    for vaga1, vaga2 in vagas:
        vaga_dupla = f"{vaga1}-{vaga2}"  # Nome único para a vaga dupla
        Vaga.objects.get_or_create(vaga=vaga_dupla, bloco=None, defaults={"subsolo": subsolo})

# Criando as vagas duplas nos respectivos subsolos
criar_vagas_duplas(vagas_duplas_subsolo1, "1º Subsolo")
criar_vagas_duplas(vagas_duplas_subsolo2, "2º Subsolo")
criar_vagas_duplas(vagas_duplas_subsolo3, "3º Subsolo")

print("Vagas duplas inseridas como uma única vaga com sucesso!")
