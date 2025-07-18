from django.urls import path
from . import views

urlpatterns = [
    path('fatto-passion-sorteio/', views.fatto_passion_sorteio, name='fatto_passion_sorteio'),
    path('fatto-passion-excel/', views.fatto_passion_excel, name='fatto_passion_excel'),
    path('fatto-passion-qrcode/', views.fatto_passion_qrcode, name='fatto_passion_qrcode'),
    path('fatto-passion-zerar/', views.fatto_passion_zerar, name='fatto_passion_zerar'),
] 


