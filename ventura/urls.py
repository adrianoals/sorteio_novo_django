from django.urls import path
from ventura.views import ventura_aleatorio, excel_ventura, zerar_ventura, qrcode_ventura, ventura_presenca, ventura_filtrar, ventura_s_apartamento, ventura_final, unique_qrcode

urlpatterns = [
        path('unique-aleatorio', ventura_aleatorio, name='ventura_aleatorio'), 
        path('unique-excel/', excel_ventura, name='excel_ventura'),
        path('unique-zerar/', zerar_ventura, name='zerar_ventura'),
        path('ventura-qrcode/', qrcode_ventura, name='qrcode_ventura'), 
        path('unique-presenca/', ventura_presenca, name='ventura_presenca'), 
        path('unique-filtrar/', ventura_filtrar, name='ventura_filtrar'), 
        path('unique-s-apartamento/', ventura_s_apartamento, name='ventura_s_apartamento'), 
        path('unique_final/', ventura_final, name='ventura_final'), 
        path('unique-qrcode/', unique_qrcode, name='unique_qrcode'), 
        
]