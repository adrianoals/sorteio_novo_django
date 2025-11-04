from django.urls import path
from tres_coelhos.views import tres_coelhos_menu, tres_coelhos_sorteio, tres_coelhos_excel, tres_coelhos_qrcode, tres_coelhos_dupla, tres_coelhos_dupla_excel, tres_coelhos_zerar, tres_coelhos_resultado, tres_coelhos_resultado_excel, tres_coelhos_configurar_pne, tres_coelhos_configurar_duplas

urlpatterns = [
        # Rota para o menu principal
        path('tres-coelhos-menu/', tres_coelhos_menu, name='tres_coelhos_menu'),
        # Rota para iniciar o sorteio
        path('tres-coelhos-sorteio/', tres_coelhos_sorteio, name='tres_coelhos_sorteio'), 
        # Rota para exportar os resultados do sorteio para um arquivo Excel
        path('sorteio/excel/', tres_coelhos_excel, name='tres_coelhos_excel'),

        # Rota para gerar o QR Code do sorteio
        path('tres-coelhos-qrcode', tres_coelhos_qrcode, name='tres_coelhos_qrcode'),
        
        # Rota para iniciar o sorteio dupla
        path('tres-coelhos-dupla/', tres_coelhos_dupla, name='tres_coelhos_dupla'), 
        # Rota para exportar os resultados do sorteio para um arquivo Excel
        path('sorteio/dupla/excel/', tres_coelhos_dupla_excel, name='tres_coelhos_dupla_excel'),
        
        # Rota para zerar o sorteio
        path('tres-coelhos-zerar/', tres_coelhos_zerar, name='tres_coelhos_zerar'),

        # Rota para o resultado
        path('tres-coelhos-resultado/', tres_coelhos_resultado, name='tres_coelhos_resultado'),
        # Rota para exportar o resultado completo para Excel
        path('resultado/excel/', tres_coelhos_resultado_excel, name='tres_coelhos_resultado_excel'),
        
        # Rotas para configuração
        path('tres-coelhos-configurar-pne/', tres_coelhos_configurar_pne, name='tres_coelhos_configurar_pne'),
        path('tres-coelhos-configurar-duplas/', tres_coelhos_configurar_duplas, name='tres_coelhos_configurar_duplas'),

]

