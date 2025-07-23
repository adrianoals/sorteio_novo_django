import pandas as pd
from django.core.management.base import BaseCommand
from fatto_passion.models import Apartamento

def export_apartamentos_to_excel():
    """Exporta lista de apartamentos para Excel"""
    
    # Busca todos os apartamentos ordenados
    apartamentos = Apartamento.objects.all().order_by('bloco', 'numero')
    
    # Cria lista de dados
    dados = []
    for apt in apartamentos:
        dados.append({
            'ID': apt.id,
            'Número': apt.numero,
            'Bloco': apt.bloco,
            'PNE': 'Sim' if apt.pne else 'Não',
            'Vaga Coberta': 'Sim' if apt.vaga_coberta else 'Não',
            'Vaga Dupla': 'Sim' if apt.vaga_dupla else 'Não'
        })
    
    # Cria DataFrame
    df = pd.DataFrame(dados)
    
    # Nome do arquivo
    filename = 'apartamentos_fatto_passion.xlsx'
    
    # Salva no Excel
    df.to_excel(filename, index=False, sheet_name='Apartamentos')
    
    print(f"✅ Arquivo '{filename}' criado com sucesso!")
    print(f"📊 Total de apartamentos exportados: {len(dados)}")
    print(f"📋 Colunas: {list(df.columns)}")
    
    # Mostra algumas estatísticas
    print(f"\n📈 Estatísticas:")
    print(f"   - Blocos: {df['Bloco'].nunique()}")
    print(f"   - Apartamentos PNE: {len(df[df['PNE'] == 'Sim'])}")
    print(f"   - Apartamentos com vaga coberta: {len(df[df['Vaga Coberta'] == 'Sim'])}")
    print(f"   - Apartamentos com vaga dupla: {len(df[df['Vaga Dupla'] == 'Sim'])}")
    
    return filename

if __name__ == "__main__":
    # Para executar diretamente no Django shell
    export_apartamentos_to_excel() 