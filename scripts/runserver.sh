#!/bin/sh
# Este script inicia o servidor Django, permitindo que o app seja acessado externamente
# O parâmetro 0.0.0.0:8000 configura o servidor para aceitar conexões de qualquer endereço IP na porta 8000
python manage.py runserver 0.0.0.0:8000
