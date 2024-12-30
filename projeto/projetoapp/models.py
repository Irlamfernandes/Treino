from django.db import models

class Campo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(null=True, blank=True)  # Permitir valor nulo
    localizacao = models.CharField(max_length=200)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
