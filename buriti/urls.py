from django.urls import path
from buriti.views import buriti_sorteio, buriti_excel, buriti_qrcode, buriti_zerar

urlpatterns = [
    # Rota para iniciar o sorteio
    path('buriti-sorteio/', buriti_sorteio, name='buriti_sorteio'), 
    # Rota para exportar os resultados do sorteio para um arquivo Excel
    path('buriti-excel', buriti_excel, name='buriti_excel'),
    # Rota para gerar o QR Code do sorteio
    path('buriti-qrcode', buriti_qrcode, name='buriti_qrcode'),
    # Rota para zerar o sorteio
    path('buriti-zerar/', buriti_zerar, name='buriti_zerar'),
]

