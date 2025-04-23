from django.urls import path
from . import views

urlpatterns = [
    path('alvorada-sorteio/', views.alvorada_sorteio, name='alvorada_sorteio'),
    path('excel/', views.alvorada_excel, name='alvorada_excel'),
    path('qrcode/', views.alvorada_qrcode, name='alvorada_qrcode'),
    path('zerar/', views.alvorada_zerar, name='alvorada_zerar'),
] 