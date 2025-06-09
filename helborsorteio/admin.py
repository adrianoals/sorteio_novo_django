from django.contrib import admin
from .models import Apartamento, Vaga, Sorteio

@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'torre', 'pne')
    list_filter = ('torre', 'pne')
    search_fields = ('numero', 'torre')
    list_editable = ('pne',)

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'torre', 'pne')
    list_filter = ('torre', 'pne')
    search_fields = ('numero', 'torre')
    list_editable = ('pne',)

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'vaga', 'data_sorteio')
    list_filter = ('apartamento__torre', 'vaga__torre')
    search_fields = ('apartamento__numero', 'vaga__numero')
