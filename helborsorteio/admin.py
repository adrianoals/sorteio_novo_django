from django.contrib import admin
from .models import Apartamento, Vaga, Sorteio

@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'torre')
    list_filter = ('torre',)
    search_fields = ('numero', 'torre')

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'torre')
    list_filter = ('torre',)
    search_fields = ('numero', 'torre')

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ('apartamento', 'vaga', 'data_sorteio')
    list_filter = ('apartamento__torre', 'vaga__torre')
    search_fields = ('apartamento__numero', 'vaga__numero')
