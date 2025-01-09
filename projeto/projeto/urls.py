from django.contrib import admin
from django.urls import path, include

# Definição das URLs principais do projeto
urlpatterns = [
    # Rota para a interface de administração do Django
    path('admin/', admin.site.urls),
    
    # Inclui as URLs do aplicativo 'projetoapp'
    path('', include('projetoapp.urls')),  # A rota principal direciona para o app 'projetoapp'
]
