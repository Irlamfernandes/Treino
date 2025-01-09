#!/bin/sh

# O comando "set -e" faz com que o script pare imediatamente se qualquer comando falhar
set -e

# O script espera que o banco de dados PostgreSQL esteja pronto antes de executar os outros scripts
wait_psql.sh

# Executa a coleta dos arquivos estáticos
collectstatic.sh

# Executa as migrações do banco de dados
migrate.sh

# Inicia o servidor Django
runserver.sh
