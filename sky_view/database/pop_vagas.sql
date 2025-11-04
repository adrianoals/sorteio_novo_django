from sky_view.models import Vaga

# ============================================
# 1º SUBSOLO
# ============================================
# 14 vagas simples + 3 vagas duplas = 17 vagas para sortear
# NOTA: Cada dupla conta como 1 vaga para sorteio (mas são criadas com tipo_vaga='Dupla' no modelo)

vagas_1ss_simples = [
    'Vaga 01', 'Vaga 02', 'Vaga 03', 'Vaga 04', 'Vaga 05', 'Vaga 07', 'Vaga 08', 'Vaga 09',
    'Vaga 10', 'Vaga 11', 'Vaga 12', 'Vaga 13B', 'Vaga 17', 'Vaga 18'
]
vagas_1ss_duplas = [
    ('Vaga 06', 'Vaga 19'),  # Dupla 1
    ('Vaga 13A', 'Vaga 14'),  # Dupla 2
    ('Vaga 15', 'Vaga 16')    # Dupla 3
]

# Criar vagas simples do 1º subsolo
for numero in vagas_1ss_simples:
    is_pne = 'PNE' in numero
    numero_limpo = numero.replace(' PNE', '').replace(' Carga e Descarga', '')
    if not Vaga.objects.filter(numero=numero_limpo, subsolo='1º Subsolo').exists():
        Vaga.objects.create(numero=numero_limpo, subsolo='1º Subsolo', tipo_vaga='Simples', is_pne=is_pne)

