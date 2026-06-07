FROM python:3.14-slim

# Hardened base: non-root user, pinned deps, no cache
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000 \
    ASTRO_LOG_LEVEL=INFO

WORKDIR /app

# Install only what's required at runtime. pyswisseph is optional; the engine
# auto-upgrades if present. The MCP + FastAPI stack is required for hosting.
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the skill bundle. The repo layout (skills/astrology/...) is preserved
# so paths like skills/astrology/scripts/api.py work as documented.
COPY skills /app/skills
COPY openapi.yaml /app/openapi.yaml
COPY smithery.yaml /app/smithery.yaml
COPY gemini-extension.json /app/gemini-extension.json
COPY .claude-plugin /app/.claude-plugin
COPY AGENTS.md /app/AGENTS.md
COPY README.md /app/README.md
COPY llms.txt /app/llms.txt

# Profile persistence directory. Mount a volume here in production.
RUN mkdir -p /data/profiles && chown -R 1000:1000 /data
ENV ASTRO_PROFILE_DIR=/data/profiles

# Run as non-root
RUN useradd --create-home --uid 1000 astro
USER astro
WORKDIR /app

EXPOSE 8000

# Default: FastAPI on PORT (cloud). Override with CMD ["python","-m","skills.astrology.scripts.mcp_server"]
# to run the MCP server instead (set ASTRO_MCP_TRANSPORT=sse).
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request, sys; \
  sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/ready', timeout=3).status == 200 else 1)"

CMD ["sh", "-c", "uvicorn skills.astrology.scripts.api:app --host 0.0.0.0 --port ${PORT}"]
