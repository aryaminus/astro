FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000 \
    ASTRO_LOG_LEVEL=INFO

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# The container only needs the skill engine + API. Distribution manifests
# (smithery.yaml, .claude-plugin, gemini-extension.json) are for local skill
# installs and marketplace publishing, not for the running API.
COPY skills /app/skills
COPY openapi.yaml /app/openapi.yaml
COPY AGENTS.md /app/AGENTS.md
COPY README.md /app/README.md

# Profile persistence directory
RUN mkdir -p /data/profiles && chown -R 1000:1000 /data
ENV ASTRO_PROFILE_DIR=/data/profiles

# Non-root user
RUN useradd --create-home --uid 1000 astro
USER astro

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request, sys; \
  sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/ready', timeout=3).status == 200 else 1)"

CMD ["sh", "-c", "uvicorn skills.astrology.scripts.api:app --host 0.0.0.0 --port ${PORT}"]
