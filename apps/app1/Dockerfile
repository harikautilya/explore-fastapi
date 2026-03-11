# Stage 1 - Build the image and export dependencies
FROM alpine AS build

RUN apk update && apk add python3 curl

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH" 

COPY ./pyproject.toml /app/pyproject.toml
COPY ./apps/app1/ /app/apps/app1
COPY ./packages /app/packages

WORKDIR /app
RUN uv export --format requirements-txt --no-editable --output-file requirements.txt --package app1
RUN uv venv
RUN uv pip install -r requirements.txt

# RUN /app/venv/bin/pip install --upgrade pip
# RUN /app/venv/bin/pip install -r requirements.txt

# # Stage 3 - Create the final image and copy the virtual environment
# FROM alpine

# RUN apk update && apk add python3 

# COPY --from=build /app/venv /app/venv

# WORKDIR /app

# ENV PATH="/app/venv/bin:$PATH"

# COPY ./apps/app1/src /app/src

CMD ["uv" ,"run"  ,"python" ,"-m" ,"app1.main"]
