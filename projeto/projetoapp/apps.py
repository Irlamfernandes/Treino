from django.apps import AppConfig

class ProjetoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projetoapp'

    def ready(self):
        import projetoapp.signals  # Importa os sinais ao iniciar o app
