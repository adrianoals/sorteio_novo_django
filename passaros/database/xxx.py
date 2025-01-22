import pandas as pd
from passaros.models import Apartamento, Vaga

# Exportar Apartamentos
apartamentos = Apartamento.objects.all()
apartamentos_data = [
    {
        "Bloco": apartamento.bloco.numero,
        "Número do Apartamento": apartamento.numero,
        "Adaptado PNE": "Sim" if apartamento.is_pne else "Não",
    }
    for apartamento in apartamentos
]
apartamentos_df = pd.DataFrame(apartamentos_data)
apartamentos_df.to_excel("apartamentos.xlsx", index=False)

print("Arquivo 'apartamentos.xlsx' gerado com sucesso!")

# Exportar Vagas
vagas = Vaga.objects.all()
vagas_data = [
    {
        "Bloco": vaga.bloco.numero if vaga.bloco else "Sem Bloco",
        "Número da Vaga": vaga.numero,
        "Reservada para PNE": "Sim" if vaga.is_pne else "Não",
    }
    for vaga in vagas
]
vagas_df = pd.DataFrame(vagas_data)
vagas_df.to_excel("vagas.xlsx", index=False)

print("Arquivo 'vagas.xlsx' gerado com sucesso!")
