from django.contrib import admin
from ventura.models import Apartamento, Sorteio, Vaga


class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero_apartamento', 'presenca')
    list_display_links = ('id', 'numero_apartamento', 'presenca')

class VagaAdmin(admin.ModelAdmin):
    list_display = ('id', 'vaga')
    list_display_links = ('id', 'vaga')

class SorteioAdmin(admin.ModelAdmin):
    list_display = ('id', 'apartamento', 'vaga')
    list_display_links = ('id', 'apartamento', 'vaga')


admin.site.register(Apartamento, ApartamentoAdmin)
admin.site.register(Vaga, VagaAdmin)
admin.site.register(Sorteio, SorteioAdmin)

