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

        # SIMPLIFICAÇÃO: Mapeamento fixo de subsolo -> vaga PNE livre
        # Como existe exatamente 1 vaga PNE livre por subsolo, pré-mapeamos
        # Vagas PNE esperadas: Subsolo 1 → ID 43, Subsolo 2 → ID 95
        vaga_pne_esperada = {1: 43, 2: 95}  # Mapeamento esperado: subsolo -> id_vaga
        
        vaga_pne_por_subsolo = {}
        for vaga_pne in vagas_pne_livres:
            if vaga_pne.subsolo not in vaga_pne_por_subsolo:
                vaga_pne_por_subsolo[vaga_pne.subsolo] = vaga_pne
                # Validar se encontrou a vaga PNE esperada
                id_esperado = vaga_pne_esperada.get(vaga_pne.subsolo)
                status_validacao = "✅ CORRETO" if vaga_pne.id == id_esperado else f"⚠️ ESPERADO ID {id_esperado}"
                print(f"Mapeamento fixo: Subsolo {vaga_pne.subsolo} → Vaga PNE {vaga_pne.numero} (ID: {vaga_pne.id}) {status_validacao}")
            else:
                print(f"⚠️ ATENÇÃO: Múltiplas vagas PNE no Subsolo {vaga_pne.subsolo} - usando a primeira encontrada")

        # Lista para armazenar todos os sorteios (bulk insert - otimizado)
        sorteios_para_criar = []

        # REGRA 1: CRITÉRIO DE SUBSOLO (PRIORIDADE MÁXIMA)
        # Processar cada subsolo separadamente
        subsolos = set()
        subsolos.update([apt.subsolo for apt in apartamentos_pne + apartamentos_demais if apt.subsolo])
        subsolos.update([vaga.subsolo for vaga in vagas_livres_normais])
        subsolos.update(vaga_pne_por_subsolo.keys())

        print(f"Subsolos encontrados: {sorted(subsolos)}")

        for subsolo in sorted(subsolos):
            print(f"\n--- Processando Subsolo {subsolo} ---")

            # Separar apartamentos e vagas deste subsolo
            pne_subsolo = [apt for apt in apartamentos_pne if apt.subsolo == subsolo]
            demais_subsolo = [apt for apt in apartamentos_demais if apt.subsolo == subsolo]
            vagas_normais_subsolo = [vaga for vaga in vagas_livres_normais if vaga.subsolo == subsolo]

            print(f"Subsolo {subsolo}: {len(pne_subsolo)} PNE, {len(demais_subsolo)} Demais")
            print(f"Subsolo {subsolo}: {len(vagas_normais_subsolo)} vagas livres normais")

            # Inicializar PNE remanescentes (sempre inicializado para evitar erros)
            pne_remanescentes_subsolo = []

            # ETAPA 1: 1 PNE do subsolo ocupa a vaga PNE fixa daquele subsolo
            vaga_pne_fixa = vaga_pne_por_subsolo.get(subsolo)
            
            if vaga_pne_fixa and pne_subsolo:
                # Sortear 1 PNE para ocupar a vaga PNE fixa
                random.shuffle(pne_subsolo)
                pne_escolhido = pne_subsolo[0]
                
                # Atribuir vaga PNE fixa ao PNE escolhido
                sorteios_para_criar.append(
                    Sorteio(apartamento=pne_escolhido, vaga=vaga_pne_fixa)
                )
                print(f"Subsolo {subsolo}: Sorteado PNE {pne_escolhido.numero} → Vaga PNE {vaga_pne_fixa.numero} (fixa)")

                # PNE restantes do mesmo subsolo concorrem exclusivamente às vagas livres remanescentes
                pne_remanescentes_subsolo = pne_subsolo[1:]
                
                if pne_remanescentes_subsolo:
                    print(f"Subsolo {subsolo}: {len(pne_remanescentes_subsolo)} PNE remanescentes que devem receber vaga livre normal")
            elif pne_subsolo:
                # Há PNE mas não há vaga PNE fixa neste subsolo - todos os PNE vão para sorteio de vagas livres
                pne_remanescentes_subsolo = pne_subsolo
                print(f"Subsolo {subsolo}: {len(pne_remanescentes_subsolo)} PNE sem vaga PNE fixa - todos devem receber vaga livre normal")
            elif vaga_pne_fixa:
                # Há vaga PNE fixa mas não há PNE - vaga PNE não é atribuída (fica disponível?)
                # Na verdade, se não há PNE, a vaga PNE não deve ser atribuída a ninguém na Fase 1
                print(f"Subsolo {subsolo}: Vaga PNE fixa disponível mas sem PNE - vaga não será atribuída na Fase 1")

            # ETAPA 1b: PNE remanescentes recebem vagas livres (PRIORIDADE - antes dos demais)
            if pne_remanescentes_subsolo and vagas_normais_subsolo:
                random.shuffle(pne_remanescentes_subsolo)
                random.shuffle(vagas_normais_subsolo)
                
                # Atribuir vagas livres aos PNE remanescentes (número máximo é o menor entre vagas e PNE)
                num_atribuicoes_pne_remanescentes = min(len(pne_remanescentes_subsolo), len(vagas_normais_subsolo))
                
                for i in range(num_atribuicoes_pne_remanescentes):
                    # PNE remanescente recebe vaga livre do mesmo subsolo
                    sorteios_para_criar.append(
                        Sorteio(apartamento=pne_remanescentes_subsolo[i], vaga=vagas_normais_subsolo[i])
                    )
                    print(f"Subsolo {subsolo}: Sorteado PNE remanescente {pne_remanescentes_subsolo[i].numero} → Vaga Livre {vagas_normais_subsolo[i].numero}")
                
                # Remover vagas já atribuídas dos PNE remanescentes
                vagas_normais_subsolo = vagas_normais_subsolo[num_atribuicoes_pne_remanescentes:]
                
                if len(pne_remanescentes_subsolo) > num_atribuicoes_pne_remanescentes:
                    pne_sem_vaga = len(pne_remanescentes_subsolo) - num_atribuicoes_pne_remanescentes
                    print(f"Subsolo {subsolo}: ⚠️ {pne_sem_vaga} PNE remanescente(s) sem vaga livre (vagas esgotadas neste subsolo)")

            # ETAPA 1c: Demais apartamentos disputam as vagas livres restantes
            if demais_subsolo and vagas_normais_subsolo:
                random.shuffle(demais_subsolo)
                random.shuffle(vagas_normais_subsolo)
                
                # Atribuir vagas livres aos demais apartamentos (número máximo é o menor entre vagas e apartamentos)
                num_atribuicoes_demais = min(len(demais_subsolo), len(vagas_normais_subsolo))
                
                for i in range(num_atribuicoes_demais):
                    # Demais apartamento recebe vaga livre do mesmo subsolo
                    sorteios_para_criar.append(
                        Sorteio(apartamento=demais_subsolo[i], vaga=vagas_normais_subsolo[i])
                    )
                    print(f"Subsolo {subsolo}: Sorteado {demais_subsolo[i].numero} → Vaga Livre {vagas_normais_subsolo[i].numero}")
                
                if len(demais_subsolo) > num_atribuicoes_demais:
                    demais_sem_vaga = len(demais_subsolo) - num_atribuicoes_demais
                    print(f"Subsolo {subsolo}: {demais_sem_vaga} apartamento(s) sem vaga livre → vai(ão) para sorteio de duplas")

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

        # Obter apartamentos que já foram sorteados na Fase 1 (têm vaga livre)
        apartamentos_com_vaga_livre = set(Sorteio.objects.values_list('apartamento_id', flat=True))
        
        # Obter todas as duplas pré-cadastradas
        duplas_pre_cadastradas = list(DuplaApartamentos.objects.all())
        
        # REGRA 2: Filtrar duplas válidas (ambos não foram sorteados na Fase 1)
        duplas_validas = []
        for dupla in duplas_pre_cadastradas:
            apt1_sorteado = dupla.apartamento_1.id in apartamentos_com_vaga_livre
            apt2_sorteado = dupla.apartamento_2.id in apartamentos_com_vaga_livre if dupla.apartamento_2 else False
            
            # Dupla é válida se nenhum dos apartamentos foi sorteado na Fase 1
            if not apt1_sorteado and not apt2_sorteado and dupla.apartamento_2:
                # REGRA 3: Verificar se ambos pertencem ao mesmo subsolo
                if dupla.apartamento_1.subsolo == dupla.apartamento_2.subsolo:
                    duplas_validas.append(dupla)
                else:
                    print(f"Dupla desfeita: Apartamentos {dupla.apartamento_1.numero} e {dupla.apartamento_2.numero} em subsolos diferentes")
            else:
                print(f"Dupla desfeita: Um dos apartamentos já foi sorteado na Fase 1 ({dupla.apartamento_1.numero}, {dupla.apartamento_2.numero if dupla.apartamento_2 else 'N/A'})")

        print(f"Duplas válidas (pré-configuradas): {len(duplas_validas)}")

        # Obter apartamentos que NÃO foram sorteados na Fase 1
        apartamentos_sem_vaga = list(Apartamento.objects.exclude(id__in=apartamentos_com_vaga_livre))

        # Obter vagas duplas disponíveis (não sorteadas na Fase 1)
        # Como SorteioDupla já foi limpo no início, não precisamos filtrar por SorteioDupla
        # Uma vaga dupla não pode estar em Sorteio (Fase 1 - vagas livres)
        vagas_duplas_ids_nao_usadas_na_fase1 = set(Vaga.objects.filter(tipo='DUPLA').exclude(
            id__in=Sorteio.objects.values_list('vaga_id', flat=True)
        ).values_list('id', flat=True))
        
        vagas_duplas = list(Vaga.objects.filter(id__in=vagas_duplas_ids_nao_usadas_na_fase1).select_related('dupla_com'))

        print(f"Apartamentos sem vaga (da Fase 1): {len(apartamentos_sem_vaga)}")
        print(f"Vagas duplas disponíveis: {len(vagas_duplas)}")

        # Lista para armazenar todos os sorteios (bulk insert - otimizado)
        sorteios_dupla_para_criar = []

        # REGRA 1: CRITÉRIO DE SUBSOLO (PRIORIDADE MÁXIMA)
        # Processar cada subsolo separadamente
        subsolos = set()
        subsolos.update([apt.subsolo for apt in apartamentos_sem_vaga if apt.subsolo])
        subsolos.update([vaga.subsolo for vaga in vagas_duplas])

        print(f"Subsolos encontrados: {sorted(subsolos)}")

        for subsolo in sorted(subsolos):
            print(f"\n--- Processando Subsolo {subsolo} (Vagas Duplas) ---")

            # Separar duplas válidas deste subsolo
            duplas_subsolo = [d for d in duplas_validas if d.apartamento_1.subsolo == subsolo]
            apartamentos_subsolo = [apt for apt in apartamentos_sem_vaga if apt.subsolo == subsolo]
            vagas_duplas_subsolo = [vaga for vaga in vagas_duplas if vaga.subsolo == subsolo]

            print(f"Subsolo {subsolo}: {len(duplas_subsolo)} duplas válidas, {len(apartamentos_subsolo)} apartamentos sem vaga")
            print(f"Subsolo {subsolo}: {len(vagas_duplas_subsolo)} vagas duplas disponíveis")
            print(f"Subsolo {subsolo}: Apartamentos IDs: {[apt.numero for apt in apartamentos_subsolo]}")

            # REGRA 3: Sorteio das duplas pré-configuradas (primeiro)
            random.shuffle(duplas_subsolo)
            random.shuffle(vagas_duplas_subsolo)
            
            # Criar lista de IDs de apartamentos já sorteados nesta etapa
            apartamentos_sorteados_dupla = set()
            
            # Criar dicionário para mapear vagas e seus pares
            vagas_disponiveis_set = set(vagas_duplas_subsolo)
            vagas_usadas = set()
            
            for dupla in duplas_subsolo:
                # Encontrar par de vagas duplas disponíveis
                vaga_encontrada = None
                vaga_par = None
                
                # Buscar par de vagas duplas (uma deve ter dupla_com apontando para a outra)
                for vaga in vagas_duplas_subsolo:
                    if vaga.id in vagas_usadas:
                        continue
                    
                    if vaga.dupla_com and vaga.dupla_com.id in [v.id for v in vagas_duplas_subsolo if v.id not in vagas_usadas]:
                        vaga_encontrada = vaga
                        vaga_par = vaga.dupla_com
                        break
                
                if vaga_encontrada and vaga_par:
                    # Criar sorteios da dupla
                    sorteios_dupla_para_criar.append(
                        SorteioDupla(apartamento=dupla.apartamento_1, vaga=vaga_encontrada)
                    )
                    sorteios_dupla_para_criar.append(
                        SorteioDupla(apartamento=dupla.apartamento_2, vaga=vaga_par)
                    )
                    
                    apartamentos_sorteados_dupla.add(dupla.apartamento_1.id)
                    apartamentos_sorteados_dupla.add(dupla.apartamento_2.id)
                    
                    # Marcar vagas como usadas (evita usar remove())
                    vagas_usadas.add(vaga_encontrada.id)
                    vagas_usadas.add(vaga_par.id)
                    
                    print(f"Subsolo {subsolo}: Dupla sorteada - {dupla.apartamento_1.numero} → Vaga {vaga_encontrada.numero}, {dupla.apartamento_2.numero} → Vaga {vaga_par.numero}")
                else:
                    print(f"Subsolo {subsolo}: Dupla ({dupla.apartamento_1.numero}, {dupla.apartamento_2.numero}) sem par de vagas duplas disponível")

            # REGRA 4: Sorteio dos apartamentos restantes - Sem formar novas duplas (atribuição individual)
            apartamentos_restantes_subsolo = [apt for apt in apartamentos_subsolo if apt.id not in apartamentos_sorteados_dupla]
            
            print(f"Subsolo {subsolo}: Apartamentos restantes após duplas pré-configuradas: {len(apartamentos_restantes_subsolo)}")
            print(f"Subsolo {subsolo}: Apartamentos restantes IDs: {[apt.numero for apt in apartamentos_restantes_subsolo]}")
            print(f"Subsolo {subsolo}: Vagas usadas até agora: {len(vagas_usadas)}")
            
            random.shuffle(apartamentos_restantes_subsolo)
            
            # REGRA 4: Sorteio dos apartamentos restantes - Sem formar novas duplas (atribuição individual)
            # IMPORTANTE: Quando atribuímos uma vaga dupla individualmente, ela é atribuída sozinha.
            # A vaga par (dupla_com) permanece disponível para ser atribuída a outro apartamento.
            # Isso significa que se temos um par de vagas (Vaga A <-> Vaga B), ambas podem ser atribuídas individualmente.
            for apartamento in apartamentos_restantes_subsolo:
                # Filtrar vagas não usadas (atualizado a cada iteração)
                vagas_disponiveis = [v for v in vagas_duplas_subsolo if v.id not in vagas_usadas]
                
                if vagas_disponiveis:
                    # Apartamento recebe vaga dupla individualmente (sem formar par com outro apartamento)
                    # A vaga par (dupla_com) permanece disponível para outro apartamento
                    vaga_escolhida = vagas_disponiveis[0]  # Pega a primeira vaga disponível
                    sorteios_dupla_para_criar.append(
                        SorteioDupla(apartamento=apartamento, vaga=vaga_escolhida)
                    )
                    
                    apartamentos_sorteados_dupla.add(apartamento.id)
                    vagas_usadas.add(vaga_escolhida.id)
                    # NÃO marcamos a vaga par (dupla_com) como usada aqui, pois ela pode ser atribuída a outro apartamento
                    
                    par_info = f" (Par: {vaga_escolhida.dupla_com.numero})" if vaga_escolhida.dupla_com else ""
                    print(f"Subsolo {subsolo}: Apartamento {apartamento.numero} → Vaga Dupla {vaga_escolhida.numero}{par_info}")
                else:
                    print(f"Subsolo {subsolo}: Apartamento {apartamento.numero} sem vaga dupla disponível neste subsolo")
                    break  # Não há mais vagas disponíveis, parar o loop

        # Criar todos os sorteios de uma vez (MUITO MAIS RÁPIDO)
        if sorteios_dupla_para_criar:
            SorteioDupla.objects.bulk_create(sorteios_dupla_para_criar)
            print(f"\nTotal de sorteios de duplas criados: {len(sorteios_dupla_para_criar)}")
        else:
            print("\n⚠️ ATENÇÃO: Nenhum sorteio de dupla foi criado!")
        
        # Verificação final: contar vagas duplas não atribuídas
        total_vagas_duplas = Vaga.objects.filter(tipo='DUPLA').count()
        vagas_duplas_usadas_fase1 = Sorteio.objects.filter(vaga__tipo='DUPLA').count()
        vagas_duplas_usadas_fase2 = SorteioDupla.objects.count()
        
        print(f"\n📊 RESUMO FINAL:")
        print(f"Total de vagas duplas no sistema: {total_vagas_duplas}")
        print(f"Vagas duplas usadas na Fase 1 (erro): {vagas_duplas_usadas_fase1}")
        print(f"Vagas duplas atribuídas na Fase 2: {vagas_duplas_usadas_fase2}")
        print(f"Vagas duplas ainda disponíveis: {total_vagas_duplas - vagas_duplas_usadas_fase1 - vagas_duplas_usadas_fase2}")

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
