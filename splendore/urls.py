from django.urls import path
from . import views

urlpatterns = [
    path('sorteio/', views.splendore_sorteio, name='splendore_sorteio'),
    path('excel/', views.splendore_excel, name='splendore_excel'),
    path('qrcode/', views.splendore_qrcode, name='splendore_qrcode'),
    path('zerar/', views.splendore_zerar, name='splendore_zerar'),
] 