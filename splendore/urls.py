from django.urls import path
from . import views

urlpatterns = [
    path('splendore-sorteio/', views.splendore_sorteio, name='splendore_sorteio'),
    path('splendore-excel/', views.splendore_excel, name='splendore_excel'),
    path('splendore-qrcode/', views.splendore_qrcode, name='splendore_qrcode'),
    path('splendore-zerar/', views.splendore_zerar, name='splendore_zerar'),
] 