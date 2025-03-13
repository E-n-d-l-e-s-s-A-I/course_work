ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION:-3.11.9-slim}
ENV UV_COMPILE_BYTECODE=1

WORKDIR /src

COPY --from=ghcr.io/astral-sh/uv:0.5.0 /uv /uvx /bin/

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY . /src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

RUN chmod +x ./run.sh

ENTRYPOINT ["uv", "run", "./run.sh"]
CMD ["crud_api"]
    