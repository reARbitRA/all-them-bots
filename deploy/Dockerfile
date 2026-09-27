# syntax=docker/dockerfile:1.4
FROM python:3.11-slim-bookworm AS builder

WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final Production Stage
FROM python:3.11-slim-bookworm AS runner

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/omnibot/.local/bin:$PATH"

# Create non-root system user
RUN groupadd -g 10001 omnibot && \
    useradd -u 10001 -g omnibot -m -s /bin/bash omnibot && \
    mkdir -p /app/data && chown -R omnibot:omnibot /app

COPY --from=builder --chown=omnibot:omnibot /root/.local /home/omnibot/.local
COPY --chown=omnibot:omnibot . /app

USER omnibot:omnibot
EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')" || exit 1

ENTRYPOINT ["python3", "run.py", "--host", "0.0.0.0", "--port", "8000"]
