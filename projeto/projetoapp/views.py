from django.shortcuts import render, get_object_or_404, redirect
from .models import Campo, Reserva, Perfil
from .forms import ReservaCampoForm, EditarPerfilForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
import logging
from django.http import HttpResponse
from datetime import timedelta, datetime
from decimal import Decimal

logger = logging.getLogger(__name__)

def index(request):
    campos = Campo.objects.all()
    filtro_cidade = request.GET.get('cidade', '')
    filtro_gramado = request.GET.get('tipo_gramado', '')
    filtro_iluminacao = request.GET.get('iluminacao', '')

    if filtro_cidade:
        campos = campos.filter(cidade__icontains=filtro_cidade)
    if filtro_gramado:
        campos = campos.filter(tipo_gramado=filtro_gramado)
    if filtro_iluminacao:
        campos = campos.filter(iluminacao=(filtro_iluminacao == 'true'))

    return render(request, 'index.html', {'campos': campos})

def is_admin(user):
    return user.is_superuser

@login_required(login_url='/login/')
def detalhes_campo(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)

    # Verifica se o formulário foi enviado para a confirmação
    if request.method == 'POST':
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')

        # Se os dados de data não forem fornecidos, exibe erro
        if not data_inicio or not data_fim:
            messages.error(request, "Data de início e fim são obrigatórios.")
            return render(request, 'detalhes_campo.html', {'campo': campo})

        # Converte as datas de string para datetime
        try:
            data_inicio = datetime.strptime(data_inicio, "%Y-%m-%dT%H:%M")
            data_fim = datetime.strptime(data_fim, "%Y-%m-%dT%H:%M")
            
            # Verifica se já existe uma reserva no mesmo campo, nas mesmas datas
            if Reserva.objects.filter(campo=campo, data_inicio__lte=data_fim, data_fim__gte=data_inicio).exists():
                messages.error(request, "Este campo já está reservado para esse horário. Tente outro horário.")
                return render(request, 'detalhes_campo.html', {'campo': campo, 'data_inicio': data_inicio, 'data_fim': data_fim})

            # Converte as datas para string no formato adequado
            data_inicio_str = data_inicio.strftime("%Y-%m-%dT%H:%M")
            data_fim_str = data_fim.strftime("%Y-%m-%dT%H:%M")

            # Se não houver conflito, redireciona para a página de confirmação da reserva
            return redirect('confirmar_reserva', campo_id=campo.id, inicio=data_inicio_str, fim=data_fim_str)

        except ValueError:
            messages.error(request, "Erro ao processar as datas.")
            return render(request, 'detalhes_campo.html', {'campo': campo})

    # Se não for POST, apenas renderiza a página do campo
    return render(request, 'detalhes_campo.html', {'campo': campo})

@login_required(login_url='/login/')
def confirmar_reserva(request, campo_id, inicio, fim):
    # Converte as strings de data para objetos datetime
    try:
        data_inicio = datetime.strptime(inicio, "%Y-%m-%dT%H:%M")
        data_fim = datetime.strptime(fim, "%Y-%m-%dT%H:%M")
    except ValueError:
        # Se as datas não forem válidas, redireciona ou exibe erro
        messages.error(request, "Formato de data inválido.")
        return redirect('home')

    # Recupera o campo e cria uma nova reserva com os dados fornecidos
    campo = get_object_or_404(Campo, id=campo_id)

    # Calcula a duração e o valor total
    duracao = (data_fim - data_inicio).total_seconds() / 3600  # Duração em horas
    valor_total = campo.preco_por_hora * Decimal(duracao)

    if request.method == "POST":
        # Aqui você pega a forma de pagamento escolhida
        pagamento = request.POST.get('pagamento')

        # Cria a reserva
        reserva = Reserva.objects.create(
            campo=campo,
            usuario=request.user,
            data_inicio=data_inicio,
            data_fim=data_fim,
            valor_total=valor_total,
            pagamento=pagamento
        )
        
        # Após a confirmação, você pode redirecionar para uma página de sucesso ou exibir uma mensagem
        messages.success(request, f"Reserva confirmada! Valor total: R$ {round(valor_total, 2)}.")
        return redirect('index')  # Ou redirecionar para uma página de detalhes da reserva
    
    # Caso não seja um POST, apenas exibe a página de confirmação
    return render(request, 'confirmar_reserva.html', {
        'campo': campo,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'duracao': round(duracao, 2),  # Arredonda para 2 casas decimais
        'valor_total': round(valor_total, 2)
    })

