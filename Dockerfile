# syntax=docker/dockerfile:1.4
FROM python:3-alpine AS builder

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt
RUN pip3 install waitress

COPY . /app

ENTRYPOINT ["waitress-serve", "--port", "45678", "tpb_rss:app"]

FROM builder as dev-envs

RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /