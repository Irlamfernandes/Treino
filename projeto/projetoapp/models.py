from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from decimal import Decimal

class Campo(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    disponivel = models.BooleanField(default=True)
    data_reserva = models.DateTimeField(null=True, blank=True)
    preco_por_hora = models.DecimalField(max_digits=100, decimal_places=2)
    localizacao = models.CharField(max_length=255, blank=True, null=True)
    capacidade = models.IntegerField(default=0)
    tipo_gramado = models.CharField(max_length=100, choices=[('sintetico', 'Sintético'), ('natural', 'Natural')], default='sintetico')
    iluminacao = models.BooleanField(default=False)
    cidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        unique_together = ('nome', 'cidade')

    def calcular_valor_total(self, data_inicio, data_fim):
        # Calculando o número de horas de reserva
        delta = data_fim - data_inicio
        horas_reserva = delta.total_seconds() / 3600  # Converte a diferença para horas
        
        # Calculando o valor total da reserva
        valor_total = Decimal(horas_reserva) * self.preco_por_hora
        return valor_total

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    foto = models.ImageField(upload_to='perfil_fotos/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('email',)

class Reserva(models.Model):
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_inicio = models.DateTimeField(null=True)
    data_fim = models.DateTimeField(null=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    pagamento = models.CharField(max_length=100, choices=[
        ('credito', 'Cartão de Crédito'),
        ('debito', 'Cartão de Débito'),
        ('pix', 'Pix'),
    ], default='credito')
    
    def __str__(self):
        return f"Reserva de {self.campo.nome} por {self.usuario.username}"

    class Meta:
        unique_together = ('campo', 'data_inicio', 'data_fim')
