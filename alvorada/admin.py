from django.contrib import admin
from .models import Apartamento, Vaga, Sorteio

@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'direito_vaga_dupla')
    search_fields = ('numero',)
    list_filter = ('direito_vaga_dupla',)

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'subsolo', 'tipo_vaga')
    search_fields = ('numero',)
    list_filter = ('subsolo', 'tipo_vaga')

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ('apartamento', 'vaga', 'data_sorteio')
    search_fields = ('apartamento__numero', 'vaga__numero')
    list_filter = ('data_sorteio',)
