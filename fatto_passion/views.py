from django.shortcuts import render, redirect
from django.utils import timezone
import random
from django.http import HttpResponse
from django.urls import reverse
from openpyxl import load_workbook
from io import BytesIO
from .models import Apartamento, Vaga, Sorteio
import time
import logging

logger = logging.getLogger(__name__)

# Define os pares fixos de apartamento-vaga (PNE e travadas)
# Serão adicionados posteriormente conforme os dados fornecidos
APARTAMENTOS_VAGAS_FIXAS = {
    # Exemplo: 1: 101,  # Apartamento 1 -> Vaga 101 (PNE)
    # Exemplo: 2: 102,  # Apartamento 2 -> Vaga 102 (travada)
}

# Create your views here.

# View para realizar o sorteio
def fatto_passion_sorteio(request):
    if request.method == 'POST':
        start_time = time.time()
        
        # Limpar registros anteriores de sorteio
        logger.info("Iniciando deleção dos registros anteriores")
        delete_start = time.time()
        Sorteio.objects.all().delete()
        logger.info(f"Deleção concluída em {time.time() - delete_start:.2f} segundos")

        # Obter todos os apartamentos e vagas
        logger.info("Buscando apartamentos e vagas")
        fetch_start = time.time()
        apartamentos = list(Apartamento.objects.all())
        vagas = list(Vaga.objects.all())
        logger.info(f"Busca concluída em {time.time() - fetch_start:.2f} segundos")

        # Lista para armazenar todos os objetos Sorteio
        sorteios_para_criar = []

        # FASE 1: Vagas Travadas (PNE e fixas)
        logger.info("FASE 1: Iniciando atribuição de vagas travadas")
        pne_start = time.time()
        
        for apartamento_id, vaga_id in APARTAMENTOS_VAGAS_FIXAS.items():
            try:
                apartamento = Apartamento.objects.get(id=apartamento_id)
                vaga = Vaga.objects.get(id=vaga_id)
                sorteios_para_criar.append(
                    Sorteio(
                        apartamento=apartamento,
                        vaga=vaga
                    )
                )
                # Remover o apartamento e a vaga das listas de sorteio
                apartamentos = [apt for apt in apartamentos if apt.id != apartamento_id]
                vagas = [v for v in vagas if v.id != vaga_id]
                logger.info(f"Vaga travada atribuída: Apartamento {apartamento_id} -> Vaga {vaga_id}")
            except (Apartamento.DoesNotExist, Vaga.DoesNotExist) as e:
                logger.error(f"Erro ao atribuir vaga travada: {e}")

        logger.info(f"FASE 1 concluída em {time.time() - pne_start:.2f} segundos")

        # FASE 2: Apartamentos com vagas descobertas
        logger.info("FASE 2: Sorteio de apartamentos com vagas descobertas")
        descoberta_start = time.time()
        
        # Filtrar apartamentos que precisam de vagas descobertas
        apartamentos_descobertas = [apt for apt in apartamentos if not apt.vaga_coberta]
        vagas_descobertas = [v for v in vagas if not v.vaga_coberta]
        
        if apartamentos_descobertas and vagas_descobertas:
            # Embaralhar apartamentos e vagas descobertas
            random.shuffle(apartamentos_descobertas)
            random.shuffle(vagas_descobertas)
            
            # Alocar vagas descobertas
            i = 0
            while i < len(apartamentos_descobertas) and i < len(vagas_descobertas):
                apartamento = apartamentos_descobertas[i]
                vaga = vagas_descobertas[i]
                
                sorteios_para_criar.append(
                    Sorteio(
                        apartamento=apartamento,
                        vaga=vaga
                    )
                )
                
                # Remover da lista geral
                apartamentos = [apt for apt in apartamentos if apt.id != apartamento.id]
                vagas = [v for v in vagas if v.id != vaga.id]
                i += 1

        logger.info(f"FASE 2 concluída em {time.time() - descoberta_start:.2f} segundos")

        # FASE 3: Subsolo 3 para apartamentos do bloco Vivant
        logger.info("FASE 3: Subsolo 3 para apartamentos do bloco Vivant")
        subsolo3_start = time.time()
        
        # Filtrar apartamentos do bloco Vivant
        apartamentos_vivant = [apt for apt in apartamentos if apt.bloco == '02.Vivant']
        vagas_subsolo3 = [v for v in vagas if v.andar == 'SUBSOLO_3']
        
        if apartamentos_vivant and vagas_subsolo3:
            # Embaralhar apartamentos Vivant e vagas subsolo 3
            random.shuffle(apartamentos_vivant)
            random.shuffle(vagas_subsolo3)
            
            # Alocar vagas subsolo 3 para apartamentos Vivant
            i = 0
            while i < len(apartamentos_vivant) and i < len(vagas_subsolo3):
                apartamento = apartamentos_vivant[i]
                vaga = vagas_subsolo3[i]
                
                sorteios_para_criar.append(
                    Sorteio(
                        apartamento=apartamento,
                        vaga=vaga
                    )
                )
                
                # Remover da lista geral
                apartamentos = [apt for apt in apartamentos if apt.id != apartamento.id]
                vagas = [v for v in vagas if v.id != vaga.id]
                i += 1

        logger.info(f"FASE 3 concluída em {time.time() - subsolo3_start:.2f} segundos")

        # FASE 4: Subsolo 1 para apartamentos do bloco Amour
        logger.info("FASE 4: Subsolo 1 para apartamentos do bloco Amour")
        subsolo1_start = time.time()
        
        # Filtrar apartamentos do bloco Amour
        apartamentos_amour = [apt for apt in apartamentos if apt.bloco == '01.Amour']
        vagas_subsolo1 = [v for v in vagas if v.andar == 'SUBSOLO_1']
        
        if apartamentos_amour and vagas_subsolo1:
            # Embaralhar apartamentos Amour e vagas subsolo 1
            random.shuffle(apartamentos_amour)
            random.shuffle(vagas_subsolo1)
            
            # Alocar vagas subsolo 1 para apartamentos Amour
            i = 0
            while i < len(apartamentos_amour) and i < len(vagas_subsolo1):
                apartamento = apartamentos_amour[i]
                vaga = vagas_subsolo1[i]
                
                sorteios_para_criar.append(
                    Sorteio(
                        apartamento=apartamento,
                        vaga=vaga
                    )
                )
                
                # Remover da lista geral
                apartamentos = [apt for apt in apartamentos if apt.id != apartamento.id]
                vagas = [v for v in vagas if v.id != vaga.id]
                i += 1

        logger.info(f"FASE 4 concluída em {time.time() - subsolo1_start:.2f} segundos")

        # FASE 5: Subsolo 2 misturado (ambos os blocos)
        logger.info("FASE 5: Subsolo 2 misturado para apartamentos restantes")
        subsolo2_start = time.time()
        
        # Filtrar vagas subsolo 2
        vagas_subsolo2 = [v for v in vagas if v.andar == 'SUBSOLO_2']
        
        if apartamentos and vagas_subsolo2:
            # Embaralhar apartamentos restantes e vagas subsolo 2
            random.shuffle(apartamentos)
            random.shuffle(vagas_subsolo2)
            
            # Alocar vagas subsolo 2 para apartamentos restantes
            i = 0
            while i < len(apartamentos) and i < len(vagas_subsolo2):
                apartamento = apartamentos[i]
                vaga = vagas_subsolo2[i]
                
                sorteios_para_criar.append(
                    Sorteio(
                        apartamento=apartamento,
                        vaga=vaga
                    )
                )
                
                i += 1

        logger.info(f"FASE 5 concluída em {time.time() - subsolo2_start:.2f} segundos")

        # Criar todos os registros de uma vez usando bulk_create
        Sorteio.objects.bulk_create(sorteios_para_criar)
        logger.info(f"Criação dos registros concluída em {time.time() - start_time:.2f} segundos")

        # Marcar o sorteio como iniciado e armazenar o horário de conclusão
        request.session['sorteio_iniciado'] = True
        request.session['horario_conclusao'] = timezone.localtime().strftime("%d/%m/%Y às %Hh %Mmin e %Ss")

        logger.info(f"Sorteio total concluído em {time.time() - start_time:.2f} segundos")
        
        # Redireciona para a mesma página após o sorteio
        return redirect(reverse('fatto_passion_sorteio'))

    # Se o método for GET, exibe os resultados ou a interface de sorteio
    sorteio_iniciado = request.session.get('sorteio_iniciado', False)
    vagas_atribuidas = Sorteio.objects.exists()
    resultados_sorteio = Sorteio.objects.select_related('apartamento', 'vaga').order_by('apartamento__id') if vagas_atribuidas else None

    context = {
        'sorteio_iniciado': sorteio_iniciado,
        'vagas_atribuidas': vagas_atribuidas,
        'resultados_sorteio': resultados_sorteio,
        'horario_conclusao': request.session.get('horario_conclusao', '')
    }

    return render(request, 'fatto_passion/fatto_passion_sorteio.html', context)

