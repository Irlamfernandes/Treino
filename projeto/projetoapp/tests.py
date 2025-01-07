from django.test import TestCase
from .models import Campo

class CampoModelTest(TestCase):

    def setUp(self):
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
        self.assertEqual(self.campo.nome, 'Campo de Futebol')
        self.assertTrue(self.campo.disponivel)
        self.assertEqual(self.campo.tipo_gramado, 'sintetico')
        self.assertTrue(self.campo.iluminacao)


from django.urls import reverse

class ReservaViewTest(TestCase):

    def setUp(self):
        self.campo = Campo.objects.create(
            nome='Campo de Futebol',
            descricao='Campo para jogos de futebol',
            disponivel=True
        )
    
    def test_reservar_campo(self):
        response = self.client.post(reverse('reservar', args=[self.campo.id]))
        self.campo.refresh_from_db()
        self.assertFalse(self.campo.disponivel)
        self.assertEqual(response.status_code, 302)  # Redireciona após reservar

from django.contrib.auth.models import User

class PerfilViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_perfil_view(self):
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
