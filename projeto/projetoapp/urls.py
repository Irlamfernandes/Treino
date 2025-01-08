from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', views.index, name='index'),
    path('campo/<int:campo_id>/', views.detalhes_campo, name='detalhes_campo'),
    path('confirmar_reserva/<int:campo_id>/<str:inicio>/<str:fim>/', views.confirmar_reserva, name='confirmar_reserva'),
    
    path('editar/<int:campo_id>/', views.editar_campo, name='editar_campo'),
    path('excluir/<int:campo_id>/', views.excluir_campo, name='excluir_campo'),

    path('perfil/', views.perfil, name='perfil'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('historico_reservas/', views.historico_reservas, name='historico_reservas'),
    path('detalhes_reserva/<int:reserva_id>/', views.detalhes_reserva, name='detalhes_reserva'),
    path('editar_reserva/<int:reserva_id>/', views.editar_reserva, name='editar_reserva'),
    path('cancelar_reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    
    path('confirmar-cancelamento/<int:campo_id>/', views.confirmar_cancelamento, name='confirmar_cancelamento'),
    path('cancelamento-confirmado/<int:campo_id>/', views.cancelamento_confirmado, name='cancelamento_confirmado'),
]
