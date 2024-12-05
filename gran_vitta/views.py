from django.shortcuts import render, redirect
from django.utils import timezone
import random
from django.http import HttpResponse
from django.urls import reverse
# from openpyxl import Workbook  # Para gerar o Excel
from openpyxl import load_workbook
from io import BytesIO  # Para manipular imagens em memória
from .models import Apartamento, Vaga, Sorteio

# View para realizar o sorteio
def gran_vitta_sorteio(request):
    if request.method == 'POST':
        # Limpar registros anteriores de sorteio
        Sorteio.objects.all().delete()

        # Apartamentos com vagas travadas no Subsolo 01 e 02
        apartamentos_vagas_travadas = {
            '1301': [('13B', '1º Subsolo')],  # Subsolo 01
            '1604': [('15', '1º Subsolo'), ('16', '1º Subsolo')],  # Subsolo 01
            '1603': [('16', '2º Subsolo'), ('17', '2º Subsolo')]   # Subsolo 02
        }

        # Apartamentos com direito a vagas no térreo
        apartamentos_terreo_travados = ['0101', '0102', '0103', '0104', '0201', '0202', '0203', '0204', '0205']

        # Obtenha todos os apartamentos e vagas disponíveis
        apartamentos = list(Apartamento.objects.all())
        vagas_simples = list(Vaga.objects.filter(tipo_vaga='Simples'))  # Convertido para lista
        vagas_duplas = list(Vaga.objects.filter(tipo_vaga='Dupla'))  # Vagas duplas
        vaga_pne = Vaga.objects.filter(is_pne=True).first()  # Vaga PNE do térreo

        # Filtrar as vagas do térreo
        vagas_terreo = [vaga for vaga in vagas_simples if vaga.subsolo == 'Térreo']

        resultados_sorteio = []

        # Logs iniciais
        print("Inicialmente, apartamentos:")
        for apt in apartamentos:
            print(f" - {apt.numero}")

        print("Inicialmente, vagas simples:")
        for vaga in vagas_simples:
            print(f" - {vaga.numero} - {vaga.subsolo} ({vaga.tipo_vaga})")

        print("Inicialmente, vagas duplas:")
        for vaga in vagas_duplas:
            print(f" - {vaga}")

        print(f"Vaga PNE inicial: {vaga_pne.numero if vaga_pne else 'Nenhuma vaga PNE disponível'}")
        print("Vagas no térreo:")
        for vaga in vagas_terreo:
            print(f" - {vaga.numero}")

        # 1. Alocar as vagas travadas
        for apt_num, vagas in apartamentos_vagas_travadas.items():
            apartamento = Apartamento.objects.get(numero=apt_num)
            for vaga_num, subsolo in vagas:
                vaga = Vaga.objects.filter(numero=f'Vaga {vaga_num}', subsolo=subsolo).first()
                if vaga:
                    sorteio = Sorteio.objects.create(apartamento=apartamento, vaga=vaga)
                    resultados_sorteio.append(sorteio)
                    vagas_simples.remove(vaga)
                    print(f"Vaga {vaga.numero} alocada para apartamento {apartamento.numero}.")

        # 2. Sorteio de apartamentos PNE
        apartamento_pne = [apt for apt in apartamentos if apt.is_pne]
        apt_movido_para_subsolo = None

        if apartamento_pne and vaga_pne:
            sorteio_pne = Sorteio.objects.create(apartamento=apartamento_pne[0], vaga=vaga_pne)
            resultados_sorteio.append(sorteio_pne)
            print(f"Vaga PNE {vaga_pne.numero} alocada para apartamento {apartamento_pne[0].numero}.")
            vagas_terreo.remove(vaga_pne)
            apt_movido_para_subsolo = apartamentos_terreo_travados.pop()  # Mover um apt para sorteio no subsolo
            apartamento_pne.pop(0)

        # 3. Sorteio das vagas no térreo
        print("Vagas disponíveis no térreo antes do sorteio:")
        for vaga in vagas_terreo:
            print(f" - {vaga.numero}")

        random.shuffle(vagas_terreo)
        for apt_num in apartamentos_terreo_travados:
            apartamento = Apartamento.objects.get(numero=apt_num)
            if vagas_terreo:
                vaga_terreo = vagas_terreo.pop(0)
                sorteio = Sorteio.objects.create(apartamento=apartamento, vaga=vaga_terreo)
                resultados_sorteio.append(sorteio)
                vagas_simples.remove(vaga_terreo)
                print(f"Vaga {vaga_terreo.numero} do térreo alocada para apartamento {apartamento.numero}.")

        # Verificar se um apartamento foi movido para sorteio com as vagas simples
        if apt_movido_para_subsolo:
            apartamento = Apartamento.objects.get(numero=apt_movido_para_subsolo)
            if vagas_simples:
                vaga_simples = random.choice(vagas_simples)
                sorteio = Sorteio.objects.create(apartamento=apartamento, vaga=vaga_simples)
                resultados_sorteio.append(sorteio)
                vagas_simples.remove(vaga_simples)
                print(f"Vaga {vaga_simples.numero} alocada para apartamento {apartamento.numero}.")

        # 4. Sorteio das vagas duplas
        for apartamento in apartamentos:
            if apartamento.direito_vaga_dupla and apartamento.numero not in apartamentos_vagas_travadas:
                if vagas_duplas:
                    vaga_dupla = random.choice(vagas_duplas)
                    sorteio = Sorteio.objects.create(apartamento=apartamento, vaga=vaga_dupla)
                    resultados_sorteio.append(sorteio)
                    vagas_duplas.remove(vaga_dupla)
                    print(f"Vaga dupla {vaga_dupla.numero} alocada para apartamento {apartamento.numero}.")

        # 5. Sorteio das vagas simples para os demais apartamentos
        for apartamento in apartamentos:
            if apartamento.numero not in apartamentos_vagas_travadas and apartamento.numero not in apartamentos_terreo_travados and not apartamento.direito_vaga_dupla:
                if vagas_simples:
                    vaga_simples = random.choice(vagas_simples)
                    sorteio = Sorteio.objects.create(apartamento=apartamento, vaga=vaga_simples)
                    resultados_sorteio.append(sorteio)
                    vagas_simples.remove(vaga_simples)
                    print(f"Vaga {vaga_simples.numero} alocada para apartamento {apartamento.numero}.")

        # Marcar o sorteio como iniciado e armazenar o horário de conclusão
        request.session['sorteio_iniciado'] = True
        request.session['horario_conclusao'] = timezone.localtime().strftime("%d/%m/%Y às %Hh %Mmin e %Ss")

        # Redireciona para a mesma página após o sorteio
        return redirect(reverse('gran_vitta_sorteio'))

    # Se o método for GET, exibe os resultados ou a interface de sorteio
    sorteio_iniciado = request.session.get('sorteio_iniciado', False)
    vagas_atribuidas = Sorteio.objects.exists()
    # resultados_sorteio = Sorteio.objects.all() if vagas_atribuidas else None
    resultados_sorteio = Sorteio.objects.order_by('apartamento__id') if vagas_atribuidas else None

    context = {
        'sorteio_iniciado': sorteio_iniciado,
        'vagas_atribuidas': vagas_atribuidas,
        'resultados_sorteio': resultados_sorteio,
        'horario_conclusao': request.session.get('horario_conclusao', '')  # Exibe o horário de conclusão
    }

    return render(request, 'gran_vitta/gran_vitta_sorteio.html', context)



