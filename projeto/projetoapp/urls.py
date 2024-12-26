from django.urls import path
from projetoapp.views import LoginView, SignupView  # Importa as classes corrigidas

urlpatterns = [
    path('', LoginView.as_view(), name='login'),  # Usa LoginView ao invés de login
    path('signup/', SignupView.as_view(), name='signup'),  # Usa SignupView ao invés de signup
]
