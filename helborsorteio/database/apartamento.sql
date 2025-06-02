from helborsorteio.models import Apartamento

# Definição dos apartamentos conforme configuração
apartamentos = [
    # Torre 1
    ('01', '1'), ('02', '1'), ('03', '1'), ('04', '1'), ('11', '1'), ('12', '1'), ('13', '1'), ('14', '1'),
    ('21', '1'), ('22', '1'), ('23', '1'), ('24', '1'), ('31', '1'), ('32', '1'), ('33', '1'), ('34', '1'),
    ('41', '1'), ('42', '1'), ('43', '1'), ('44', '1'), ('51', '1'), ('52', '1'), ('53', '1'), ('54', '1'),

    # Torre 2
    ('01', '2'), ('02', '2'), ('03', '2'), ('04', '2'), ('11', '2'), ('12', '2'), ('13', '2'), ('14', '2'),
    ('21', '2'), ('22', '2'), ('23', '2'), ('24', '2'), ('31', '2'), ('32', '2'), ('33', '2'), ('34', '2'),
    ('41', '2'), ('42', '2'), ('43', '2'), ('44', '2'), ('51', '2'), ('52', '2'), ('53', '2'), ('54', '2'),

]

# Loop de criação
for numero, torre in apartamentos:
    try:
        apartamento = Apartamento.objects.create(numero=numero, torre=torre)
        print(f"✓ {numero} - Torre {torre}")
    except Exception as e:
        print(f"Erro ao criar apartamento {numero}: {str(e)}")