def fatto_passion_excel(request):
    # Caminho do modelo Excel
    caminho_modelo = 'setup/static/assets/modelos/sorteiofatto_passion.xlsx'

    # Carregar o modelo existente
    wb = load_workbook(caminho_modelo)
    ws = wb.active

    # Ordenar os resultados do sorteio pelo ID do apartamento
    resultados_sorteio = Sorteio.objects.select_related('apartamento', 'vaga').order_by('apartamento__id').all()

    # Pegar o horário de conclusão do sorteio
    horario_conclusao = request.session.get('horario_conclusao', 'Horário não disponível')
    ws['B8'] = f"Sorteio realizado em: {horario_conclusao}"

    # Começar a partir da linha 10 (baseado no layout do seu modelo)
    linha = 11
    for sorteio in resultados_sorteio:
        ws[f'A{linha}'] = sorteio.apartamento.bloco
        ws[f'B{linha}'] = sorteio.apartamento.numero
        ws[f'C{linha}'] = sorteio.vaga.numero
        ws[f'D{linha}'] = sorteio.vaga.get_andar_display()
        ws[f'E{linha}'] = "PNE" if sorteio.vaga.pne else "-"
        ws[f'F{linha}'] = "Coberta" if sorteio.vaga.vaga_coberta else "Descoberta"
        linha += 1

    # Configurar a resposta para o download do Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sorteio_fatto_passion.xlsx"'

    # Salvar o arquivo Excel na resposta
    wb.save(response)

    return response

