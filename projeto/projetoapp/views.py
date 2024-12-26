from django.shortcuts import render
from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = 'account/login.html'  # Define o template diretamente

class SignupView(TemplateView):
    template_name = 'account/signup.html'  # Define o template diretamente
