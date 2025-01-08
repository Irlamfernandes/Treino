from django import forms
from .models import Campo, Reserva, Perfil
from django.db.models import Q

class ReservaCampoForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['data_inicio', 'data_fim']
        labels = {
            'data_inicio': 'Data e Hora de Início',
            'data_fim': 'Data e Hora de Fim',
        }

    def __init__(self, *args, **kwargs):
        campo = kwargs.pop('campo', None)  # Recebe o campo passado na view
        super().__init__(*args, **kwargs)
        self.campo = campo  # Atribui o campo à instância
        self.fields['data_inicio'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        self.fields['data_fim'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')

        if data_inicio and data_fim:
            # Verifica se há reservas conflitantes
            reservas_existentes = Reserva.objects.filter(campo=self.campo).filter(
                Q(data_inicio__lt=data_fim) & Q(data_fim__gt=data_inicio)
            )
            if reservas_existentes.exists():
                raise forms.ValidationError('O campo já está reservado para este horário.')

        return cleaned_data


class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefone', 'email', 'foto']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verificando se o email já está sendo usado por outro usuário
        if email and Perfil.objects.filter(email=email).exclude(user=self.instance.user).exists():
            raise forms.ValidationError('Este email já está em uso por outro usuário.')
        return email
