from django.contrib import admin
from .models import Apartamento, Vaga, Sorteio


@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'tipo_vaga_direito')
    list_display_links = ('id', 'numero')
    list_editable = ('tipo_vaga_direito',)
    list_filter = ('tipo_vaga_direito',)
    search_fields = ('numero',)

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'tipo_vaga', 'is_carro', 'is_moto')
    list_display_links = ('id', 'numero')
    list_editable = ('tipo_vaga', 'is_carro', 'is_moto')
    list_filter = ('tipo_vaga', 'is_carro', 'is_moto')
    search_fields = ('numero',)
    
    def save_model(self, request, obj, form, change):
        # Garantir que os campos booleanos sejam atualizados quando o tipo_vaga mudar
        if obj.tipo_vaga == 'Carro':
            obj.is_carro = True
            obj.is_moto = False
        elif obj.tipo_vaga == 'Moto':
            obj.is_carro = False
            obj.is_moto = True
        # Se os booleanos foram alterados manualmente, atualizar o tipo_vaga
        elif obj.is_carro and not obj.is_moto:
            obj.tipo_vaga = 'Carro'
        elif obj.is_moto and not obj.is_carro:
            obj.tipo_vaga = 'Moto'
        super().save_model(request, obj, form, change)

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'vaga', 'data_sorteio')
    list_filter = ('data_sorteio',)
    search_fields = ('apartamento__numero', 'vaga__numero')

