from django import forms
from .models import Campo, Reserva, Perfil

# Formulário para realizar uma reserva de campo
class ReservaCampoForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['data_inicio', 'data_fim', 'campo']
        labels = {
            'data_inicio': 'Data e Hora de Início',
            'data_fim': 'Data e Hora de Fim',
            'campo': 'Campo de Futebol',
        }


    def __init__(self, *args, **kwargs):
        campo = kwargs.pop('campo', None)
        super().__init__(*args, **kwargs)
        self.campo = campo
        self.fields['data_inicio'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['data_fim'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')

        if data_inicio and data_fim:
            reservas_existentes = Reserva.objects.filter(campo=self.campo).filter(
                Q(data_inicio__lt=data_fim) & Q(data_fim__gt=data_inicio)
            )
            if reservas_existentes.exists():
                raise forms.ValidationError('O campo já está reservado para este horário.')

        return cleaned_data

# Formulário para editar o perfil de um usuário
class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefone', 'email', 'foto']
        labels = {
            'telefone': 'Telefone',
            'email': 'Email',
            'foto': 'Foto de Perfil',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Perfil.objects.filter(email=email).exclude(user=self.instance.user).exists():
            raise forms.ValidationError('Este email já está em uso por outro usuário.')
        return email

# Formulário para editar as informações de um campo
class EditarCampoForm(forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['nome', 'descricao', 'capacidade', 'tipo_gramado', 'iluminacao', 'preco_por_hora', 'localizacao']
        labels = {
            'nome': 'Nome do Campo',
            'descricao': 'Descrição do Campo',
            'capacidade': 'Capacidade',
            'tipo_gramado': 'Tipo de Gramado',
            'iluminacao': 'Possui Iluminação',
            'preco_por_hora': 'Preço por Hora',
            'localizacao': 'Localização',
        }
