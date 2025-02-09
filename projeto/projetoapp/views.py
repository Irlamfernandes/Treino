from django.shortcuts import render, get_object_or_404, redirect
from .models import Campo, Reserva, Perfil
from .forms import ReservaCampoForm, EditarPerfilForm, EditarCampoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.db.models import Q
import logging
from django.http import HttpResponse
from datetime import timedelta, datetime
from decimal import Decimal

# Configuração do logger para registrar eventos
logger = logging.getLogger(__name__)

# Função de visualização da página inicial com filtro de campos
def index(request):
    campos = Campo.objects.all()
    
    # Filtrar por cidade
    cidade = request.GET.get('cidade')
    if cidade:
        campos = campos.filter(cidade__icontains=cidade)
    
    # Filtrar por tipo de gramado
    tipo_gramado = request.GET.get('tipo_gramado')
    if tipo_gramado:
        campos = campos.filter(tipo_gramado=tipo_gramado)
    
    # Filtrar por iluminação
    iluminacao = request.GET.get('iluminacao')
    if iluminacao == 'true':
        campos = campos.filter(iluminacao=True)
    
    return render(request, 'index.html', {'campos': campos})

# Função para verificar se o usuário é administrador
def is_admin(user):
    return user.is_superuser

# Detalhes do campo e confirmação de reserva
@login_required(login_url='/login/')
def detalhes_campo(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)

    # Verificação se o formulário de reserva foi enviado
    if request.method == 'POST':
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')

        if not data_inicio or not data_fim:
            messages.error(request, "Data de início e fim são obrigatórios.")
            return render(request, 'detalhes_campo.html', {'campo': campo})

        # Conversão das datas para datetime
        try:
            data_inicio = datetime.strptime(data_inicio, "%Y-%m-%dT%H:%M")
            data_fim = datetime.strptime(data_fim, "%Y-%m-%dT%H:%M")
            
            # Verificação se o campo já está reservado no horário desejado
            if Reserva.objects.filter(campo=campo, data_inicio__lte=data_fim, data_fim__gte=data_inicio).exists():
                messages.error(request, "Este campo já está reservado para esse horário. Tente outro horário.")
                return render(request, 'detalhes_campo.html', {'campo': campo, 'data_inicio': data_inicio, 'data_fim': data_fim})

            # Redireciona para a página de confirmação de reserva
            data_inicio_str = data_inicio.strftime("%Y-%m-%dT%H:%M")
            data_fim_str = data_fim.strftime("%Y-%m-%dT%H:%M")
            return redirect('confirmar_reserva', campo_id=campo.id, inicio=data_inicio_str, fim=data_fim_str)

        except ValueError:
            messages.error(request, "Erro ao processar as datas.")
            return render(request, 'detalhes_campo.html', {'campo': campo})

    return render(request, 'detalhes_campo.html', {'campo': campo})

# Função de confirmação da reserva
@login_required(login_url='/login/')
def confirmar_reserva(request, campo_id, inicio, fim):
    try:
        data_inicio = datetime.strptime(inicio, "%Y-%m-%dT%H:%M")
        data_fim = datetime.strptime(fim, "%Y-%m-%dT%H:%M")
    except ValueError:
        messages.error(request, "Formato de data inválido.")
        return redirect('home')

    campo = get_object_or_404(Campo, id=campo_id)
    
    # Validação: data_inicio não pode ser no passado
    if data_inicio < datetime.now():
        messages.error(request, "A data de início não pode ser no passado.")
        return render(request, 'detalhes_campo.html', {'campo': campo})

    # Validação: data_inicio deve ser anterior à data_fim
    if data_inicio >= data_fim:
        messages.error(request, "A data de início deve ser anterior à data de fim.")
        return render(request, 'detalhes_campo.html', {'campo': campo})

    # Cálculo do valor utilizando o método do modelo
    valor_total = campo.calcular_valor_total(data_inicio, data_fim)
    
    duracao = data_fim - data_inicio
    horas = duracao.seconds // 3600  # horas
    minutos = (duracao.seconds // 60) % 60  # minutos

    duracao_formatada = f"Duração: {horas:02} horas e {minutos:02} minutos" 

    if request.method == "POST":
        pagamento = request.POST.get('pagamento')  # Captura o pagamento selecionado

        # Criação da reserva
        reserva = Reserva.objects.create(
            campo=campo,
            usuario=request.user,
            data_inicio=data_inicio,
            data_fim=data_fim,
            valor_total=valor_total,
            pagamento=pagamento  # Armazena o método de pagamento
        )
        
        # Mensagem de sucesso
        messages.success(request, f"Reserva confirmada! Valor total: R$ {round(valor_total, 2)}.")
        return redirect('index')  # Redireciona para a página inicial
    
    return render(request, 'confirmar_reserva.html', {
        'campo': campo,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'valor_total': round(valor_total, 2),
        'duracao_formatada': duracao_formatada,  # Adicionando a duração formatada
    })

# Histórico de reservas do usuário
@login_required
def historico_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-data_inicio')
    return render(request, 'historico_reservas.html', {'reservas': reservas})

# Detalhes da reserva
@login_required
def detalhes_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'detalhes_reserva.html', {'reserva': reserva})

