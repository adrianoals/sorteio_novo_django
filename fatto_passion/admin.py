from django.contrib import admin
from .models import Apartamento, Vaga, Sorteio

@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'bloco', 'pne', 'vaga_coberta', 'vaga_dupla')
    search_fields = ('numero', 'bloco')
    list_filter = ('bloco', 'pne', 'vaga_coberta', 'vaga_dupla')

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'bloco', 'pne', 'vaga_coberta')
    search_fields = ('numero', 'bloco')
    list_filter = ('bloco', 'pne', 'vaga_coberta')

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ('apartamento', 'vaga', 'data_sorteio')
    search_fields = ('apartamento__numero', 'apartamento__bloco', 'vaga__numero', 'vaga__bloco')
    list_filter = ('apartamento__bloco', 'vaga__bloco')
