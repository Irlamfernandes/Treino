from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projetoapp.urls')),  # Direciona para as URLs do app campos
]