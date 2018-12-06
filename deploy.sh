docker build . -t cc_golf_app
if [ ! "$(docker ps -a | grep cc_golf_db)" ] ; then
    docker volume create pgdata
    docker run \
        --name cc_golf_db \
        --env-file .env -d \
        --volume pgdata:/var/lib/postgresql/data
        --restart unless-stopped \
        postgres
fi
docker run \
    --name cc_golf_app_install \
    --rm -it --env-file .env \
    --link cc_golf_db:db \
    cc_golf_app python3 install.py

docker stop cc_golf_app
docker rm cc_golf_app
docker run \
    --name cc_golf_app \
    -dit --env-file .env \
    -p 5111:5000 \
    --memory 256m \
    --memory-swappiness 0 \
    --kernel-memory 300m \
    --cpus .5 \
    --cpu-shares 512 \
    --restart unless-stopped \
    --cap-add=NET_ADMIN \
    --ulimit nproc=80 \
    --pids-limit 64 \
    --link cc_golf_db:db \
    cc_golf_app

