from django.test import TestCase
from .models import Campo
from django.urls import reverse
from django.contrib.auth.models import User

# Testes para o modelo Campo
class CampoModelTest(TestCase):

    def setUp(self):
        # Configuração inicial, criando um objeto Campo para ser usado nos testes
        self.campo = Campo.objects.create(
            nome='Campo de Futebol',
            descricao='Campo para jogos de futebol',
            disponivel=True,
            preco_por_hora=100.00,
            localizacao='São Paulo',
            capacidade=22,
            tipo_gramado='sintetico',
            iluminacao=True
        )

    def test_criar_campo(self):
        # Teste para verificar se o campo foi criado corretamente
        self.assertEqual(self.campo.nome, 'Campo de Futebol')
        self.assertTrue(self.campo.disponivel)
        self.assertEqual(self.campo.tipo_gramado, 'sintetico')
        self.assertTrue(self.campo.iluminacao)

# Testes para a view de reserva
class ReservaViewTest(TestCase):

    def setUp(self):
        # Configuração inicial, criando um campo para ser reservado
        self.campo = Campo.objects.create(
            nome='Campo de Futebol',
            descricao='Campo para jogos de futebol',
            disponivel=True
        )
    
    def test_reservar_campo(self):
        # Teste para verificar se a reserva de um campo altera a disponibilidade
        response = self.client.post(reverse('reservar', args=[self.campo.id]))
        self.campo.refresh_from_db()  # Atualiza o campo do banco de dados
        self.assertFalse(self.campo.disponivel)  # Campo deve estar indisponível após a reserva
        self.assertEqual(response.status_code, 302)  # Verifica se há redirecionamento após a reserva

# Testes para a view de perfil
class PerfilViewTest(TestCase):

    def setUp(self):
        # Configuração inicial, criando e autenticando um usuário
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_perfil_view(self):
        # Teste para verificar se a página de perfil exibe as informações do usuário corretamente
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 200)  # Verifica se a página carrega corretamente
        self.assertContains(response, 'testuser')  # Verifica se o nome de usuário está na resposta
