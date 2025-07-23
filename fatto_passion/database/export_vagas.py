import pandas as pd
from django.core.management.base import BaseCommand
from fatto_passion.models import Vaga

def export_vagas_to_excel():
    """Exporta lista de vagas para Excel"""
    
    # Busca todas as vagas ordenadas
    vagas = Vaga.objects.all().order_by('bloco', 'andar', 'numero')
    
    # Cria lista de dados
    dados = []
    for vaga in vagas:
        dados.append({
            'ID': vaga.id,
            'Número': vaga.numero,
            'Bloco': vaga.bloco,
            'Andar': vaga.get_andar_display(),
            'Tamanho': vaga.get_tamanho_display(),
            'PNE': 'Sim' if vaga.pne else 'Não',
            'Vaga Coberta': 'Sim' if vaga.vaga_coberta else 'Não'
        })
    
    # Cria DataFrame
    df = pd.DataFrame(dados)
    
    # Nome do arquivo
    filename = 'vagas_fatto_passion.xlsx'
    
    # Salva no Excel
    df.to_excel(filename, index=False, sheet_name='Vagas')
    
    print(f"✅ Arquivo '{filename}' criado com sucesso!")
    print(f"📊 Total de vagas exportadas: {len(dados)}")
    print(f"📋 Colunas: {list(df.columns)}")
    
    # Mostra algumas estatísticas
    print(f"\n📈 Estatísticas:")
    print(f"   - Blocos: {df['Bloco'].nunique()}")
    print(f"   - Andares: {df['Andar'].nunique()}")
    print(f"   - Tamanhos: {df['Tamanho'].nunique()}")
    print(f"   - Vagas PNE: {len(df[df['PNE'] == 'Sim'])}")
    print(f"   - Vagas cobertas: {len(df[df['Vaga Coberta'] == 'Sim'])}")
    
    # Estatísticas por andar
    print(f"\n🏢 Vagas por andar:")
    andares = df['Andar'].value_counts()
    for andar, count in andares.items():
        print(f"   - {andar}: {count} vagas")
    
    # Estatísticas por tamanho
    print(f"\n📏 Vagas por tamanho:")
    tamanhos = df['Tamanho'].value_counts()
    for tamanho, count in tamanhos.items():
        print(f"   - {tamanho}: {count} vagas")
    
    return filename

if __name__ == "__main__":
    # Para executar diretamente no Django shell
    export_vagas_to_excel() 