# from django.contrib import admin
# from .models import Bloco, Apartamento, Vaga, Sorteio

# @admin.register(Bloco)
# class BlocoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'numero')  # Exibe o ID e o número do bloco
#     list_filter = ('numero',)  # Adiciona filtro por bloco
#     search_fields = ('numero',)  # Permite busca pelo número do bloco

# @admin.register(Apartamento)
# class ApartamentoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'numero', 'bloco', 'is_pne')  # Inclui o bloco no display
#     list_display_links = ('id', 'numero')
#     list_editable = ('is_pne',)
#     list_filter = ('bloco', 'is_pne')  # Adiciona filtro por bloco
#     search_fields = ('numero', 'bloco__numero')  # Permite busca pelo número do bloco e do apartamento

# @admin.register(Vaga)
# class VagaAdmin(admin.ModelAdmin):
#     list_display = ('id', 'numero', 'bloco', 'is_pne')  # Inclui o bloco no display
#     list_display_links = ('id', 'numero')
#     list_editable = ('is_pne',)
#     list_filter = ('bloco', 'is_pne')  # Adiciona filtro por bloco
#     search_fields = ('numero', 'bloco__numero')  # Permite busca pelo número da vaga e do bloco

# @admin.register(Sorteio)
# class SorteioAdmin(admin.ModelAdmin):
#     list_display = ('id', 'apartamento', 'vaga', 'data_sorteio')
#     list_filter = ('apartamento__bloco', 'vaga__bloco', 'data_sorteio')  # Adiciona filtro pelos blocos dos apartamentos e vagas
#     search_fields = ('apartamento__numero', 'apartamento__bloco__numero', 'vaga__numero', 'vaga__bloco__numero')  # Permite busca detalhada
