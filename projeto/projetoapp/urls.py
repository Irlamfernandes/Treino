from django.urls import path
from projetoapp import views

urlpatterns = [
    path('', views.pesquisa_campos, name='pesquisa_campos'),  # Exibe os campos
    path('reservar/<int:id>/', views.reservar_campo, name='reservar_campo'),  # Reserva de campo
    path('gerenciar/', views.gerenciar_campos, name='gerenciar_campos'),  # Gerenciar campos
]
