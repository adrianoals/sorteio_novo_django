from django.contrib import admin
from .models import Bloco, Apartamento, Vaga, Sorteio

@admin.register(Bloco)
class BlocoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome",)
    search_fields = ("id", "nome",)

@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "numero_apartamento", "bloco", "presenca")
    list_filter = ("bloco", "presenca")
    search_fields = ("numero_apartamento",)
    list_editable = ("presenca",)

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ("id", "vaga", "subsolo")
    list_filter = ("subsolo",)
    search_fields = ("vaga",)

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ("id","apartamento", "get_bloco", "vaga", "get_subsolo")
    list_filter = ("apartamento__bloco", "vaga__subsolo")
    search_fields = ("apartamento__numero_apartamento", "vaga__vaga")

    def get_bloco(self, obj):
        return obj.apartamento.bloco.nome
    get_bloco.admin_order_field = "apartamento__bloco"
    get_bloco.short_description = "Bloco"

    def get_subsolo(self, obj):
        return obj.vaga.subsolo
    get_subsolo.admin_order_field = "vaga__subsolo"
    get_subsolo.short_description = "Subsolo"
