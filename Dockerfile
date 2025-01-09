# Utiliza a imagem base do Python 3.11.3 com a versão do Alpine 3.18
FROM python:3.11.3-alpine3.18

# Informações do mantenedor da imagem
LABEL maintainer="luizomf@gmail.com"  

# Variável de ambiente para evitar a criação de arquivos .pyc (bytecode) no disco
# Definir como 1 significa que o Python não escreverá arquivos de bytecode no disco.
ENV PYTHONDONTWRITEBYTECODE 1

# Variável de ambiente para desativar o buffer de saída do Python
# Definir como 1 permite que os outputs do Python sejam exibidos imediatamente no console.
ENV PYTHONUNBUFFERED 1

# Copia a pasta "projeto" e "scripts" para dentro do container
# Copia o diretório "projeto" para o container
COPY projeto /projeto
# Copia o diretório "scripts" para o container 
COPY scripts /scripts  

# Define o diretório de trabalho para /projeto dentro do container
WORKDIR /projeto

# Expõe a porta 8000 do container para que o Django possa ser acessado externamente
EXPOSE 8000

# Comando RUN para configurar o ambiente Python e instalar dependências
# - Cria um ambiente virtual em /venv
# - Instala o pip mais recente dentro do ambiente virtual
# - Instala as dependências listadas no arquivo requirements.txt
# - Cria o usuário duser, sem senha, sem diretório home
# - Cria os diretórios para arquivos estáticos e de mídia, e define permissões adequadas
# - Torna os diretórios estáticos e de mídia acessíveis ao usuário duser
# - Concede permissões para o diretório /scripts, permitindo execução dos scripts
RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /projeto/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chown -R duser:duser /data/web/media && \
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media && \
  chmod -R +x /scripts  # Ajusta permissões e prepara o ambiente

# Adiciona os diretórios /scripts e /venv/bin ao PATH do container,
# permitindo que os scripts e o ambiente virtual sejam executados diretamente.
ENV PATH="/scripts:/venv/bin:$PATH"

# Muda para o usuário duser (para evitar rodar como root no container)
USER duser

# Executa o script "commands.sh" localizado no diretório /scripts dentro do container
CMD ["commands.sh"]