@login_required
def historico_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-data_inicio')
    return render(request, 'historico_reservas.html', {'reservas': reservas})

@login_required
def detalhes_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'detalhes_reserva.html', {'reserva': reserva})

@login_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        # Atualiza as datas de início e fim
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        pagamento = request.POST.get('pagamento')

        # Se os dados de data ou pagamento não forem fornecidos, exibe erro
        if not data_inicio or not data_fim or not pagamento:
            messages.error(request, "Data de início, data de fim e forma de pagamento são obrigatórios.")
            return render(request, 'editar_reserva.html', {'reserva': reserva})

        try:
            # Converte as datas de string para datetime
            data_inicio = datetime.strptime(data_inicio, "%Y-%m-%dT%H:%M")
            data_fim = datetime.strptime(data_fim, "%Y-%m-%dT%H:%M")

            # Verifica se já existe uma reserva no mesmo campo, nas mesmas datas
            if Reserva.objects.filter(campo=reserva.campo, data_inicio__lte=data_fim, data_fim__gte=data_inicio).exclude(id=reserva.id).exists():
                messages.error(request, "Este campo já está reservado para esse horário. Tente outro horário.")
                return render(request, 'editar_reserva.html', {'reserva': reserva})

            reserva.data_inicio = data_inicio
            reserva.data_fim = data_fim
            reserva.pagamento = pagamento  # Atualiza a forma de pagamento
            reserva.save()

            messages.success(request, "Reserva editada com sucesso!")
            return redirect('detalhes_reserva', reserva_id=reserva.id)
        except ValueError:
            messages.error(request, "Erro ao processar as datas.")
        
    return render(request, 'editar_reserva.html', {'reserva': reserva})

@login_required
def confirmar_cancelamento(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    return render(request, 'confirmar_cancelamento.html', {'campo': campo})

@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reserva cancelada com sucesso!")
        return redirect('historico_reservas')

    return render(request, 'confirmar_cancelamento.html', {'reserva': reserva})

@login_required
def cancelamento_confirmado(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    return render(request, 'cancelamento_confirmado.html', {'campo': campo})

@user_passes_test(is_admin)
def editar_campo(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    if request.method == 'POST':
        form = ReservaCampoForm(request.POST, instance=campo)
        if form.is_valid():
            form.save()
            messages.success(request, f"O campo '{campo.nome}' foi atualizado com sucesso.")
            return redirect('index')
    else:
        form = ReservaCampoForm(instance=campo)
    return render(request, 'editar_campo.html', {'form': form, 'campo': campo})

@user_passes_test(is_admin)
def excluir_campo(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    if request.method == 'POST':
        campo.delete()
        messages.success(request, f"O campo '{campo.nome}' foi excluído com sucesso.")
        return redirect('index')
    return render(request, 'confirmar_exclusao.html', {'campo': campo})

@login_required
def perfil(request):
    perfil = request.user.perfil
    campos_reservados = Campo.objects.filter(reserva__usuario=request.user)
    return render(request, 'perfil.html', {'perfil': perfil, 'campos_reservados': campos_reservados})

@login_required
def editar_perfil(request):
    perfil = Perfil.objects.get(user=request.user)
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=perfil)
    return render(request, 'editar_perfil.html', {'form': form})

def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso! Faça login para continuar.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'cadastro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next', '/')  # Se não houver 'next', redireciona para a página inicial
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
