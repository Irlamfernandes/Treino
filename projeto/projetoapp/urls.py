from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reservar/<int:campo_id>/', views.reservar, name='reservar'),
    path('cancelar/<int:campo_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('confirmar-cancelamento/<int:campo_id>/', views.confirmar_cancelamento, name='confirmar_cancelamento'),
    path('editar/<int:campo_id>/', views.editar_campo, name='editar_campo'),  # Nova URL para editar
    path('excluir/<int:campo_id>/', views.excluir_campo, name='excluir_campo'),  # Nova URL para excluir
]
