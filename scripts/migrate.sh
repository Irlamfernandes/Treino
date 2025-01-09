#!/bin/sh
# Primeiro, executa o script "makemigrations.sh" para gerar as migrações, se necessário
./makemigrations.sh

# Após gerar as migrações, executa o comando para aplicar as migrações ao banco de dados
echo 'Executando migrate.sh'
python manage.py migrate --noinput
