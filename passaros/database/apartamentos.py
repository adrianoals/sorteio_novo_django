from passaros.models import Bloco, Apartamento

# Configuração inicial
blocos = [f"{str(i).zfill(2)}" for i in range(1, 35)]  # Blocos "01" a "34"
unidades = [f"{str(i).zfill(2)}" for i in [1, 2, 3, 4, 11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41, 42, 43, 44]]

# Unidades excluídas
excluidos = {
    "10": ["03"],
    "13": ["01"],
    "23": ["01"],
    "09": ["01"],
    "26": ["03"],
    "27": ["31", "32", "33", "34"],
    "28": ["31", "32", "33", "34"],
    "29": ["31", "32", "33", "34"],
    "30": ["31", "32", "33", "34"],
    "31": ["32", "33", "34"],
    "32": ["32", "34"],
    "33": ["32", "34"],
    "34": ["01", "32", "34"],
    "22": ["03"],
}

# Criar blocos e apartamentos válidos
for bloco_numero in blocos:
    bloco, created = Bloco.objects.get_or_create(numero=bloco_numero)  # Cria o bloco se ainda não existir
    for unidade_numero in unidades:
        if bloco_numero not in excluidos or unidade_numero not in excluidos[bloco_numero]:
            Apartamento.objects.get_or_create(bloco=bloco, numero=unidade_numero)

print("Unidades válidas criadas com sucesso!")
