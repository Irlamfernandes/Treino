from django.db import models

class Campo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    disponivel = models.BooleanField(default=True)
    data_reserva = models.DateField(null=True, blank=True)  # Quando o campo foi reservado
    preco_por_hora = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Preço por hora
    localizacao = models.CharField(max_length=255, blank=True, null=True)  # Localização do campo
    capacidade = models.IntegerField(default=0)  # Quantas pessoas o campo comporta

    def __str__(self):
        return self.nome
