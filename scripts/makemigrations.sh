#!/bin/sh
# Este script cria as migrações para o banco de dados com base nas mudanças nos modelos Django
echo 'Executando makemigrations.sh'
python manage.py makemigrations --noinput
