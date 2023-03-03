# nlp


per installare da macchine di sviluppo (Docker Desktop): 

```sh
docker-compose build
docker-compose up -d
```

Sul server invece

```sh
DOCKER_BUILDKIT=1 docker compose build
DOCKER_BUILDKIT=1 docker compose up -d
```

