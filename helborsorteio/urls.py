from django.urls import path
from . import views

urlpatterns = [
    path('helborsorteio-sorteio/', views.helborsorteio_sorteio, name='helborsorteio_sorteio'),
    path('helborsorteio-excel/', views.helborsorteio_excel, name='helborsorteio_excel'),
    path('helborsorteio-qrcode/', views.helborsorteio_qrcode, name='helborsorteio_qrcode'),
    path('helborsorteio-zerar/', views.helborsorteio_zerar, name='helborsorteio_zerar'),
] 