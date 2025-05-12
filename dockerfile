# Этап установки зависимостей с помощью uv
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS requirements-stage
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Этап получения финального образа без uv
FROM python:3.12-slim
WORKDIR /app
COPY --from=requirements-stage --chown=app:app /app /app
ENV PATH="/app/.venv/bin:$PATH"
RUN chmod +x ./run.sh
ENTRYPOINT ["./run.sh"]
CMD ["crud_api"]
    