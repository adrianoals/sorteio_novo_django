from django.contrib import admin
from .models import Apartamento, Vaga, Sorteio


@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'direito_vaga_dupla', 'direito_duas_vagas_livres', 'is_pne')
    list_display_links = ('id', 'numero')
    list_editable = ('direito_vaga_dupla', 'direito_duas_vagas_livres', 'is_pne')
    list_filter = ('direito_vaga_dupla', 'direito_duas_vagas_livres', 'is_pne')
    search_fields = ('numero',)

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'subsolo', 'tipo_vaga', 'is_pne')
    list_display_links = ('id', 'numero')
    list_editable = ('subsolo', 'tipo_vaga', 'is_pne')
    list_filter = ('subsolo', 'tipo_vaga', 'is_pne')
    search_fields = ('numero',)

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'vaga', 'data_sorteio')
    list_filter = ('data_sorteio',)
    search_fields = ('apartamento__numero', 'vaga__numero')

