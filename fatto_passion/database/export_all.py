import pandas as pd
from django.core.management.base import BaseCommand
from fatto_passion.models import Apartamento, Vaga

def export_all_to_excel():
    """Exporta apartamentos e vagas para Excel em um único arquivo"""
    
    # ===== EXPORTAÇÃO DE APARTAMENTOS =====
    apartamentos = Apartamento.objects.all().order_by('bloco', 'numero')
    
    dados_apt = []
    for apt in apartamentos:
        dados_apt.append({
            'ID': apt.id,
            'Número': apt.numero,
            'Bloco': apt.bloco,
            'PNE': 'Sim' if apt.pne else 'Não',
            'Vaga Coberta': 'Sim' if apt.vaga_coberta else 'Não',
            'Vaga Dupla': 'Sim' if apt.vaga_dupla else 'Não'
        })
    
    df_apt = pd.DataFrame(dados_apt)
    
    # ===== EXPORTAÇÃO DE VAGAS =====
    vagas = Vaga.objects.all().order_by('bloco', 'andar', 'numero')
    
    dados_vagas = []
    for vaga in vagas:
        dados_vagas.append({
            'ID': vaga.id,
            'Número': vaga.numero,
            'Bloco': vaga.bloco,
            'Andar': vaga.get_andar_display(),
            'Tamanho': vaga.get_tamanho_display(),
            'PNE': 'Sim' if vaga.pne else 'Não',
            'Vaga Coberta': 'Sim' if vaga.vaga_coberta else 'Não'
        })
    
    df_vagas = pd.DataFrame(dados_vagas)
    
    # ===== SALVA NO EXCEL =====
    filename = 'fatto_passion_completo.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df_apt.to_excel(writer, sheet_name='Apartamentos', index=False)
        df_vagas.to_excel(writer, sheet_name='Vagas', index=False)
    
    print(f"✅ Arquivo '{filename}' criado com sucesso!")
    print(f"📊 Total de apartamentos: {len(dados_apt)}")
    print(f"📊 Total de vagas: {len(dados_vagas)}")
    
    # ===== ESTATÍSTICAS DOS APARTAMENTOS =====
    print(f"\n🏢 ESTATÍSTICAS DOS APARTAMENTOS:")
    print(f"   - Blocos: {df_apt['Bloco'].nunique()}")
    print(f"   - Apartamentos PNE: {len(df_apt[df_apt['PNE'] == 'Sim'])}")
    print(f"   - Apartamentos com vaga coberta: {len(df_apt[df_apt['Vaga Coberta'] == 'Sim'])}")
    print(f"   - Apartamentos com vaga dupla: {len(df_apt[df_apt['Vaga Dupla'] == 'Sim'])}")
    
    # Estatísticas por bloco
    print(f"\n🏢 Apartamentos por bloco:")
    blocos_apt = df_apt['Bloco'].value_counts()
    for bloco, count in blocos_apt.items():
        print(f"   - {bloco}: {count} apartamentos")
    
    # ===== ESTATÍSTICAS DAS VAGAS =====
    print(f"\n🚗 ESTATÍSTICAS DAS VAGAS:")
    print(f"   - Blocos: {df_vagas['Bloco'].nunique()}")
    print(f"   - Andares: {df_vagas['Andar'].nunique()}")
    print(f"   - Vagas PNE: {len(df_vagas[df_vagas['PNE'] == 'Sim'])}")
    print(f"   - Vagas cobertas: {len(df_vagas[df_vagas['Vaga Coberta'] == 'Sim'])}")
    
    # Estatísticas por andar
    print(f"\n🏢 Vagas por andar:")
    andares = df_vagas['Andar'].value_counts()
    for andar, count in andares.items():
        print(f"   - {andar}: {count} vagas")
    
    # Estatísticas por tamanho
    print(f"\n📏 Vagas por tamanho:")
    tamanhos = df_vagas['Tamanho'].value_counts()
    for tamanho, count in tamanhos.items():
        print(f"   - {tamanho}: {count} vagas")
    
    return filename

if __name__ == "__main__":
    # Para executar diretamente no Django shell
    export_all_to_excel() 