# install & run

```bash
cp example_env .env
vim .env
docker-compose up -d db
docker-compose up -d --build app
# done!
```

# dev version (with autoreload)

```bash
docker-compose up -d db
docker-compose -f docker-compose.dev.yml up app
```

# updating server
docker-compose stop app && docker-compose up --build -d app
