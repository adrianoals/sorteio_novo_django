from django.contrib import admin
from .models import Apartamento, Vaga, Sorteio

@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'bloco', 'pne', 'vaga_coberta', 'vaga_dupla')
    search_fields = ('numero', 'bloco')
    list_filter = ('bloco', 'pne', 'vaga_coberta', 'vaga_dupla')
    list_editable = ('pne', 'vaga_coberta', 'vaga_dupla')
    actions = ['export_to_csv']
    
    def export_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="apartamentos.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Número', 'Bloco', 'PNE', 'Vaga Coberta', 'Vaga Dupla'])
        
        for apt in queryset:
            writer.writerow([
                apt.id, apt.numero, apt.bloco, 
                'Sim' if apt.pne else 'Não',
                'Sim' if apt.vaga_coberta else 'Não',
                'Sim' if apt.vaga_dupla else 'Não'
            ])
        
        return response
    
    export_to_csv.short_description = "Exportar selecionados para CSV"

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'bloco', 'andar', 'tamanho', 'pne', 'vaga_coberta')
    search_fields = ('numero', 'bloco')
    list_filter = ('bloco', 'andar', 'tamanho', 'pne', 'vaga_coberta')
    list_editable = ('andar', 'tamanho', 'pne', 'vaga_coberta')
    ordering = ('bloco', 'andar', 'numero')
    actions = ['export_to_csv']
    
    def export_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="vagas.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Número', 'Bloco', 'Andar', 'Tamanho', 'PNE', 'Vaga Coberta'])
        
        for vaga in queryset:
            writer.writerow([
                vaga.id, vaga.numero, vaga.bloco, 
                vaga.get_andar_display(), vaga.get_tamanho_display(),
                'Sim' if vaga.pne else 'Não',
                'Sim' if vaga.vaga_coberta else 'Não'
            ])
        
        return response
    
    export_to_csv.short_description = "Exportar selecionados para CSV"

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'vaga', 'data_sorteio')
    search_fields = ('apartamento__numero', 'apartamento__bloco', 'vaga__numero', 'vaga__bloco')
    list_filter = ('apartamento__bloco', 'vaga__bloco')
