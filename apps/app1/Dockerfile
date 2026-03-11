# Stage 1 - Build the image and export dependencies
FROM alpine AS build

RUN apk update && apk add python3 curl

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH" 

COPY ./pyproject.toml /app/pyproject.toml
COPY ./uv.lock /app/uv.lock
COPY ./apps/app1/ /app/apps/app1
COPY ./packages /app/packages

WORKDIR /app
RUN uv venv
RUN uv sync --frozen --no-editable --no-dev --package app1


# Stage 3 - Create the final image and copy the virtual environment
FROM alpine

RUN apk update && apk add python3 

COPY --from=build /app/.venv /app/.venv

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"


COPY ./apps/app1/alembic.ini /app/alembic.ini
COPY ./apps/app1/alembic /app/alembic

RUN /app/.venv/bin/alembic upgrade head
RUN rm -rf /app/alembic
RUN rm -rf /app/alembic.ini

CMD ["python" ,"-m" ,"app1.main"]
