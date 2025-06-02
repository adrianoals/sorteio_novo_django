from django.urls import path
from . import views

urlpatterns = [
    path('helbor-sorteio/', views.helborsorteio_sorteio, name='helbor_sorteio'),
    path('helbor-excel/', views.helborsorteio_excel, name='helbor_excel'),
    path('helbor-qrcode/', views.helborsorteio_qrcode, name='helbor_qrcode'),
    path('helbor-zerar/', views.helborsorteio_zerar, name='helbor_zerar'),
] 