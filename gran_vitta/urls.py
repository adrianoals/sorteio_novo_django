from django.urls import path
from gran_vitta.views import gran_vitta_sorteio, gran_vitta_excel, gran_vitta_qrcode, gran_vitta_zerar

urlpatterns = [
        # Rota para iniciar o sorteio
        path('gran-vitta-sorteio/', gran_vitta_sorteio, name='gran_vitta_sorteio'), 
        # Rota para exportar os resultados do sorteio para um arquivo Excel
        path('gran-vitta-excel', gran_vitta_excel, name='gran_vitta_excel'),

        # Rota para gerar o QR Code do sorteio
        path('gran-vitta-qrcode', gran_vitta_qrcode, name='gran_vitta_qrcode'),
        
        # Rota para zerar o sorteio
        path('gran-vitta-zerar/', gran_vitta_zerar, name='gran_vitta_zerar'),

]