from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from decimal import Decimal

# Modelo representando um campo de futebol
class Campo(models.Model):
    nome = models.CharField(max_length=255)  # Nome do campo
    descricao = models.TextField()  # Descrição do campo
    disponivel = models.BooleanField(default=True)  # Indica se o campo está disponível para reserva
    data_reserva = models.DateTimeField(null=True, blank=True)  # Data da última reserva
    preco_por_hora = models.DecimalField(max_digits=100, decimal_places=2)  # Preço por hora de uso
    localizacao = models.CharField(max_length=255, blank=True, null=True)  # Localização do campo
    capacidade = models.IntegerField(default=0)  # Capacidade de pessoas no campo
    tipo_gramado = models.CharField(
        max_length=100, 
        choices=[('sintetico', 'Sintético'), ('natural', 'Natural')], 
        default='sintetico'  # Tipo de gramado
    )
    iluminacao = models.BooleanField(default=False)  # Indica se o campo tem iluminação
    cidade = models.CharField(max_length=100, blank=True, null=True)  # Cidade onde o campo está localizado

    def __str__(self):
        return self.nome  # Representação do campo como string

    def calcular_valor_total(self, data_inicio, data_fim):
        duracao = (data_fim - data_inicio).total_seconds() / 3600  # Duração em horas
        return self.preco_por_hora * Decimal(duracao)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nome', 'cidade'], name='unique_nome_cidade')
        ]

# Modelo representando o perfil de um usuário
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relacionamento um-para-um com o modelo User
    telefone = models.CharField(max_length=15, blank=True, null=True)  # Telefone do usuário
    email = models.EmailField(blank=True, null=True)  # Email do usuário
    foto = models.ImageField(upload_to='perfil_fotos/', blank=True, null=True)  # Foto do perfil

    def __str__(self):
        return self.user.username  # Representação do perfil como string

    class Meta:
        unique_together = ('email',)  # Garantia de unicidade para o email

# Modelo representando uma reserva de campo
class Reserva(models.Model):
    campo = models.ForeignKey(Campo, on_delete=models.CASCADE)  # Campo reservado
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuário que fez a reserva
    data_inicio = models.DateTimeField(null=True)  # Data e hora de início da reserva
    data_fim = models.DateTimeField(null=True)  # Data e hora de fim da reserva
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Valor total da reserva
    pagamento = models.CharField(
        max_length=100, 
        choices=[
            ('credito', 'Cartão de Crédito'),
            ('debito', 'Cartão de Débito'),
            ('pix', 'Pix'),
            ('boleto', 'Boleto Bancário')
        ], 
        default='credito'  # Método de pagamento
    )

    def __str__(self):
        return f"Reserva de {self.campo.nome} por {self.usuario.username}"  # Representação da reserva como string

    class Meta:
        unique_together = ('campo', 'data_inicio', 'data_fim')  # Garantia de unicidade para campo, data de início e fim
