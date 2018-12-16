set -e

docker run \
    --name cc_golf_db \
    --env-file .env -d \
    --volume "$(pwd)/pgdata":/var/lib/postgresql/data \
    -it --rm \
    --link cc_golf_db:postgres
    postgres psql 
