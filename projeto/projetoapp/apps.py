from django.apps import AppConfig

class ProjetoappConfig(AppConfig):
    # Define o tipo padrão de campo automático para os modelos
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nome do aplicativo
    name = 'projetoapp'

    # Método chamado quando o aplicativo é inicializado
    def ready(self):
        # Importação dos sinais para conectar funções aos eventos do Django
        import projetoapp.signals
