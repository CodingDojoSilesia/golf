docker build . -t cc_golf_app
docker stop cc_golf_db cc_golf_app
docker run --name cc_golf_db --env-file .env -d postgres
docker run --rm -it --env-file .env --link db cc_golf_app python3 install.py
docker run \
    --name cc_golf_app \
    --rm -it \
    --env-file .env \
    -p 80:5000 \
    --tmpfs /code \
    --memory 256m \
    --cpus .5 \
    --restart unless-stopped \
    --privileged --cap-add=NET_ADMIN \
    --link db \
    cc_golf_app \

