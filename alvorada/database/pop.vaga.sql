from alvorada.models import Vaga

# Definição das vagas conforme configuração
vagas = [
    # Térreo
    ('00', 'Térreo', 'Simples'),
    ('01', 'Térreo', 'Simples'),
    ('02', 'Térreo', 'Simples'),
    ('03', 'Térreo', 'Dupla'),
    ('04', 'Térreo', 'Dupla'),

    # Subsolo 1 (todas simples)
    ('05', 'Subsolo 1', 'Simples'),
    ('06', 'Subsolo 1', 'Simples'),
    ('07', 'Subsolo 1', 'Simples'),
    ('08', 'Subsolo 1', 'Simples'),
    ('09', 'Subsolo 1', 'Simples'),
    ('10', 'Subsolo 1', 'Simples'),
    ('11', 'Subsolo 1', 'Simples'),
    ('12', 'Subsolo 1', 'Simples'),
    ('13', 'Subsolo 1', 'Simples'),
    ('14', 'Subsolo 1', 'Simples'),
    ('15', 'Subsolo 1', 'Simples'),
    ('16', 'Subsolo 1', 'Simples'),
    ('17', 'Subsolo 1', 'Simples'),
    ('18', 'Subsolo 1', 'Simples'),
    ('19', 'Subsolo 1', 'Simples'),

    # Subsolo 2
    ('20', 'Subsolo 2', 'Dupla'),
    ('21', 'Subsolo 2', 'Dupla'),
    ('22', 'Subsolo 2', 'Simples'),
    ('23', 'Subsolo 2', 'Simples'),
    ('24', 'Subsolo 2', 'Dupla'),
    ('25', 'Subsolo 2', 'Dupla'),
    ('26', 'Subsolo 2', 'Dupla'),
    ('27', 'Subsolo 2', 'Simples'),
    ('28', 'Subsolo 2', 'Simples'),
    ('29', 'Subsolo 2', 'Dupla'),
    ('30', 'Subsolo 2', 'Simples'),
    ('31', 'Subsolo 2', 'Simples'),
    ('32', 'Subsolo 2', 'Simples'),
]

# Loop de criação
for numero, subsolo, tipo in vagas:
    vaga, created = Vaga.objects.get_or_create(
        numero=numero,
        defaults={'subsolo': subsolo, 'tipo_vaga': tipo}
    )
    tag = "✓ Criada" if created else "→ Já existia"
    print(f"{tag}: Vaga {numero} - {subsolo} ({tipo})")
