#!/bin/bash
set -e

until psql "postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@:5432" -c '\q'; do
  >&2 echo "Postgres is unavailable - waiting..."
  sleep 1
done

psql -v ON_ERROR_STOP=1 "postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@:5432" <<-EOSQL
  DROP DATABASE IF EXISTS pr_fhir;
  DROP USER IF EXISTS dev;
  CREATE USER dev WITH PASSWORD 'dev';
  CREATE DATABASE pr_fhir;
  GRANT ALL PRIVILEGES ON DATABASE pr_fhir TO dev;
EOSQL

# psql -v ON_ERROR_STOP=1 "postgresql://$POSTGRES_USER@:5432/pr-fhir" <<-EOSQL
#   CREATE EXTENSION IF NOT EXISTS pgcrypto;
#   SELECT gen_random_uuid();
# EOSQL
