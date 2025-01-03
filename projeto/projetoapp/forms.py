from django import forms
from .models import Campo

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
