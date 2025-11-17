from django.urls import path
from la_corunha.views import la_corunha_sorteio, la_corunha_excel, la_corunha_qrcode, la_corunha_zerar

urlpatterns = [
    # Rota para iniciar o sorteio
    path('la-corunha-sorteio/', la_corunha_sorteio, name='la_corunha_sorteio'), 
    # Rota para exportar os resultados do sorteio para um arquivo Excel
    path('la-corunha-excel', la_corunha_excel, name='la_corunha_excel'),
    # Rota para gerar o QR Code do sorteio
    path('la-corunha-qrcode', la_corunha_qrcode, name='la_corunha_qrcode'),
    # Rota para zerar o sorteio
    path('la-corunha-zerar/', la_corunha_zerar, name='la_corunha_zerar'),
]

