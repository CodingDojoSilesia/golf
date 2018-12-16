#!/bin/bash
set -e
source .env
docker run \
    -it --rm \
    --link cc_golf_db:db \
	-e PGHOST=db \
	-e PGDATABASE=$POSTGRES_DB \
	-e PGUSER=$POSTGRES_USER \
	-e PGPASSWORD=$POSTGRES_PASSWORD \
    postgres psql
