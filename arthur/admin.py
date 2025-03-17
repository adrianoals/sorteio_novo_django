from django.contrib import admin
from .models import Apartamento, Vaga, Sorteio

@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "numero_apartamento", "presenca", "prioridade")
    list_filter = ("presenca", "prioridade")
    search_fields = ("numero_apartamento",)
    list_editable = ("presenca", "prioridade")
    ordering = ("numero_apartamento",)

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ("id", "vaga")
    search_fields = ("vaga",)

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ("apartamento", "vaga",)
    autocomplete_fields = ("apartamento", "vaga")
