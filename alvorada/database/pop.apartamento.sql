from alvorada.models import Apartamento

# Lista dos números de apartamento
apartamentos = [
    '11', '12', '13', '14',
    '21', '22', '23', '24',
    '31', '32', '33', '34',
    '41', '42', '43', '44',
    '51', '52', '53', '54',
    '61', '62', '63', '64',
    '71', '72', '73', '74',
    '81', '82', '83', '84',
]

def populate_apartamentos():
    for apt_num in apartamentos:
        obj, created = Apartamento.objects.get_or_create(
            numero=apt_num,
            defaults={'direito_vaga_dupla': False}
        )
        if created:
            print(f"  • Criado: Apartamento {apt_num}")
        else:
            print(f"  • Já existe: Apartamento {apt_num}")
    print("Processo concluído.")

populate_apartamentos()