def fatto_passion_qrcode(request):
    # Obter todos os apartamentos para preencher o dropdown
    apartamentos_disponiveis = Apartamento.objects.all().order_by('bloco', 'numero')
    
    # Obter o apartamento e bloco selecionados através do filtro (via GET)
    numero_apartamento = request.GET.get('apartamento')
    bloco_selecionado = request.GET.get('bloco')

    # Inicializar a variável de resultados filtrados como uma lista vazia
    resultados_filtrados = []

    # Se o apartamento foi selecionado, realizar a filtragem dos resultados do sorteio
    if numero_apartamento:
        # Construir o filtro base com o número do apartamento
        filtro = {'apartamento__numero': numero_apartamento}
        
        # Se um bloco específico foi selecionado, adicionar ao filtro
        if bloco_selecionado:
            filtro['apartamento__bloco'] = bloco_selecionado
            
        # Buscar os sorteios com os filtros aplicados
        resultados_filtrados = list(Sorteio.objects.filter(**filtro).select_related('apartamento', 'vaga'))
        
        # Debug: verificar se há dados
        print(f"Filtro aplicado: {filtro}")
        print(f"Resultados encontrados: {len(resultados_filtrados)}")
        for resultado in resultados_filtrados:
            print(f"Apartamento: {resultado.apartamento.numero} - Bloco: {resultado.apartamento.bloco}")
            print(f"Vaga: {resultado.vaga.numero} - Andar: {resultado.vaga.get_andar_display()}")

    return render(request, 'fatto_passion/fatto_passion_qrcode.html', {
        'resultados_filtrados': resultados_filtrados,
        'apartamento_selecionado': numero_apartamento,
        'bloco_selecionado': bloco_selecionado,
        'apartamentos_disponiveis': apartamentos_disponiveis,
    })

def fatto_passion_zerar(request):
    if request.method == 'POST':
        Sorteio.objects.all().delete()
        return redirect('fatto_passion_sorteio')
    return render(request, 'fatto_passion/fatto_passion_zerar.html')
