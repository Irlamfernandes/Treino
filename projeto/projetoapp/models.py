from django.db import models
from django.contrib.auth.models import User

class Campo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    disponivel = models.BooleanField(default=True)
    data_reserva = models.DateTimeField(null=True, blank=True)
    preco_por_hora = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    localizacao = models.CharField(max_length=255, blank=True, null=True)
    capacidade = models.IntegerField(default=0)
    tipo_gramado = models.CharField(max_length=100, choices=[
        ('sintetico', 'Sintético'),
        ('natural', 'Natural'),
    ], default='sintetico')
    iluminacao = models.BooleanField(default=False)
    cidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Reserva(models.Model):
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_reserva = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.usuario.username} no campo {self.campo.nome}"
