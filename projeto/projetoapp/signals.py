from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Perfil

# Função para criar automaticamente um perfil quando um novo usuário é criado
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Verifica se o usuário foi criado
        Perfil.objects.create(user=instance)  # Cria um perfil para o usuário

# Função para salvar automaticamente o perfil quando o usuário é salvo
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfil.save()  # Salva o perfil relacionado ao usuário
