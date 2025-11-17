from la_corunha.models import Vaga

# Lista das vagas com seus respectivos tipos
vagas = [
    ('M01', 'Moto'),
    ('M02', 'Moto'),
    ('M03', 'Moto'),
    ('M04', 'Moto'),
    ('M05', 'Moto'),
    ('M06', 'Moto'),
    ('M07', 'Moto'),
    ('M08', 'Moto'),
    ('M09', 'Moto'),
    ('5', 'Carro'),
    ('6', 'Carro'),
    ('7', 'Carro'),
    ('8', 'Carro'),
    ('9', 'Moto'),
    ('10', 'Moto'),
    ('11', 'Carro'),
    ('12', 'Carro'),
    ('13', 'Carro'),
    ('14', 'Carro'),
    ('15', 'Moto'),
    ('16', 'Moto'),
    ('17', 'Carro'),
    ('18', 'Carro'),
    ('19', 'Carro'),
    ('20', 'Carro'),
    ('21', 'Moto'),
    ('22', 'Moto'),
    ('23', 'Carro'),
    ('24', 'Carro'),
]

# Verificar se já existem vagas antes de criar
if Vaga.objects.exists():
    print("⚠️ Já existem vagas cadastradas. Use o Django Admin para gerenciar ou delete todas antes de executar este script.")
else:
    # Criar as vagas
    for numero, tipo_vaga in vagas:
        Vaga.objects.create(
            numero=numero,
            tipo_vaga=tipo_vaga
        )
        print(f"✅ Vaga {numero} criada como tipo {tipo_vaga}")

    print(f"\n✅ Total de {len(vagas)} vagas criadas com sucesso!")
    print(f"   - {sum(1 for _, tipo in vagas if tipo == 'Carro')} vagas de Carro")
    print(f"   - {sum(1 for _, tipo in vagas if tipo == 'Moto')} vagas de Moto")
