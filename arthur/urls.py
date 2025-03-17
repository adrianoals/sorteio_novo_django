from django.urls import path
from arthur.views import arthur_aleatorio, excel_arthur, zerar_arthur, qrcode_arthur, arthur_presenca, arthur_filtrar, arthur_s_apartamento, arthur_final

urlpatterns = [
        path('arthur-aleatorio', arthur_aleatorio, name='arthur_aleatorio'), 
        path('arthur-excel/', excel_arthur, name='excel_arthur'),
        path('arthur-zerar/', zerar_arthur, name='zerar_arthur'),
        path('arthur-qrcode/', qrcode_arthur, name='qrcode_arthur'), 
        path('arthur-presenca/', arthur_presenca, name='arthur_presenca'), 
        path('arthur-filtrar/', arthur_filtrar, name='arthur_filtrar'), 
        path('arthur-s-apartamento/', arthur_s_apartamento, name='arthur_s_apartamento'), 
        path('arthur_final/', arthur_final, name='arthur_final'), 
        
]