import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import dj_database_url

# Caminhos base dentro do projeto, facilitando o uso de subdiretórios
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / 'data' / 'web'

# Carregar variáveis de ambiente do arquivo .env
load_dotenv(BASE_DIR.parent / 'dotenv_files' / '.env', override=True)

# Chave secreta do Django, importante manter em segredo em produção
SECRET_KEY = os.getenv('SECRET_KEY')

# Controle do modo de depuração (não utilizar em produção)
DEBUG = bool(int(os.getenv('DEBUG', 0)))

# Hosts permitidos para acessar a aplicação
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',') 
    if h.strip()
]

# Definição das aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplicativo do projeto
    'projetoapp',

    # Aplicativo Axes para segurança
    'axes',
]

# Middleware para manipulação de requisições e segurança
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middleware do Axes (deve ser o último da lista)
    'axes.middleware.AxesMiddleware',
]

# URLs de login e redirecionamento
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/perfil/'
LOGOUT_REDIRECT_URL = 'index'

# Configurações de logging para monitoramento e debugging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'projetoapp': {  # Substitua 'projetoapp' pelo nome correto do seu app
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Configuração das URLs principais do projeto
ROOT_URLCONF = 'projeto.urls'

# Configurações de templates para renderização de páginas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configurações do banco de dados, utilizando URL de conexão do .env
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', '')
    )
}

# Backends de autenticação
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Configurações de arquivos estáticos e de mídia
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'projetoapp' / 'static',  # Corrigido para o diretório correto do app 'projetoapp'
]
STATIC_ROOT = DATA_DIR / 'static'
# Outras configurações...


MEDIA_URL = '/media/'
MEDIA_ROOT = DATA_DIR / 'media'

# Configurações do Axes para controle de acessos
AXES_ENABLED = True
AXES_FAILURE_LIMIT = 30
AXES_COOLOFF_TIME = 0.1  # 1 Hora
AXES_RESET_ON_SUCCESS = True

# Desativa o Axes durante testes
if 'test' in sys.argv:
    AXES_ENABLED = False
