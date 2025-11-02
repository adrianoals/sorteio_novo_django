from django.contrib import admin
from .models import Apartamento, Vaga, Sorteio, DuplaApartamentos, SorteioDupla
from django.core.exceptions import ValidationError
from django import forms


# Customizando a exibição do model Apartamento no admin
@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'is_pne', 'is_idoso', 'subsolo', 'apenas_dupla', 'apenas_livre')  # Exibe o ID, o número, PNE, Idoso, Subsolo, Dupla e Livre
    list_display_links = ('id', 'numero')  # Links clicáveis para edição
    list_editable = ('is_pne', 'is_idoso', 'subsolo', 'apenas_dupla', 'apenas_livre')  # Permite edição direta
    list_filter = ('is_pne', 'is_idoso', 'subsolo', 'apenas_dupla', 'apenas_livre')  # Filtros para facilitar a seleção
    search_fields = ['numero']  # Adiciona a possibilidade de busca por número do apartamento

# Customizando a exibição do model Vaga no admin
@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'tipo', 'especial', 'subsolo', 'is_livre_quando_nao_especial', 'dupla_com')  # Exibe informações importantes das vagas
    list_display_links = ('id', 'numero', 'tipo', 'especial', 'subsolo', 'is_livre_quando_nao_especial', 'dupla_com')  # Links clicáveis para edição
    list_filter = ('tipo', 'especial', 'subsolo', 'is_livre_quando_nao_especial')  # Filtros para facilitar a navegação no admin
    search_fields = ['numero']  # Permite busca por número da vaga

# Customizando a exibição do model Sorteio no admin
@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'vaga', 'data_sorteio')  # Exibe o ID, apartamento, vaga e data do sorteio
    list_display_links = ('id', 'apartamento', 'vaga')  # Links clicáveis para edição
    list_filter = ('apartamento', 'vaga')  # Filtros para facilitar a navegação
    date_hierarchy = 'data_sorteio'  # Permite filtragem por data do sorteio


class DuplaApartamentosForm(forms.ModelForm):
    class Meta:
        model = DuplaApartamentos
        fields = ['apartamento_1', 'apartamento_2']

    def clean(self):
        cleaned_data = super().clean()
        apartamento_1 = cleaned_data.get("apartamento_1")
        apartamento_2 = cleaned_data.get("apartamento_2")

        if apartamento_1 == apartamento_2:
            raise ValidationError("Os dois apartamentos não podem ser iguais.")

        return cleaned_data

@admin.register(DuplaApartamentos)
class DuplaApartamentosAdmin(admin.ModelAdmin):
    form = DuplaApartamentosForm
    list_display = ('apartamento_1', 'apartamento_2', 'data_criacao')

    # Filtra para que apenas apartamentos que não foram sorteados e que não estão em outra dupla apareçam
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ['apartamento_1', 'apartamento_2']:
            # Captura apenas os IDs dos apartamentos que já estão em uma dupla
            used_apartments_1 = DuplaApartamentos.objects.values_list('apartamento_1', flat=True)
            used_apartments_2 = DuplaApartamentos.objects.values_list('apartamento_2', flat=True)

            # Exclui os apartamentos já sorteados e os que já estão em duplas
            kwargs["queryset"] = Apartamento.objects.exclude(id__in=used_apartments_1).exclude(id__in=used_apartments_2).exclude(sorteio__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(SorteioDupla)
class SorteioDuplaAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'vaga', 'vaga_dupla', 'data_sorteio')

    def vaga_dupla(self, obj):
        # Acessa a vaga dupla associada (via vaga.dupla_com)
        return obj.vaga.dupla_com.numero if obj.vaga.dupla_com else 'N/A'
    
    vaga_dupla.short_description = 'Vaga Dupla Com'  # Nome da coluna no admin
