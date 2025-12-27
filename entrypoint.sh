#!/bin/sh
set -e

echo "Aguardando banco de dados..."
until pg_isready -h db -p 5432 -U "$POSTGRES_USER"; do
  sleep 1
done


echo "Banco disponível"
exec "$@"