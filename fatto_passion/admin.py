from django.contrib import admin
from .models import Apartamento, Vaga, Sorteio

@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'bloco', 'pne', 'vaga_coberta', 'vaga_dupla')
    search_fields = ('numero', 'bloco')
    list_filter = ('bloco', 'pne', 'vaga_coberta', 'vaga_dupla')
    list_editable = ('pne', 'vaga_coberta', 'vaga_dupla')

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'bloco', 'andar', 'tamanho', 'pne', 'vaga_coberta')
    search_fields = ('numero', 'bloco')
    list_filter = ('bloco', 'andar', 'tamanho', 'pne', 'vaga_coberta')
    list_editable = ('andar', 'tamanho', 'pne', 'vaga_coberta')
    ordering = ('bloco', 'andar', 'numero')

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'vaga', 'data_sorteio')
    search_fields = ('apartamento__numero', 'apartamento__bloco', 'vaga__numero', 'vaga__bloco')
    list_filter = ('apartamento__bloco', 'vaga__bloco')
