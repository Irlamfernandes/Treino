#!/bin/sh
# Este script coleta os arquivos estáticos do Django e os coloca no diretório correto
# O parâmetro --noinput impede que o Django solicite qualquer interação do usuário durante o processo
python manage.py collectstatic --noinput
