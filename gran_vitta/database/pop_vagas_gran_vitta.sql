from gran_vitta.models import Vaga

# Lista de distribuição
vaga_data = [
    ('Térreo', range(1, 21)),  # 20 vagas
    ('1º Subsolo', range(21, 61)),  # 40 vagas
    ('2º Subsolo', range(61, 111)),  # 50 vagas
    ('3º Subsolo', range(111, 161)),  # 50 vagas
    ('4º Subsolo', range(161, 201)),  # 49 vagas
]

# Criar vagas
for subsolo, numeros in vaga_data:
    for numero in numeros:
        Vaga.objects.create(
            numero=f"Vaga {numero:03}",  # Ex: "Vaga 001"
            subsolo=subsolo,
            is_pne=False  # PNE será configurado depois
        )

print("Vagas criadas com sucesso!")
