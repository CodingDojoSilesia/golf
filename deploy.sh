set -e
docker build . -t cc_golf_app
if [ ! "$(docker ps -a | grep cc_golf_db)" ] ; then
    set +e
    docker volume create cc_golf_pgdata
    set -e
    docker run \
        --name cc_golf_db \
        --env-file .env -d \
        --volume cc_golf_pgdata:/var/lib/postgresql/data \
        --restart unless-stopped \
        postgres
fi

docker run \
    --name cc_golf_app_install \
    --rm -it --env-file .env \
    --link cc_golf_db:db \
    cc_golf_app python3 install.py

set +e
docker stop cc_golf_app
docker rm cc_golf_app
set -e

docker run \
    --name cc_golf_app \
    -dit --env-file .env \
    -p 5111:5000 \
    --link cc_golf_db:db \
    --privileged \
    cc_golf_app

