#!/bin/bash
set -e
source .env
docker-compose run \
    --rm \
	-e PGHOST=db \
	-e PGDATABASE=$POSTGRES_DB \
	-e PGUSER=$POSTGRES_USER \
	-e PGPASSWORD=$POSTGRES_PASSWORD \
    db psql
