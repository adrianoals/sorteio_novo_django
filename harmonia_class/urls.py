from django.urls import path
from harmonia_class.views import (
    harmonia_class_sorteio,
    harmonia_class_excel,
    harmonia_class_qrcode,
    harmonia_class_zerar,
)

urlpatterns = [
    path('harmonia-class-sorteio/', harmonia_class_sorteio, name='harmonia_class_sorteio'),
    path('harmonia-class-excel', harmonia_class_excel, name='harmonia_class_excel'),
    path('harmonia-class-qrcode', harmonia_class_qrcode, name='harmonia_class_qrcode'),
    path('harmonia-class-zerar/', harmonia_class_zerar, name='harmonia_class_zerar'),
]
