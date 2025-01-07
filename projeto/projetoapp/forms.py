from django import forms
from .models import Campo, Perfil

class ReservaCampoForm(forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['nome', 'descricao', 'preco_por_hora', 'localizacao', 'capacidade']
        labels = {
            'nome': 'Nome do Campo',
            'descricao': 'Descrição',
            'preco_por_hora': 'Preço por Hora',
            'localizacao': 'Localização',
            'capacidade': 'Capacidade',
        }

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefone', 'cidade']
