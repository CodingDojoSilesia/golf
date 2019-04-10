#!/bin/bash
set -e
source .env
docker-compose run db \
    --rm \
	-e PGHOST=db \
	-e PGDATABASE=$POSTGRES_DB \
	-e PGUSER=$POSTGRES_USER \
	-e PGPASSWORD=$POSTGRES_PASSWORD \
    postgres psql
