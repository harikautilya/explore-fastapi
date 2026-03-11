FROM alpine:latest

RUN apk update && apk add python3 curl docker

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH" 

WORKDIR /workspaces/explore-fastapi
