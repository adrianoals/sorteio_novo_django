# from django.contrib import admin
# from .models import Bloco, Apartamento, Vaga, Sorteio

# @admin.register(Bloco)
# class BlocoAdmin(admin.ModelAdmin):
#     list_display = ("id", "nome")
#     search_fields = ("id", "nome")
#     ordering = ("nome",)

# @admin.register(Apartamento)
# class ApartamentoAdmin(admin.ModelAdmin):
#     list_display = ("id", "numero_apartamento", "get_bloco", "presenca", "prioridade")
#     list_filter = ("bloco", "presenca", "prioridade")
#     search_fields = ("numero_apartamento",)
#     list_editable = ("presenca", "prioridade")
#     ordering = ("bloco", "numero_apartamento")
#     autocomplete_fields = ("bloco",)

#     def get_bloco(self, obj):
#         return obj.bloco.nome if obj.bloco else "-"
#     get_bloco.admin_order_field = "bloco"
#     get_bloco.short_description = "Bloco"

# @admin.register(Vaga)
# class VagaAdmin(admin.ModelAdmin):
#     list_display = ("id", "vaga", "subsolo", "get_bloco")
#     list_filter = ("subsolo", "bloco")
#     search_fields = ("vaga",)
#     ordering = ("subsolo", "vaga")
#     autocomplete_fields = ("bloco",)

#     def get_bloco(self, obj):
#         return obj.bloco.nome if obj.bloco else "Torre 2 e Torre 3"
#     get_bloco.admin_order_field = "bloco"
#     get_bloco.short_description = "Bloco"

# @admin.register(Sorteio)
# class SorteioAdmin(admin.ModelAdmin):
#     list_display = ("id", "apartamento", "get_bloco", "vaga", "get_subsolo")
#     list_filter = ("apartamento__bloco", "vaga__subsolo")
#     search_fields = ("apartamento__numero_apartamento", "vaga__vaga")
#     ordering = ("apartamento__bloco", "apartamento__numero_apartamento")
#     autocomplete_fields = ("apartamento", "vaga")

#     def get_bloco(self, obj):
#         return obj.apartamento.bloco.nome if obj.apartamento.bloco else "-"
#     get_bloco.admin_order_field = "apartamento__bloco"
#     get_bloco.short_description = "Bloco"

#     def get_subsolo(self, obj):
#         return obj.vaga.subsolo if obj.vaga else "-"
#     get_subsolo.admin_order_field = "vaga__subsolo"
#     get_subsolo.short_description = "Subsolo"
