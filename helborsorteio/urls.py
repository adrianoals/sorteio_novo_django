from django.urls import path
from . import views

urlpatterns = [
    path('helbor-sorteio/', views.helbor_sorteio, name='helbor_sorteio'),
    path('helbor-excel/', views.helbor_excel, name='helbor_excel'),
    path('helbor-qrcode/', views.helbor_qrcode, name='helbor_qrcode'),
    path('helbor-zerar/', views.helbor_zerar, name='helbor_zerar'),
] 