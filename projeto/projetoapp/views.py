from django.shortcuts import render, get_object_or_404, redirect
from .models import Campo

# Página de lista de campos
def pesquisa_campos(request):
    campos = Campo.objects.filter(disponivel=True)  # Exibe apenas campos disponíveis
    return render(request, 'pesquisa_campos.html', {'campos': campos})

# Função de reserva de campo
def reservar_campo(request, id):
    campo = get_object_or_404(Campo, id=id)
    campo.disponivel = False  # Marca o campo como reservado
    campo.save()
    return redirect('pesquisa_campos')  # Redireciona para a lista de campos

# Gerenciamento de campos (disponibilidade)
def gerenciar_campos(request):
    campos = Campo.objects.all()  # Exibe todos os campos, independentemente da disponibilidade
    return render(request, 'gerenciar_campos.html', {'campos': campos})
