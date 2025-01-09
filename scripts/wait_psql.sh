#!/bin/sh
# Este script aguarda até que o banco de dados PostgreSQL esteja pronto para aceitar conexões
# O comando "nc -z" verifica se a porta do PostgreSQL está aberta

# O loop verifica se o PostgreSQL está pronto a cada 2 segundos até que a conexão seja bem-sucedida
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Aguardando a inicialização do banco de dados Postgres ($POSTGRES_HOST:$POSTGRES_PORT) ..."
  sleep 2
done

# Uma vez que o banco de dados esteja pronto, uma mensagem de sucesso é exibida
echo "✅ Banco de dados Postgres iniciado com sucesso ($POSTGRES_HOST:$POSTGRES_PORT)"
