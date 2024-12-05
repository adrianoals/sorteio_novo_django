from gran_vitta.models import Vaga

# Lista de vagas para o 1º subsolo
vagas_1ss_simples = [
    'Vaga 01', 'Vaga 02', 'Vaga 03', 'Vaga 04', 'Vaga 05', 'Vaga 07', 'Vaga 08', 'Vaga 09',
    'Vaga 10', 'Vaga 11', 'Vaga 12', 'Vaga 13B', 'Vaga 15', 'Vaga 16', 'Vaga 17', 'Vaga 18' 
]


# Lista de vagas para o 2º e 3º subsolo
vagas_2_3ss_simples = [
    'Vaga 01', 'Vaga 02', 'Vaga 03', 'Vaga 04', 'Vaga 06', 'Vaga 08', 'Vaga 09', 'Vaga 10', 
    'Vaga 11', 'Vaga 12', 'Vaga 13', 'Vaga 16', 'Vaga 17', 'Vaga 18', 'Vaga 19', 'Vaga 20'
]

vagas_2_3ss_duplas = [
    ('Vaga 05', 'Vaga 07'),
    ('Vaga 14', 'Vaga 15')
]

# Lista de vagas para o 4º subsolo
vagas_4ss_simples = [
    'Vaga 11', 'Vaga 12', 'Vaga 13', 'Vaga 14', 'Vaga 15', 'Vaga 16', 'Vaga 17',
    'Vaga 18', 'Vaga 21', 'Vaga 22', 'Vaga 23', 'Vaga 24', 'Vaga 25'
]
vagas_4ss_duplas = [
    ('Vaga 01', 'Vaga 02'),
    ('Vaga 03', 'Vaga 04'),
    ('Vaga 05', 'Vaga 06'),
    ('Vaga 07', 'Vaga 08'),
    ('Vaga 09', 'Vaga 10'),
    ('Vaga 19', 'Vaga 20')
]

# Lista de vagas para o térreo, com PNE
vagas_terreo_simples = [
    'Vaga 01', 'Vaga 03', 'Vaga 04 PNE', 'Vaga 05', 'Vaga 06', 'Vaga 07', 'Vaga 08', 'Vaga 09', 'Vaga 10'
]

# Função para criar vagas
def criar_vagas(vagas_simples, vagas_duplas, subsolo):
    # Criar vagas simples
    for numero in vagas_simples:
        is_pne = 'PNE' in numero  # Define is_pne como True se "PNE" estiver no nome da vaga
        numero = numero.replace(' PNE', '')  # Remove "PNE" do número da vaga
        Vaga.objects.create(
            numero=numero,
            subsolo=subsolo,
            tipo_vaga='Simples',
            is_pne=is_pne
        )
    # Criar vagas duplas
    for vaga1, vaga2 in vagas_duplas:
        dupla = f"Dupla ({vaga1}, {vaga2})"
        Vaga.objects.create(
            numero=dupla,
            subsolo=subsolo,
            tipo_vaga='Dupla'
        )

# Criando as vagas do 1º subsolo
criar_vagas(vagas_1ss_simples, vagas_1ss_duplas, '1º Subsolo')

# Criando as vagas do 2º e 3º subsolo (mesmas vagas para ambos)
criar_vagas(vagas_2_3ss_simples, vagas_2_3ss_duplas, '2º Subsolo')
criar_vagas(vagas_2_3ss_simples, vagas_2_3ss_duplas, '3º Subsolo')

# Criando as vagas do 4º subsolo
criar_vagas(vagas_4ss_simples, vagas_4ss_duplas, '4º Subsolo')

# Criando as vagas do térreo
criar_vagas(vagas_terreo_simples, [], 'Térreo')

print("Vagas populadas com sucesso!")
