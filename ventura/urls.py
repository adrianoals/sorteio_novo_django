from django.urls import path
from ventura.views import ventura_aleatorio, excel_ventura, zerar_ventura, qrcode_ventura, ventura_presenca, ventura_filtrar, ventura_s_apartamento, ventura_final

urlpatterns = [
        path('ventura-aleatorio', ventura_aleatorio, name='ventura_aleatorio'), 
        path('ventura-excel/', excel_ventura, name='excel_ventura'),
        path('ventura-zerar/', zerar_ventura, name='zerar_ventura'),
        path('ventura-qrcode/', qrcode_ventura, name='qrcode_ventura'), 
        path('ventura-presenca/', ventura_presenca, name='ventura_presenca'), 
        path('ventura-filtrar/', ventura_filtrar, name='ventura_filtrar'), 
        path('ventura-s-apartamento/', ventura_s_apartamento, name='ventura_s_apartamento'), 
        path('ventura_final/', ventura_final, name='ventura_final'), 
        
]