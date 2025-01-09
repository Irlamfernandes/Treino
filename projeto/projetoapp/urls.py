from django.urls import path
from . import views  # Importa as views do seu aplicativo
from django.contrib.auth import views as auth_views  # Importa as views de autenticação do Django

urlpatterns = [
    # Rota para a página de cadastro do usuário
    path('cadastro/', views.cadastro, name='cadastro'),

    # Rota para a página de login, usando a view padrão de login do Django
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # Rota para a página de logout, usando a view padrão de logout do Django
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Rota para a página inicial do site (index)
    path('', views.index, name='index'),

    # Rota para exibir os detalhes de um campo específico (campo_id é o identificador do campo)
    path('campo/<int:campo_id>/', views.detalhes_campo, name='detalhes_campo'),

    # Rota para confirmar a reserva de um campo, passando o ID do campo e as datas de início e fim
    path('confirmar_reserva/<int:campo_id>/<str:inicio>/<str:fim>/', views.confirmar_reserva, name='confirmar_reserva'),

    # Rota para editar um campo específico (campo_id é o identificador do campo)
    path('editar/<int:campo_id>/', views.editar_campo, name='editar_campo'),

    # Rota para excluir um campo específico (campo_id é o identificador do campo)
    path('excluir/<int:campo_id>/', views.excluir_campo, name='excluir_campo'),

    # Rota para exibir o perfil do usuário
    path('perfil/', views.perfil, name='perfil'),

    # Rota para editar o perfil do usuário
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),

    # Rota para exibir o histórico de reservas do usuário
    path('historico_reservas/', views.historico_reservas, name='historico_reservas'),

    # Rota para exibir os detalhes de uma reserva específica (reserva_id é o identificador da reserva)
    path('detalhes_reserva/<int:reserva_id>/', views.detalhes_reserva, name='detalhes_reserva'),

    # Rota para editar uma reserva específica (reserva_id é o identificador da reserva)
    path('editar_reserva/<int:reserva_id>/', views.editar_reserva, name='editar_reserva'),

    # Rota para cancelar uma reserva específica (reserva_id é o identificador da reserva)
    path('cancelar_reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),

    # Rota para confirmar o cancelamento de uma reserva (campo_id é o identificador do campo)
    path('confirmar-cancelamento/<int:campo_id>/', views.confirmar_cancelamento, name='confirmar_cancelamento'),

    # Rota para exibir a confirmação do cancelamento de uma reserva
    path('cancelamento-confirmado/<int:campo_id>/', views.cancelamento_confirmado, name='cancelamento_confirmado'),
]
