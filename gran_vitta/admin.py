# from django.contrib import admin
# from .models import Apartamento, Vaga, Sorteio


# @admin.register(Apartamento)
# class ApartamentoAdmin(admin.ModelAdmin):
#     list_display = ('id', 'numero', 'is_pne')
#     list_display_links = ('id', 'numero')
#     list_editable = ('is_pne',)
#     list_filter = ('is_pne',)
#     search_fields = ('numero',)

# @admin.register(Vaga)
# class VagaAdmin(admin.ModelAdmin):
#     list_display = ('id', 'numero', 'subsolo', 'is_pne')
#     list_display_links = ('id', 'numero')
#     list_editable = ('is_pne',)
#     list_filter = ('is_pne',)
#     search_fields = ('numero',)

# @admin.register(Sorteio)
# class SorteioAdmin(admin.ModelAdmin):
#     list_display = ('id', 'apartamento', 'vaga', 'data_sorteio')
#     list_filter = ('data_sorteio',)
#     search_fields = ('apartamento__numero', 'vaga__numero')

