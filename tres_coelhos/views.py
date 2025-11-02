from django.shortcuts import render, redirect
from django.utils import timezone
import random
from django.http import HttpResponse
# from openpyxl import Workbook  # Para gerar o Excel
from openpyxl import load_workbook
import qrcode  # Para gerar o QR Code
from io import BytesIO  # Para manipular imagens em memória
from .models import Apartamento, Vaga, Sorteio, SorteioDupla, DuplaApartamentos


def tres_coelhos_sorteio(request):
    if request.method == 'POST':
        # Limpar registros anteriores de sorteio
        Sorteio.objects.all().delete()
        print("Sorteios anteriores apagados.")

        # Obter todos os apartamentos e vagas LIVRES
        apartamentos_pne = list(Apartamento.objects.filter(is_pne=True))
        apartamentos_demais = list(Apartamento.objects.filter(is_pne=False))
        vagas_pne_livres = list(Vaga.objects.filter(especial='PNE', tipo='LIVRE'))
        vagas_livres_normais = list(Vaga.objects.filter(especial='NORMAL', tipo='LIVRE'))

        print(f"Apartamentos PNE: {len(apartamentos_pne)}")
        print(f"Apartamentos Demais: {len(apartamentos_demais)}")
        print(f"Vagas PNE Livres: {len(vagas_pne_livres)}")
        print(f"Vagas Livres Normais: {len(vagas_livres_normais)}")

        # Lista para armazenar todos os sorteios (bulk insert - otimizado)
        sorteios_para_criar = []

        # REGRA 1: CRITÉRIO DE SUBSOLO (PRIORIDADE MÁXIMA)
        # Processar cada subsolo separadamente
        subsolos = set()
        subsolos.update([apt.subsolo for apt in apartamentos_pne + apartamentos_demais if apt.subsolo])
        subsolos.update([vaga.subsolo for vaga in vagas_pne_livres + vagas_livres_normais])

        print(f"Subsolos encontrados: {sorted(subsolos)}")

        for subsolo in sorted(subsolos):
            print(f"\n--- Processando Subsolo {subsolo} ---")

            # Separar apartamentos e vagas deste subsolo
            pne_subsolo = [apt for apt in apartamentos_pne if apt.subsolo == subsolo]
            demais_subsolo = [apt for apt in apartamentos_demais if apt.subsolo == subsolo]
            vagas_pne_subsolo = [vaga for vaga in vagas_pne_livres if vaga.subsolo == subsolo]
            vagas_normais_subsolo = [vaga for vaga in vagas_livres_normais if vaga.subsolo == subsolo]

            print(f"Subsolo {subsolo}: {len(pne_subsolo)} PNE, {len(demais_subsolo)} Demais")
            print(f"Subsolo {subsolo}: {len(vagas_pne_subsolo)} vagas PNE, {len(vagas_normais_subsolo)} vagas normais")

            # REGRA 2: PRIORIDADE PNE (dentro deste subsolo)
            # Se não há PNE neste subsolo, todas as vagas PNE entram no pool geral deste subsolo
            if not pne_subsolo:
                vagas_normais_subsolo.extend(vagas_pne_subsolo)
                vagas_pne_subsolo = []
                print(f"Subsolo {subsolo}: Sem PNE - todas vagas PNE incluídas no pool geral")

            # ETAPA 1: PNE recebem vagas PNE Livres (se houver PNE e vagas PNE neste subsolo)
            if pne_subsolo and vagas_pne_subsolo:
                random.shuffle(pne_subsolo)
                random.shuffle(vagas_pne_subsolo)
                
                for i, vaga_pne in enumerate(vagas_pne_subsolo):
                    if i < len(pne_subsolo):
                        # PNE recebe vaga PNE Livre do mesmo subsolo
                        sorteios_para_criar.append(
                            Sorteio(apartamento=pne_subsolo[i], vaga=vaga_pne)
                        )
                        print(f"Subsolo {subsolo}: Sorteado PNE {pne_subsolo[i].numero} → Vaga PNE {vaga_pne.numero}")

                # Separar PNE que receberam vaga dos que ficaram sem
                pne_com_vaga = len(vagas_pne_subsolo)
                pne_remanescentes_subsolo = pne_subsolo[pne_com_vaga:]  # PNE que não receberam vaga PNE
                
                # REGRA 3: Vagas PNE não usadas entram no pool geral deste subsolo
                if len(vagas_pne_subsolo) > len(pne_subsolo):
                    vagas_pne_nao_usadas = vagas_pne_subsolo[len(pne_subsolo):]
                    vagas_normais_subsolo.extend(vagas_pne_nao_usadas)
                    print(f"Subsolo {subsolo}: {len(vagas_pne_nao_usadas)} vagas PNE não usadas incluídas no pool geral")
            else:
                # Se não há vagas PNE ou não há PNE que receberam, todos os PNE vão para etapa 2
                pne_remanescentes_subsolo = pne_subsolo
                # Se sobram vagas PNE não usadas, incluir no pool geral
                if vagas_pne_subsolo:
                    vagas_normais_subsolo.extend(vagas_pne_subsolo)
                    print(f"Subsolo {subsolo}: Todas vagas PNE incluídas no pool geral")

            # ETAPA 2: Sorteio geral deste subsolo
            apartamentos_disponiveis_subsolo = pne_remanescentes_subsolo + demais_subsolo
            
            random.shuffle(apartamentos_disponiveis_subsolo)
            random.shuffle(vagas_normais_subsolo)
            
            for i, apartamento in enumerate(apartamentos_disponiveis_subsolo):
                if i < len(vagas_normais_subsolo):
                    # Apartamento recebe vaga livre do mesmo subsolo
                    sorteios_para_criar.append(
                        Sorteio(apartamento=apartamento, vaga=vagas_normais_subsolo[i])
                    )
                    print(f"Subsolo {subsolo}: Sorteado {apartamento.numero} → Vaga Livre {vagas_normais_subsolo[i].numero}")
                else:
                    # Sem mais vagas livres neste subsolo - apartamento vai para sorteio de duplas
                    print(f"Subsolo {subsolo}: Apartamento {apartamento.numero} sem vaga livre → vai para sorteio de duplas")

        # Criar todos os sorteios de uma vez (MUITO MAIS RÁPIDO)
        if sorteios_para_criar:
            Sorteio.objects.bulk_create(sorteios_para_criar)

        # Armazenar informações do sorteio na sessão
        request.session['sorteio_iniciado'] = True
        request.session['horario_conclusao'] = timezone.localtime().strftime("%d/%m/%Y às %Hh %Mmin e %Ss")

        return redirect('tres_coelhos_sorteio')

    else:
        sorteio_iniciado = request.session.get('sorteio_iniciado', False)
        resultados_sorteio = Sorteio.objects.select_related('apartamento', 'vaga').order_by('apartamento__id').all()
        vagas_atribuidas = resultados_sorteio.exists()

        return render(request, 'tres_coelhos/tres_coelhos_sorteio.html', {
            'resultados_sorteio': resultados_sorteio,
            'vagas_atribuidas': vagas_atribuidas,
            'sorteio_iniciado': sorteio_iniciado,
            'horario_conclusao': request.session.get('horario_conclusao', '')
        })