# Edição de reserva
@login_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    if request.method == 'POST':
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        pagamento = request.POST.get('pagamento')

        if not data_inicio or not data_fim or not pagamento:
            messages.error(request, "Data de início, data de fim e forma de pagamento são obrigatórios.")
            return render(request, 'editar_reserva.html', {'reserva': reserva})

        try:
            data_inicio = datetime.strptime(data_inicio, "%Y-%m-%dT%H:%M")
            data_fim = datetime.strptime(data_fim, "%Y-%m-%dT%H:%M")

            if Reserva.objects.filter(campo=reserva.campo, data_inicio__lte=data_fim, data_fim__gte=data_inicio).exclude(id=reserva.id).exists():
                messages.error(request, "Este campo já está reservado para esse horário. Tente outro horário.")
                return render(request, 'editar_reserva.html', {'reserva': reserva})

            reserva.data_inicio = data_inicio
            reserva.data_fim = data_fim
            reserva.pagamento = pagamento
            reserva.save()

            messages.success(request, "Reserva editada com sucesso!")
            return redirect('detalhes_reserva', reserva_id=reserva.id)
        except ValueError:
            messages.error(request, "Erro ao processar as datas.")
        
    return render(request, 'editar_reserva.html', {'reserva': reserva})

# Confirmação de cancelamento da reserva
@login_required
def confirmar_cancelamento(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    return render(request, 'confirmar_cancelamento.html', {'campo': campo})

# Cancelamento de reserva
@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)    
    reserva.delete()
    messages.success(request, "Reserva cancelada com sucesso.")
    return redirect('historico_reservas')

# Confirmação de cancelamento com sucesso
@login_required
def cancelamento_confirmado(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    return render(request, 'cancelamento_confirmado.html', {'campo': campo})

# Função para editar campos (somente para administradores)
@user_passes_test(is_admin)
def editar_campo(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    if request.method == 'POST':
        form = EditarCampoForm(request.POST, instance=campo)
        if form.is_valid():
            form.save()
            messages.success(request, f"O campo '{campo.nome}' foi atualizado com sucesso.")
            return redirect('index')
    else:
        form = EditarCampoForm(instance=campo)
    return render(request, 'editar_campo.html', {'form': form, 'campo': campo})

# Função para excluir campos (somente para administradores)
@user_passes_test(is_admin)
def excluir_campo(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    
    # Verifica se há reservas associadas ao campo
    if Reserva.objects.filter(campo=campo).exists():
        messages.error(request, "Este campo não pode ser excluído porque possui reservas.")
        return redirect('index')
    
    campo.delete()
    messages.success(request, "Campo excluído com sucesso.")
    return redirect('index')

# Função de visualização do perfil do usuário
@login_required
def perfil(request):
    perfil = request.user.perfil
    campos_reservados = Campo.objects.filter(reserva__usuario=request.user)
    return render(request, 'perfil.html', {'perfil': perfil, 'campos_reservados': campos_reservados})

# Edição do perfil do usuário
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

# Função de cadastro de novo usuário
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

# Função de login do usuário
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
