from la_corunha.models import Apartamento

# Lista dos apartamentos com seus respectivos tipos de vaga
apartamentos = [
    ('1', 'Carro'),
    ('2', 'Carro'),
    ('4', 'Moto'),
    ('5', 'Carro'),
    ('6', 'Carro'),
    ('11', 'Carro'),
    ('12', 'Carro'),
    ('13', 'Moto'),
    ('14', 'Moto'),
    ('15', 'Carro'),
    ('16', 'Carro'),
    ('21', 'Carro'),
    ('22', 'Carro'),
    ('23', 'Moto'),
    ('24', 'Moto'),
    ('25', 'Carro'),
    ('26', 'Carro'),
    ('31', 'Carro'),
    ('32', 'Carro'),
    ('33', 'Moto'),
    ('34', 'Moto'),
    ('35', 'Carro'),
    ('36', 'Carro'),
    ('41', 'Carro'),
    ('42', 'Carro'),
    ('43', 'Moto'),
    ('44', 'Moto'),
    ('45', 'Carro'),
    ('46', 'Carro'),
]

# Verificar se já existem apartamentos antes de criar
if Apartamento.objects.exists():
    print("⚠️ Já existem apartamentos cadastrados. Use o Django Admin para gerenciar ou delete todos antes de executar este script.")
else:
    # Criar os apartamentos
    for numero, tipo_vaga in apartamentos:
        Apartamento.objects.create(
            numero=f"Apartamento {numero}",
            tipo_vaga_direito=tipo_vaga
        )
        print(f"✅ Apartamento {numero} criado com direito a vaga de {tipo_vaga}")

    print(f"\n✅ Total de {len(apartamentos)} apartamentos criados com sucesso!")
    print(f"   - {sum(1 for _, tipo in apartamentos if tipo == 'Carro')} apartamentos com direito a vaga de Carro")
    print(f"   - {sum(1 for _, tipo in apartamentos if tipo == 'Moto')} apartamentos com direito a vaga de Moto")
