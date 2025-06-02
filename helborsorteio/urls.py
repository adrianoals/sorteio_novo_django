from django.urls import path
from . import views

urlpatterns = [
    path('helbor-sorteio/', views.helborsorteio_sorteio, name='helborsorteio_sorteio'),
    path('helbor-excel/', views.helborsorteio_excel, name='helborsorteio_excel'),
    path('helbor-qrcode/', views.helborsorteio_qrcode, name='helborsorteio_qrcode'),
    path('helbor-zerar/', views.helborsorteio_zerar, name='helborsorteio_zerar'),
] 