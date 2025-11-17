from la_corunha.models import Vaga

# Script para atualizar os campos booleanos is_carro e is_moto nas vagas existentes
# Execute este script no Django shell após criar a migration

vagas = Vaga.objects.all()
atualizadas = 0

for vaga in vagas:
    if vaga.tipo_vaga == 'Carro':
        vaga.is_carro = True
        vaga.is_moto = False
    elif vaga.tipo_vaga == 'Moto':
        vaga.is_carro = False
        vaga.is_moto = True
    
    # Salvar sem chamar save() para evitar loop infinito
    Vaga.objects.filter(id=vaga.id).update(
        is_carro=vaga.is_carro,
        is_moto=vaga.is_moto
    )
    atualizadas += 1
    print(f"✅ Vaga {vaga.numero} atualizada: is_carro={vaga.is_carro}, is_moto={vaga.is_moto}")

print(f"\n✅ Total de {atualizadas} vagas atualizadas com sucesso!")

