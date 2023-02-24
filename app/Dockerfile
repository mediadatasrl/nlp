# syntax=docker/dockerfile:1.4
#FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder
FROM python:3.11-bullseye AS builder


RUN apt-get update
RUN apt-get -y install git gcc

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

#installo i modelli di spacy
RUN python -m spacy download it_core_news_lg

COPY . /app

ENTRYPOINT ["python3"]
CMD ["app.py"]

FROM builder as dev-envs

#RUN <<EOF
#apk update
#apk add git
#EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