def tres_coelhos_excel(request):
    # Caminho do modelo Excel
    caminho_modelo = 'setup/static/assets/modelos/sorteio_novo.xlsx'

    # Carregar o modelo existente
    wb = load_workbook(caminho_modelo)
    ws = wb.active

    # Ordenar os resultados do sorteio pelo ID do apartamento
    resultados_sorteio = Sorteio.objects.select_related('apartamento', 'vaga').order_by('apartamento__id').all()

    # Pegar o horário de conclusão do sorteio
    horario_conclusao = request.session.get('horario_conclusao', 'Horário não disponível')
    ws['B8'] = f"Sorteio realizado em: {horario_conclusao}"

    # Começar a partir da linha 10 (baseado no layout do seu modelo)
    linha = 10
    for sorteio in resultados_sorteio:
        ws[f'B{linha}'] = sorteio.apartamento.numero  # Número do apartamento
        ws[f'C{linha}'] = sorteio.vaga.numero  # Número da vaga
        ws[f'D{linha}'] = f'Subsolo {sorteio.vaga.subsolo}'  # Subsolo
        ws[f'E{linha}'] = sorteio.vaga.get_tipo_display()  # Tipo da vaga
        ws[f'F{linha}'] = sorteio.vaga.get_especial_display()  # Especialidade da vaga
        linha += 1

    # Configurar a resposta para o download do Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="resultado_sorteio_tres_coelhos.xlsx"'

    # Salvar o arquivo Excel na resposta
    wb.save(response)

    return response



