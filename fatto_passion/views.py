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

# Apartamentos com duas vagas travadas
APARTAMENTOS_DUPLA_VAGA_FIXA = {
    # Exemplo: 3: [103, 104],  # Apartamento 3 -> Vagas 103 e 104 (ambas travadas)
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

        # Primeira Fase: Vagas PNE (travadas)
        logger.info("Iniciando atribuição de vagas PNE travadas")
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
                logger.info(f"Vaga PNE travada atribuída: Apartamento {apartamento_id} -> Vaga {vaga_id}")
            except (Apartamento.DoesNotExist, Vaga.DoesNotExist) as e:
                logger.error(f"Erro ao atribuir vaga PNE travada: {e}")

        # Segunda Fase: Vagas travadas (incluindo duplas)
        logger.info("Iniciando atribuição de vagas travadas")
        travada_start = time.time()
        
        for apartamento_id, vagas_ids in APARTAMENTOS_DUPLA_VAGA_FIXA.items():
            try:
                apartamento = Apartamento.objects.get(id=apartamento_id)
                for vaga_id in vagas_ids:
                    vaga = Vaga.objects.get(id=vaga_id)
                    sorteios_para_criar.append(
                        Sorteio(
                            apartamento=apartamento,
                            vaga=vaga
                        )
                    )
                    vagas = [v for v in vagas if v.id != vaga_id]
                apartamentos = [apt for apt in apartamentos if apt.id != apartamento_id]
                logger.info(f"Vagas travadas duplas atribuídas: Apartamento {apartamento_id} -> Vagas {vagas_ids}")
            except (Apartamento.DoesNotExist, Vaga.DoesNotExist) as e:
                logger.error(f"Erro ao atribuir vagas travadas duplas: {e}")

        logger.info(f"Vagas travadas concluídas em {time.time() - travada_start:.2f} segundos")

        # Terceira Fase: Sorteio Normal por Bloco e Tipo
        logger.info("Iniciando sorteio normal por bloco e tipo")
        normal_start = time.time()
        
        # Agrupar apartamentos e vagas por bloco e tipo
        apartamentos_por_bloco_tipo = {}
        vagas_por_bloco_tipo = {}
        
        for apartamento in apartamentos:
            bloco = apartamento.bloco
            tipo = 'coberta' if apartamento.vaga_coberta else 'descoberta'
            chave = f"{bloco}_{tipo}"
            
            if chave not in apartamentos_por_bloco_tipo:
                apartamentos_por_bloco_tipo[chave] = []
            apartamentos_por_bloco_tipo[chave].append(apartamento)
            
        for vaga in vagas:
            bloco = vaga.bloco
            tipo = 'coberta' if vaga.vaga_coberta else 'descoberta'
            chave = f"{bloco}_{tipo}"
            
            if chave not in vagas_por_bloco_tipo:
                vagas_por_bloco_tipo[chave] = []
            vagas_por_bloco_tipo[chave].append(vaga)

        # Sorteio por bloco e tipo
        for chave in apartamentos_por_bloco_tipo:
            if chave in vagas_por_bloco_tipo:
                apartamentos_grupo = apartamentos_por_bloco_tipo[chave]
                vagas_grupo = vagas_por_bloco_tipo[chave]
                
                # Embaralhar apartamentos e vagas
                random.shuffle(apartamentos_grupo)
                random.shuffle(vagas_grupo)
                
                # Alocar vagas para apartamentos
                i = 0
                while i < len(apartamentos_grupo) and i < len(vagas_grupo):
                    apartamento = apartamentos_grupo[i]
                    vaga = vagas_grupo[i]
                    
                    sorteios_para_criar.append(
                        Sorteio(
                            apartamento=apartamento,
                            vaga=vaga
                        )
                    )
                    
                    # Se o apartamento tem direito a duas vagas, tentar alocar uma segunda
                    if apartamento.vaga_dupla and i + 1 < len(vagas_grupo):
                        segunda_vaga = vagas_grupo[i + 1]
                        sorteios_para_criar.append(
                            Sorteio(
                                apartamento=apartamento,
                                vaga=segunda_vaga
                            )
                        )
                        # Remover a segunda vaga da lista
                        vagas_grupo.pop(i + 1)
                    
                    i += 1

        logger.info(f"Sorteio normal concluído em {time.time() - normal_start:.2f} segundos")

        # Criar todos os registros de uma vez usando bulk_create
        Sorteio.objects.bulk_create(sorteios_para_criar)
        logger.info(f"Criação dos registros concluída em {time.time() - normal_start:.2f} segundos")

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
        ws[f'D{linha}'] = sorteio.vaga.bloco
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
        resultados_filtrados = Sorteio.objects.filter(**filtro)

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
