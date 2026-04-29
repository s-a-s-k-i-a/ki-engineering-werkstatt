# Python-Sidecar für KI-Plugin-Helfer RAG
# Stand: 0.1.0 (Stub-Modus + FastAPI-Skelett)

FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# uv als 2026er-Standard-Paket-Manager
RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
RUN uv pip install --system --no-cache .

COPY sidecar.py ./

EXPOSE 8765

# Healthcheck für docker-compose
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request as u; u.urlopen('http://localhost:8765/health', timeout=3)" || exit 1

CMD ["python", "sidecar.py"]
