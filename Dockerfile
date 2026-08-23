# syntax=docker/dockerfile:1

# ---------- builder: install dependencies ----------
FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Dependencies only. This layer stays cached until pyproject.toml or uv.lock
# change, so editing application code reinstalls nothing.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project


# ---------- runtime: the image you actually ship ----------
FROM python:3.13-slim AS runtime

ARG GIT_SHA=unknown

ENV GIT_SHA=${GIT_SHA} \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN groupadd --system app && useradd --system --gid app app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv ./.venv
COPY --chown=app:app app ./app
COPY --chown=app:app alembic ./alembic
COPY --chown=app:app alembic.ini ./

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]