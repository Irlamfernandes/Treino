from django.shortcuts import render, get_object_or_404, redirect
from .models import Campo
from .forms import ReservaCampoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
import logging

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
def reservar(request, campo_id):
    logger.info(f"Acessou a função de reserva para o campo ID: {campo_id}")
    
    campo = get_object_or_404(Campo, id=campo_id)
    
    if not campo.disponivel:
        logger.warning(f"Campo '{campo.nome}' não disponível para reserva.")
        messages.error(request, "Este campo já está reservado.")
        return redirect('index')
    
    if request.method == 'POST':
        campo.disponivel = False
        campo.data_reserva = request.POST.get('data_reserva')
        campo.save()
        logger.info(f"Campo '{campo.nome}' reservado com sucesso para {campo.data_reserva}.")
        messages.success(request, f"O campo '{campo.nome}' foi reservado com sucesso para {campo.data_reserva}.")
        return redirect('detalhes_reserva', campo_id=campo.id)

    return render(request, 'reservar.html', {'campo': campo})

@login_required
def detalhes_reserva(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    return render(request, 'detalhes_reserva.html', {'campo': campo})

@login_required
def historico_reservas(request):
    campos_reservados = Campo.objects.filter(disponivel=False)
    return render(request, 'historico_reservas.html', {'campos_reservados': campos_reservados})

@login_required
def confirmar_cancelamento(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    return render(request, 'confirmar_cancelamento.html', {'campo': campo})

@login_required
def cancelar_reserva(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    
    if campo.disponivel:
        messages.error(request, f"O campo '{campo.nome}' não está reservado para cancelamento.")
        return redirect('index')
    
    if request.method == "POST":
        campo.disponivel = True
        campo.data_reserva = None
        campo.save()
        messages.info(request, f"A reserva do campo '{campo.nome}' foi cancelada com sucesso.")
        return redirect('cancelamento_confirmado', campo_id=campo.id)
    
    return render(request, 'confirmar_cancelamento.html', {'campo': campo})

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
    perfil = request.user.perfil
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso.')
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