def tres_coelhos_qrcode(request):
    # Obter todos os apartamentos para preencher o dropdown
    apartamentos_disponiveis = Apartamento.objects.all()
    
    # Obter o apartamento selecionado através do filtro (via GET)
    numero_apartamento = request.GET.get('apartamento')
    
    # Inicializar a variável de resultados filtrados como uma lista vazia
    resultados_filtrados = []

    # Se o apartamento foi selecionado, realizar a filtragem dos resultados do sorteio
    if numero_apartamento:
        # Buscar os sorteios para o apartamento selecionado
        sorteios_duplas = SorteioDupla.objects.filter(apartamento__numero=numero_apartamento)

        # Armazenar os resultados filtrados
        resultados_filtrados = sorteios_duplas

    return render(request, 'tres_coelhos/tres_coelhos_qrcode.html', {
        'resultados_filtrados': resultados_filtrados,
        'apartamento_selecionado': numero_apartamento,
        'apartamentos_disponiveis': apartamentos_disponiveis,
    })



def tres_coelhos_dupla(request):
    if request.method == 'POST':
        # Limpar registros anteriores de sorteio de duplas
        SorteioDupla.objects.all().delete()
        print("Sorteios anteriores apagados (duplas).")

        # Obter todas as duplas de apartamentos (pré-selecionadas)
        duplas_apartamentos = list(DuplaApartamentos.objects.all())
        
        # Capturar IDs de apartamentos que fazem parte das duplas
        apartamentos_em_duplas_ids = [dupla.apartamento_1.id for dupla in duplas_apartamentos] + \
                                    [dupla.apartamento_2.id for dupla in duplas_apartamentos if dupla.apartamento_2]

        # Obter apartamentos que não foram sorteados e que não fazem parte de nenhuma dupla
        apartamentos_nao_sorteados = list(Apartamento.objects.exclude(id__in=apartamentos_em_duplas_ids).exclude(sorteio__isnull=False))

        print(f"Duplas formadas: {len(duplas_apartamentos)}")
        print(f"Apartamentos não sorteados: {len(apartamentos_nao_sorteados)}")

        # Obter as vagas duplas disponíveis (para duplas) filtrando por subsolo
        vagas_duplas = list(Vaga.objects.filter(tipo='DUPLA', sorteio__isnull=True))

        print(f"Vagas duplas disponíveis: {len(vagas_duplas)}")

        # **Sorteio de vagas duplas para apartamentos em duplas**
        random.shuffle(duplas_apartamentos)
        for dupla in duplas_apartamentos:
            # Filtrar as vagas de acordo com o subsolo do primeiro apartamento da dupla
            vagas_duplas_subsolo = [vaga for vaga in vagas_duplas if vaga.subsolo == dupla.apartamento_1.subsolo]
            
            if vagas_duplas_subsolo:
                vaga_escolhida_1 = random.choice(vagas_duplas_subsolo)
                vaga_escolhida_2 = vaga_escolhida_1.dupla_com  # Vaga dupla associada

                # Criar o sorteio da dupla
                SorteioDupla.objects.create(apartamento=dupla.apartamento_1, vaga=vaga_escolhida_1)
                SorteioDupla.objects.create(apartamento=dupla.apartamento_2, vaga=vaga_escolhida_2)

                print(f"Sorteado: Apartamento {dupla.apartamento_1.numero} -> Vaga {vaga_escolhida_1.numero}")
                print(f"Sorteado: Apartamento {dupla.apartamento_2.numero} -> Vaga {vaga_escolhida_2.numero}")

                # Remover as vagas duplas da lista de disponíveis
                vagas_duplas.remove(vaga_escolhida_1)
            else:
                print(f"Sem vagas duplas disponíveis no subsolo {dupla.apartamento_1.subsolo}")
                break  # Sem mais vagas duplas no subsolo

        # **Sorteio para apartamentos não sorteados**
        # Apartamentos que não formaram duplas vão concorrer às vagas duplas restantes
        random.shuffle(apartamentos_nao_sorteados)
        
        for apartamento in apartamentos_nao_sorteados:
            # Filtrar as vagas de acordo com o subsolo do apartamento
            vagas_restantes_subsolo = [vaga for vaga in vagas_duplas if vaga.subsolo == apartamento.subsolo]

            if vagas_restantes_subsolo:
                vaga_escolhida = random.choice(vagas_restantes_subsolo)
                SorteioDupla.objects.create(apartamento=apartamento, vaga=vaga_escolhida)
                print(f"Sorteado: Apartamento {apartamento.numero} -> Vaga {vaga_escolhida.numero}")
                vagas_duplas.remove(vaga_escolhida)
            else:
                print(f"Sem vagas disponíveis no subsolo {apartamento.subsolo}")
                break  # Sem mais vagas disponíveis no subsolo

        # Armazenar informações do sorteio na sessão
        request.session['sorteio_dupla_iniciado'] = True
        request.session['horario_conclusao_dupla'] = timezone.localtime().strftime("%d/%m/%Y às %Hh %Mmin e %Ss")

        return redirect('tres_coelhos_dupla')

    else:
        sorteio_iniciado = request.session.get('sorteio_dupla_iniciado', False)
        resultados_sorteio = SorteioDupla.objects.select_related('apartamento', 'vaga').order_by('apartamento__id').all()
        vagas_atribuidas = resultados_sorteio.exists()

        return render(request, 'tres_coelhos/tres_coelhos_dupla.html', {
            'resultados_sorteio': resultados_sorteio,
            'vagas_atribuidas': vagas_atribuidas,
            'sorteio_iniciado': sorteio_iniciado,
            'horario_conclusao': request.session.get('horario_conclusao_dupla', '')
        })



