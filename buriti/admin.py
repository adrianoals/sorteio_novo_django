from django.contrib import admin
from .models import Apartamento, Vaga, Sorteio


@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'bloco')
    list_display_links = ('id', 'numero')
    list_editable = ('bloco',)
    list_filter = ('bloco',)
    search_fields = ('numero', 'bloco')

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'bloco')
    list_display_links = ('id', 'numero')
    list_editable = ('bloco',)
    list_filter = ('bloco',)
    search_fields = ('numero', 'bloco')

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'vaga', 'data_sorteio')
    list_filter = ('data_sorteio', 'apartamento__bloco')
    search_fields = ('apartamento__numero', 'apartamento__bloco', 'vaga__numero')

