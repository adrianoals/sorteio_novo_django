from django.urls import path
from passaros.views import passaros_sorteio, passaros_excel, passaros_qrcode, passaros_zerar

urlpatterns = [
        # Rota para iniciar o sorteio
        path('passaros-sorteio/', passaros_sorteio, name='passaros_sorteio'), 
        # Rota para exportar os resultados do sorteio para um arquivo Excel
        path('passaros-excel', passaros_excel, name='passaros_excel'),

        # Rota para gerar o QR Code do sorteio
        path('passaros-qrcode', passaros_qrcode, name='passaros_qrcode'),
        
        # Rota para zerar o sorteio
        path('passaros-zerar/', passaros_zerar, name='passaros_zerar'),
]