def tres_coelhos_dupla_excel(request):
    # Caminho do modelo Excel
    caminho_modelo = 'setup/static/assets/modelos/sorteio_novo2.xlsx'

    # Carregar o modelo existente
    wb = load_workbook(caminho_modelo)
    ws = wb.active

    # Ordenar os resultados do sorteio pelo ID do apartamento
    resultados_sorteio = SorteioDupla.objects.select_related('apartamento', 'vaga').order_by('apartamento__id').all()

    # Pegar o horário de conclusão do sorteio
    horario_conclusao = request.session.get('horario_conclusao', 'Horário não disponível')
    ws['A8'] = f"Sorteio realizado em: {horario_conclusao}"

    # Começar a partir da linha 10 (baseado no layout do seu modelo)
    linha = 10
    for sorteio in resultados_sorteio:
        ws[f'A{linha}'] = sorteio.apartamento.numero  # Número do apartamento
        ws[f'B{linha}'] = sorteio.vaga.numero  # Número da vaga
        ws[f'C{linha}'] = f'Subsolo {sorteio.vaga.subsolo}'  # Subsolo
        ws[f'D{linha}'] = sorteio.vaga.get_tipo_display()  # Tipo da vaga
        ws[f'E{linha}'] = sorteio.vaga.get_especial_display()  # Especialidade da vaga

        # Adicionar "Dupla Com" (número da vaga associada, se houver)
        ws[f'F{linha}'] = sorteio.vaga.dupla_com.numero if sorteio.vaga.dupla_com else "N/A"  # Número da vaga dupla

        linha += 1

    # Configurar a resposta para o download do Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="resultado_sorteio_dupla_tres_coelhos.xlsx"'

    # Salvar o arquivo Excel na resposta
    wb.save(response)

    return response


def tres_coelhos_zerar(request):
    if request.method == 'POST':
        Sorteio.objects.all().delete()
        SorteioDupla.objects.all().delete()
        return redirect('tres_coelhos_sorteio')
    else:
        return render(request, 'tres_coelhos/tres_coelhos_zerar.html')
    

def tres_coelhos_resultado(request):
    # Obtenha os resultados do sorteio e do sorteio duplo
    resultados_sorteio = list(Sorteio.objects.all())
    resultados_sorteio_dupla = list(SorteioDupla.objects.all())

    # Combine os resultados em uma única lista
    resultados_combinados = resultados_sorteio + resultados_sorteio_dupla

    # Ordene os resultados combinados pelo ID
    resultados_combinados.sort(key=lambda x: x.id)

    # Crie uma lista unificada com dados consistentes
    resultados_formatados = []
    for sorteio in resultados_combinados:
        apartamento_numero = sorteio.apartamento.numero if hasattr(sorteio, 'apartamento') else '-'
        vaga_numero = sorteio.vaga.numero if hasattr(sorteio, 'vaga') else '-'
        vaga_subsolo = sorteio.vaga.subsolo if hasattr(sorteio, 'vaga') else '-'
        tipo_vaga = sorteio.vaga.get_tipo_display() if hasattr(sorteio, 'vaga') else '-'
        especialidade = sorteio.vaga.get_especial_display() if hasattr(sorteio, 'vaga') else '-'
        dupla_com_numero = sorteio.vaga.dupla_com.numero if hasattr(sorteio.vaga, 'dupla_com') and sorteio.vaga.dupla_com else '-'

        resultados_formatados.append({
            'apartamento': apartamento_numero,
            'vaga': vaga_numero,
            'subsolo': vaga_subsolo,
            'tipo_vaga': tipo_vaga,
            'especialidade': especialidade,
            'dupla_com': dupla_com_numero
        })

    # Passe os dados formatados para o contexto
    context = {
        'resultados_combinados': resultados_formatados
    }

    return render(request, 'tres_coelhos/tres_coelhos_resultado.html', context)