def gran_vitta_excel(request):
    # Caminho do modelo Excel
    caminho_modelo = 'setup/static/assets/modelos/sorteioskyview.xlsx'

    # Carregar o modelo existente
    wb = load_workbook(caminho_modelo)
    ws = wb.active

    # Ordenar os resultados do sorteio pelo ID do apartamento
    resultados_sorteio = Sorteio.objects.select_related('apartamento', 'vaga').order_by('apartamento__id').all()

    # Pegar o horário de conclusão do sorteio
    horario_conclusao = request.session.get('horario_conclusao', 'Horário não disponível')
    ws['A8'] = f"Sorteio realizado em: {horario_conclusao}"

    # Começar a partir da linha 10 (baseado no layout do seu modelo)
    linha = 10
    for sorteio in resultados_sorteio:
        ws[f'A{linha}'] = sorteio.apartamento.numero  # Número do apartamento
        ws[f'B{linha}'] = sorteio.vaga.numero  # Número da vaga
        ws[f'C{linha}'] = f'Subsolo {sorteio.vaga.subsolo}'  # Subsolo
        ws[f'D{linha}'] = sorteio.vaga.tipo_vaga  # Tipo da vaga
        linha += 1

    # Configurar a resposta para o download do Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sorteio_gran_vitta.xlsx"'

    # Salvar o arquivo Excel na resposta
    wb.save(response)

    return response



def gran_vitta_qrcode(request):
    # Obter todos os apartamentos para preencher o dropdown
    apartamentos_disponiveis = Apartamento.objects.all()
    
    # Obter o apartamento selecionado através do filtro (via GET)
    numero_apartamento = request.GET.get('apartamento')

    # Inicializar a variável de resultados filtrados como uma lista vazia
    resultados_filtrados = []

    # Se o apartamento foi selecionado, realizar a filtragem dos resultados do sorteio
    if numero_apartamento:
        # Buscar os sorteios para o apartamento selecionado
        resultados_filtrados = Sorteio.objects.filter(apartamento__numero=numero_apartamento)

    return render(request, 'gran_vitta/gran_vitta_qrcode.html', {
        'resultados_filtrados': resultados_filtrados,
        'apartamento_selecionado': numero_apartamento,
        'apartamentos_disponiveis': apartamentos_disponiveis,
    })



def gran_vitta_zerar(request):
    if request.method == 'POST':
        Sorteio.objects.all().delete()
        return redirect('gran_vitta_sorteio')
    else:
        return render(request, 'gran_vitta/gran_vitta_zerar.html')
    

