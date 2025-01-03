from django.shortcuts import render, get_object_or_404, redirect
from .models import Campo
from .forms import ReservaCampoForm
from django.contrib import messages

def index(request):
    filtro = request.GET.get('filtro', 'todos')  # Padrão: mostrar todos os campos
    if filtro == 'disponiveis':
        campos = Campo.objects.filter(disponivel=True)
    elif filtro == 'indisponiveis':
        campos = Campo.objects.filter(disponivel=False)
    else:
        campos = Campo.objects.all()
    
    return render(request, 'index.html', {'campos': campos, 'filtro': filtro})


def reservar(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    if campo.disponivel:
        campo.disponivel = False
        campo.save()
        # Mensagem de sucesso
        messages.success(request, f"O campo '{campo.nome}' foi reservado com sucesso.")
    else:
        # Mensagem de erro, caso o campo já esteja indisponível
        messages.error(request, f"O campo '{campo.nome}' já está indisponível.")
    return redirect('index')


    
# View para confirmação de cancelamento da reserva
def confirmar_cancelamento(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    return render(request, 'confirmar_cancelamento.html', {'campo': campo})

def cancelar_reserva(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    if campo.disponivel:
        # Mensagem de erro caso o campo não tenha reserva
        messages.error(request, f"O campo '{campo.nome}' não está reservado para cancelamento.")
        return redirect('index')
    
    if request.method == "POST":
        campo.disponivel = True
        campo.data_reserva = None  # Resetando a data da reserva
        campo.save()
        # Mensagem de sucesso após o cancelamento
        messages.info(request, f"A reserva do campo '{campo.nome}' foi cancelada com sucesso.")
        return redirect('index')
    
    return render(request, 'confirmar_cancelamento.html', {'campo': campo})

# Função para editar o campo
def editar_campo(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    if request.method == 'POST':
        form = ReservaCampoForm(request.POST, instance=campo)
        if form.is_valid():
            form.save()
            messages.success(request, f"As informações do campo '{campo.nome}' foram atualizadas com sucesso.")
            return redirect('index')
    else:
        form = ReservaCampoForm(instance=campo)
    return render(request, 'editar_campo.html', {'form': form, 'campo': campo})

# Função para excluir o campo
def excluir_campo(request, campo_id):
    campo = get_object_or_404(Campo, id=campo_id)
    if request.method == 'POST':
        campo.delete()
        messages.success(request, f"O campo '{campo.nome}' foi excluído com sucesso.")
        return redirect('index')
    return render(request, 'confirmar_exclusao.html', {'campo': campo})