# Criar vagas duplas do 1º subsolo
print(f"\nCriando {len(vagas_1ss_duplas)} duplas do 1º subsolo...")
for vaga1, vaga2 in vagas_1ss_duplas:
    dupla = f"Dupla ({vaga1}, {vaga2})"
    print(f"  Tentando criar: {dupla}")
    if not Vaga.objects.filter(numero=dupla, subsolo='1º Subsolo').exists():
        try:
            vaga_dupla = Vaga.objects.create(numero=dupla, subsolo='1º Subsolo', tipo_vaga='Dupla', is_pne=False)
            print(f"  ✅ Dupla criada com sucesso: {dupla}")
        except Exception as e:
            print(f"  ❌ Erro ao criar dupla {dupla}: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"  ⚠️ Dupla já existe: {dupla}")

print(f"1º Subsolo criado: {Vaga.objects.filter(subsolo='1º Subsolo').count()} vagas")
print(f"  - Simples: {Vaga.objects.filter(subsolo='1º Subsolo', tipo_vaga='Simples').count()}")
print(f"  - Duplas: {Vaga.objects.filter(subsolo='1º Subsolo', tipo_vaga='Dupla').count()}")


# ============================================
# 2º SUBSOLO
# ============================================
# 14 vagas simples + 3 vagas duplas = 17 vagas para sortear

vagas_2ss_simples = [
    'Vaga 01', 'Vaga 02', 'Vaga 03', 'Vaga 04', 'Vaga 06', 'Vaga 08', 'Vaga 09', 'Vaga 10', 
    'Vaga 11', 'Vaga 12', 'Vaga 13', 'Vaga 18', 'Vaga 19', 'Vaga 20'
]
vagas_2ss_duplas = [
    ('Vaga 05', 'Vaga 07'),   # Dupla 1
    ('Vaga 14', 'Vaga 15'),   # Dupla 2
    ('Vaga 16', 'Vaga 17')    # Dupla 3
]

# Criar vagas simples do 2º subsolo
for numero in vagas_2ss_simples:
    is_pne = 'PNE' in numero
    numero_limpo = numero.replace(' PNE', '').replace(' Carga e Descarga', '')
    if not Vaga.objects.filter(numero=numero_limpo, subsolo='2º Subsolo').exists():
        Vaga.objects.create(numero=numero_limpo, subsolo='2º Subsolo', tipo_vaga='Simples', is_pne=is_pne)

# Criar vagas duplas do 2º subsolo
print(f"\nCriando {len(vagas_2ss_duplas)} duplas do 2º subsolo...")
for vaga1, vaga2 in vagas_2ss_duplas:
    dupla = f"Dupla ({vaga1}, {vaga2})"
    print(f"  Tentando criar: {dupla}")
    if not Vaga.objects.filter(numero=dupla, subsolo='2º Subsolo').exists():
        try:
            vaga_dupla = Vaga.objects.create(numero=dupla, subsolo='2º Subsolo', tipo_vaga='Dupla', is_pne=False)
            print(f"  ✅ Dupla criada com sucesso: {dupla}")
        except Exception as e:
            print(f"  ❌ Erro ao criar dupla {dupla}: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"  ⚠️ Dupla já existe: {dupla}")

print(f"2º Subsolo criado: {Vaga.objects.filter(subsolo='2º Subsolo').count()} vagas")
print(f"  - Simples: {Vaga.objects.filter(subsolo='2º Subsolo', tipo_vaga='Simples').count()}")
print(f"  - Duplas: {Vaga.objects.filter(subsolo='2º Subsolo', tipo_vaga='Dupla').count()}")


# ============================================
# 3º SUBSOLO
# ============================================
# 16 vagas simples + 2 vagas duplas = 18 vagas para sortear

vagas_3ss_simples = [
    'Vaga 01', 'Vaga 02', 'Vaga 03', 'Vaga 04', 'Vaga 06', 'Vaga 08', 'Vaga 09', 'Vaga 10', 
    'Vaga 11', 'Vaga 12', 'Vaga 13', 'Vaga 16', 'Vaga 17', 'Vaga 18', 'Vaga 19', 'Vaga 20'
]
vagas_3ss_duplas = [
    ('Vaga 05', 'Vaga 07'),   # Dupla 1
    ('Vaga 14', 'Vaga 15')    # Dupla 2
]

# Criar vagas simples do 3º subsolo
for numero in vagas_3ss_simples:
    is_pne = 'PNE' in numero
    numero_limpo = numero.replace(' PNE', '').replace(' Carga e Descarga', '')
    if not Vaga.objects.filter(numero=numero_limpo, subsolo='3º Subsolo').exists():
        Vaga.objects.create(numero=numero_limpo, subsolo='3º Subsolo', tipo_vaga='Simples', is_pne=is_pne)

# Criar vagas duplas do 3º subsolo
print(f"\nCriando {len(vagas_3ss_duplas)} duplas do 3º subsolo...")
for vaga1, vaga2 in vagas_3ss_duplas:
    dupla = f"Dupla ({vaga1}, {vaga2})"
    print(f"  Tentando criar: {dupla}")
    if not Vaga.objects.filter(numero=dupla, subsolo='3º Subsolo').exists():
        try:
            vaga_dupla = Vaga.objects.create(numero=dupla, subsolo='3º Subsolo', tipo_vaga='Dupla', is_pne=False)
            print(f"  ✅ Dupla criada com sucesso: {dupla}")
        except Exception as e:
            print(f"  ❌ Erro ao criar dupla {dupla}: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"  ⚠️ Dupla já existe: {dupla}")

print(f"3º Subsolo criado: {Vaga.objects.filter(subsolo='3º Subsolo').count()} vagas")
print(f"  - Simples: {Vaga.objects.filter(subsolo='3º Subsolo', tipo_vaga='Simples').count()}")
print(f"  - Duplas: {Vaga.objects.filter(subsolo='3º Subsolo', tipo_vaga='Dupla').count()}")


# ============================================
# 4º SUBSOLO
# ============================================
# 13 vagas simples + 6 vagas duplas = 19 vagas para sortear

vagas_4ss_simples = [
    'Vaga 11', 'Vaga 12', 'Vaga 13', 'Vaga 14', 'Vaga 15', 'Vaga 16', 'Vaga 17',
    'Vaga 18', 'Vaga 21', 'Vaga 22', 'Vaga 23', 'Vaga 24', 'Vaga 25'
]
vagas_4ss_duplas = [
    ('Vaga 01', 'Vaga 02'),   # Dupla 1
    ('Vaga 03', 'Vaga 04'),   # Dupla 2
    ('Vaga 05', 'Vaga 06'),   # Dupla 3
    ('Vaga 07', 'Vaga 08'),   # Dupla 4
    ('Vaga 09', 'Vaga 10'),   # Dupla 5
    ('Vaga 19', 'Vaga 20')    # Dupla 6
]

# Criar vagas simples do 4º subsolo
for numero in vagas_4ss_simples:
    is_pne = 'PNE' in numero
    numero_limpo = numero.replace(' PNE', '').replace(' Carga e Descarga', '')
    if not Vaga.objects.filter(numero=numero_limpo, subsolo='4º Subsolo').exists():
        Vaga.objects.create(numero=numero_limpo, subsolo='4º Subsolo', tipo_vaga='Simples', is_pne=is_pne)

# Criar vagas duplas do 4º subsolo
print(f"\nCriando {len(vagas_4ss_duplas)} duplas do 4º subsolo...")
for vaga1, vaga2 in vagas_4ss_duplas:
    dupla = f"Dupla ({vaga1}, {vaga2})"
    print(f"  Tentando criar: {dupla}")
    if not Vaga.objects.filter(numero=dupla, subsolo='4º Subsolo').exists():
        try:
            vaga_dupla = Vaga.objects.create(numero=dupla, subsolo='4º Subsolo', tipo_vaga='Dupla', is_pne=False)
            print(f"  ✅ Dupla criada com sucesso: {dupla}")
        except Exception as e:
            print(f"  ❌ Erro ao criar dupla {dupla}: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"  ⚠️ Dupla já existe: {dupla}")

print(f"4º Subsolo criado: {Vaga.objects.filter(subsolo='4º Subsolo').count()} vagas")
print(f"  - Simples: {Vaga.objects.filter(subsolo='4º Subsolo', tipo_vaga='Simples').count()}")
print(f"  - Duplas: {Vaga.objects.filter(subsolo='4º Subsolo', tipo_vaga='Dupla').count()}")


# ============================================
# TÉRREO
# ============================================
# 8 vagas simples + 1 vaga PNE + 1 vaga carga e descarga = 10 vagas

vagas_terreo_simples = ['Vaga 01', 'Vaga 03', 'Vaga 05', 'Vaga 06', 'Vaga 07', 'Vaga 08', 'Vaga 09', 'Vaga 10']
vagas_terreo_pne = ['Vaga 04 PNE']
vagas_terreo_especial = ['Vaga 02 Carga e Descarga']

# Criar vagas simples do térreo
for numero in vagas_terreo_simples:
    if not Vaga.objects.filter(numero=numero, subsolo='Térreo').exists():
        Vaga.objects.create(numero=numero, subsolo='Térreo', tipo_vaga='Simples', is_pne=False)

# Criar vaga PNE do térreo
for numero in vagas_terreo_pne:
    numero_limpo = numero.replace(' PNE', '')
    if not Vaga.objects.filter(numero=numero_limpo, subsolo='Térreo').exists():
        Vaga.objects.create(numero=numero_limpo, subsolo='Térreo', tipo_vaga='Simples', is_pne=True)

# Criar vaga carga e descarga do térreo
for numero in vagas_terreo_especial:
    numero_limpo = numero.replace(' Carga e Descarga', '')
    if not Vaga.objects.filter(numero=numero_limpo, subsolo='Térreo').exists():
        Vaga.objects.create(numero=numero_limpo, subsolo='Térreo', tipo_vaga='Simples', is_pne=False)

print(f"Térreo criado: {Vaga.objects.filter(subsolo='Térreo').count()} vagas")
print(f"  - Simples: {Vaga.objects.filter(subsolo='Térreo', tipo_vaga='Simples').count()}")
print(f"  - Duplas: {Vaga.objects.filter(subsolo='Térreo', tipo_vaga='Dupla').count()}")


# ============================================
# RESUMO FINAL
# ============================================
print(f"\n=== RESUMO TOTAL ===")
print(f"Total de vagas criadas: {Vaga.objects.count()}")
for subsolo in ['1º Subsolo', '2º Subsolo', '3º Subsolo', '4º Subsolo', 'Térreo']:
    simples = Vaga.objects.filter(subsolo=subsolo, tipo_vaga='Simples').count()
    duplas = Vaga.objects.filter(subsolo=subsolo, tipo_vaga='Dupla').count()
    total_vagas_sorteio = simples + duplas
    print(f"{subsolo}: {simples} simples + {duplas} duplas = {total_vagas_sorteio} vagas para sortear")
