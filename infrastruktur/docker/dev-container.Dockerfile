FROM python:3.13-slim-bookworm

# Werkzeuge
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates git just \
    && rm -rf /var/lib/apt/lists/*

# uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /work
COPY pyproject.toml uv.lock* /work/
RUN uv sync --no-dev || true   # initiales Sync, fehlt uv.lock noch

EXPOSE 2718 6006 6333

CMD ["bash"]
