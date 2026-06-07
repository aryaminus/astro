"""
Astrology API — FastAPI cloud + self-hosted.

Free by default. Env-driven features:
  ASTRO_API_KEY=sk_live_xxx        → gates all /chart endpoints behind API key
  ASTRO_RATE_LIMIT=100             → max requests per IP per hour (0 = unlimited)
  ASTRO_BILLING_ENABLED=true       → adds X-Tool-Price + X-Tool-Name headers
  ASTRO_PROFILE_DIR=/data/profiles → where saved profiles are persisted (container-safe)
  ASTRO_LOG_LEVEL=INFO             → uvicorn log level
"""
import os
import time
import json
import uuid
import logging
import secrets
from collections import defaultdict, deque
from threading import Lock
from typing import Optional, List

from fastapi import (
    FastAPI, Depends, HTTPException, Security, Response, Request,
    Header,
)
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import sys
import os

# Make the scripts directory importable for `import astro_engine`.
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
import astro_engine  # noqa: E402

VERSION = "2.4.0"

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=os.getenv("ASTRO_LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("astrology-api")

# ── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Astrology API",
    description=(
        "Trustworthy multi-tradition astrology. Deterministic ephemeris engine. "
        "19 modes: natal, transit, synastry, compatibility, composite, astrocartography, "
        "horary, event, solar_return, lunar_return, planetary_return, navamsa, varga, "
        "panchang, moon_phase, numerology, progressions, planetary_hours, transit_natal_aspects. "
        "3 traditions: Western tropical, Vedic/Jyotisha, Chinese BaZi. "
        "Free by default. Set ASTRO_API_KEY to monetize."
    ),
    version=VERSION,
)

from fastapi.staticfiles import StaticFiles

_WELL_KNOWN_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), ".well-known")
if os.path.isdir(_WELL_KNOWN_DIR):
    app.mount("/.well-known", StaticFiles(directory=_WELL_KNOWN_DIR, html=True), name="well-known")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "X-Request-Id", "X-RateLimit-Limit", "X-RateLimit-Remaining",
        "X-RateLimit-Reset", "X-Tool-Price", "X-Tool-Name", "X-API-Version",
    ],
)

# ── Feature Flags ────────────────────────────────────────────────────────────
EXPECTED_API_KEY = os.getenv("ASTRO_API_KEY")                       # unset = free
RATE_LIMIT = int(os.getenv("ASTRO_RATE_LIMIT", "0"))                # 0 = unlimited
RATE_WINDOW_SEC = int(os.getenv("ASTRO_RATE_WINDOW", "3600"))       # default 1h
BILLING_ENABLED = True                                                # price headers always on
PROFILE_DIR = os.getenv("ASTRO_PROFILE_DIR", os.path.expanduser("~"))
PROFILE_PATH = os.path.join(PROFILE_DIR, ".astro_profiles.json")
os.makedirs(PROFILE_DIR, exist_ok=True)

API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


# ── Rate limiter (in-process, per-IP) ───────────────────────────────────────
class RateLimiter:
    """Sliding-window per-IP counter. Thread-safe; resets on process restart.

    For multi-instance deploys, swap for Redis (REDIS_URL env var)."""
    def __init__(self, limit: int, window_sec: int):
        self.limit = limit
        self.window = window_sec
        self.buckets: dict[str, deque] = defaultdict(deque)
        self.lock = Lock()
        self.stats = {"allowed": 0, "blocked": 0, "since_reset": time.time()}

    def check(self, ip: str) -> tuple[bool, int, int]:
        """Return (allowed, remaining, reset_in_sec)."""
        if self.limit <= 0:
            return True, -1, -1
        now = time.time()
        cutoff = now - self.window
        with self.lock:
            q = self.buckets[ip]
            while q and q[0] < cutoff:
                q.popleft()
            if len(q) >= self.limit:
                reset_in = int(q[0] + self.window - now) + 1
                self.stats["blocked"] += 1
                return False, 0, reset_in
            q.append(now)
            self.stats["allowed"] += 1
            return True, self.limit - len(q), int(q[0] + self.window - now)


rate_limiter = RateLimiter(RATE_LIMIT, RATE_WINDOW_SEC)


# ── Middleware: request id, rate limit, logging ──────────────────────────────
@app.middleware("http")
async def add_request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id") or uuid.uuid4().hex[:16]
    client_ip = request.client.host if request.client else "unknown"
    if request.headers.get("X-Forwarded-For"):
        client_ip = request.headers["X-Forwarded-For"].split(",")[0].strip()

    # Public paths skip rate limit and auth entirely
    public_paths = {"/", "/health", "/ready", "/pricing", "/version", "/metrics", "/docs", "/openapi.json", "/redoc"}
    is_public = request.url.path in public_paths

    # Rate limit
    if not is_public:
        allowed, remaining, reset_in = rate_limiter.check(client_ip)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"error": "rate_limited", "detail": f"Limit {RATE_LIMIT}/{RATE_WINDOW_SEC}s exceeded.", "retry_after_sec": reset_in},
                headers={"Retry-After": str(reset_in), "X-Request-Id": request_id},
            )

    started = time.time()
    try:
        response = await call_next(request)
    except Exception as exc:
        log.exception("Unhandled error in %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={"error": "internal_server_error", "detail": str(exc), "request_id": request_id},
            headers={"X-Request-Id": request_id},
        )
    duration_ms = int((time.time() - started) * 1000)

    response.headers["X-Request-Id"] = request_id
    response.headers["X-API-Version"] = VERSION
    if not is_public and RATE_LIMIT > 0:
        response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
        response.headers["X-RateLimit-Reset"] = str(reset_in)
    log.info("%s %s %d %dms ip=%s req_id=%s",
             request.method, request.url.path, response.status_code, duration_ms, client_ip, request_id)
    return response


# ── Auth ────────────────────────────────────────────────────────────────────
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if not EXPECTED_API_KEY:
        return None  # free mode, no key required
    if api_key_header and (api_key_header == EXPECTED_API_KEY or api_key_header == f"Bearer {EXPECTED_API_KEY}"):
        return api_key_header
    raise HTTPException(
        status_code=403,
        detail="Invalid or missing API key. Set ASTRO_API_KEY to enable monetization, or remove it to run free.",
    )


# ── Models ──────────────────────────────────────────────────────────────────
class BirthData(BaseModel):
    year: int
    month: int
    day: int
    hour: int = 12
    minute: int = 0
    lat: float = 0.0
    lng: float = 0.0
    tz: str = "UTC"
    time_known: bool = False
    systems: List[str] = None
    gender: Optional[str] = None
    mode: str = "natal"
    transit_date: Optional[str] = None
    target_year: Optional[int] = None
    target_month: Optional[int] = None
    target_age: Optional[int] = None
    planet: Optional[str] = None
    varga: Optional[str] = None
    full_name: Optional[str] = None
    include_numerology: bool = False


class PartnerData(BaseModel):
    year: int
    month: int
    day: int
    hour: int = 12
    minute: int = 0
    lat: float = 0.0
    lng: float = 0.0
    tz: str = "UTC"
    time_known: bool = True


class PartnerRequest(BirthData):
    partner: PartnerData = None


class ProfileRequest(BaseModel):
    name: str
    year: int
    month: int
    day: int
    hour: int = 12
    minute: int = 0
    lat: float = 0.0
    lng: float = 0.0
    tz: str = "UTC"


class NumerologyRequest(BaseModel):
    year: int
    month: int
    day: int
    full_name: str = ""


class InteractMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str


class InteractRequest(BaseModel):
    """Chat-style interaction. The model calls this to 'poke' the engine with
    natural-language questions and get structured chart data + grounded context.
    Supports multi-turn via the `messages` list and an optional `profile`
    to avoid re-passing birth data every turn."""
    messages: List[InteractMessage] = Field(..., min_length=1, max_length=50)
    profile: Optional[BirthData] = Field(
        None,
        description="Birth data context. If omitted, the last profile for this session_id is used.",
    )
    session_id: Optional[str] = Field(None, description="Opaque session id. Auto-generated if absent.")
    max_context_tokens: int = Field(4000, ge=500, le=16000)


# ── Pricing ────────────────────────────────────────────────────────────────
TOOL_PRICING = {
    "natal": "$0.02", "transit": "$0.02", "synastry": "$0.05",
    "compatibility": "$0.05", "composite": "$0.05", "astrocartography": "$0.03",
    "horary": "$0.03", "event": "$0.02", "solar_return": "$0.03",
    "lunar_return": "$0.03", "planetary_return": "$0.03", "navamsa": "$0.02",
    "varga": "$0.02", "panchang": "$0.02", "moon_phase": "$0.01",
    "numerology": "$0.01", "progressions": "$0.03", "planetary_hours": "$0.01",
    "transit_natal_aspects": "$0.03", "profile": "$0.00", "geocode": "$0.00",
    "reference": "$0.00", "interact": "$0.05",
}


def _billing_header(mode: str):
    return {
        "X-Tool-Price": TOOL_PRICING.get(mode, "$0.00"),
        "X-Tool-Name": mode,
    }


# ── Profile session store (for /interact) ──────────────────────────────────
_profile_sessions: dict[str, dict] = {}
_session_lock = Lock()


def _run(data: dict):
    if data.get("systems") is None:
        data["systems"] = ["western", "vedic", "bazi"]
    try:
        return astro_engine.calculate_full_profile(data)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {e}")
    except Exception as e:
        log.exception("Engine error in mode=%s", data.get("mode"))
        raise HTTPException(status_code=500, detail=str(e))


# ── Routes ──────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "name": "Astrology API",
        "version": VERSION,
        "docs": "/docs",
        "openapi": "/openapi.json",
        "health": "/health",
        "pricing": "/pricing",
        "modes": 19,
        "auth_required": EXPECTED_API_KEY is not None,
        "rate_limit": f"{RATE_LIMIT}/{RATE_WINDOW_SEC}s" if RATE_LIMIT else "unlimited",
    }


@app.get("/health")
async def health():
    """Liveness probe. Always 200 if the process is up."""
    return {
        "status": "ok",
        "version": VERSION,
        "modes": 19,
        "tools": 18,
        "endpoints": 27,
        "auth_required": EXPECTED_API_KEY is not None,
        "rate_limit_per_window": RATE_LIMIT or "unlimited",
        "billing": "active" if BILLING_ENABLED else "disabled",
    }


@app.get("/ready")
async def ready():
    """Readiness probe. Verifies engine can be loaded."""
    try:
        # Sanity check: a quick no-op calculation
        astro_engine.calculate_full_profile({
            "year": 2000, "month": 1, "day": 1, "hour": 12, "minute": 0,
            "lat": 0, "lng": 0, "tz": "UTC", "time_known": True,
            "systems": ["western"], "mode": "moon_phase",
        })
        return {"status": "ready", "engine": "loaded"}
    except Exception as exc:
        return JSONResponse(status_code=503, content={"status": "not_ready", "error": str(exc)})


@app.get("/version")
async def version():
    return {"version": VERSION, "engine": "astro_engine"}


@app.get("/metrics")
async def metrics():
    """Operational metrics. Counters only — no PII, no per-user tracking."""
    return {
        "rate_limit": {
            "limit": RATE_LIMIT,
            "window_sec": RATE_WINDOW_SEC,
            "allowed": rate_limiter.stats["allowed"],
            "blocked": rate_limiter.stats["blocked"],
            "active_ips": len(rate_limiter.buckets),
            "uptime_sec": int(time.time() - rate_limiter.stats["since_reset"]),
        },
        "interact_sessions": len(_profile_sessions),
    }


@app.get("/pricing")
async def pricing():
    return {"currency": "USD", "per_call": TOOL_PRICING, "current_mode": "free" if not EXPECTED_API_KEY else "metered"}


# ── Chart endpoints (25) ───────────────────────────────────────────────────
@app.post("/chart", dependencies=[Depends(get_api_key)])
async def generic_chart(request: BirthData, response: Response):
    """Universal endpoint — accepts any mode. Set `mode` in the request body."""
    params = request.model_dump(exclude_none=True)
    mode = params.get("mode", "natal")
    response.headers.update(_billing_header(mode))
    return _run(params)


@app.post("/chart/natal", dependencies=[Depends(get_api_key)])
async def natal_chart(request: BirthData, response: Response):
    """Full natal chart(s). Auto-includes aspect patterns, Arabic Parts, fixed stars, dignities, BML, doshas."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "natal"
    response.headers.update(_billing_header("natal"))
    return _run(params)


@app.post("/chart/transit", dependencies=[Depends(get_api_key)])
async def transit_chart(request: BirthData, response: Response):
    """Current sky vs natal chart. Set transit_date or defaults to today."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "transit"
    response.headers.update(_billing_header("transit"))
    return _run(params)


@app.post("/chart/synastry", dependencies=[Depends(get_api_key)])
async def synastry_chart(request: PartnerRequest, response: Response):
    """Relationship comparison between two charts."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "synastry"
    response.headers.update(_billing_header("synastry"))
    return _run(params)


@app.post("/chart/compatibility", dependencies=[Depends(get_api_key)])
async def compatibility(request: PartnerRequest, response: Response):
    """0-100 compatibility scoring with 5 subscores + synastry aspects."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "compatibility"
    response.headers.update(_billing_header("compatibility"))
    return _run(params)


@app.post("/chart/composite", dependencies=[Depends(get_api_key)])
async def composite_chart(request: PartnerRequest, response: Response):
    """Midpoint composite chart — the relationship as a third entity."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "composite"
    response.headers.update(_billing_header("composite"))
    return _run(params)


@app.post("/chart/solar-return", dependencies=[Depends(get_api_key)])
async def solar_return_chart(request: BirthData, response: Response):
    """Annual solar return chart. Set target_year or defaults to next birthday."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "solar_return"
    response.headers.update(_billing_header("solar_return"))
    return _run(params)


@app.post("/chart/lunar-return", dependencies=[Depends(get_api_key)])
async def lunar_return_chart(request: BirthData, response: Response):
    """Monthly lunar return chart. Set target_year and target_month."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "lunar_return"
    response.headers.update(_billing_header("lunar_return"))
    return _run(params)


@app.post("/chart/planetary-return", dependencies=[Depends(get_api_key)])
async def planetary_return_chart(request: BirthData, response: Response):
    """Return chart for any planet. Set planet (e.g. Jupiter, Saturn) and target_year."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "planetary_return"
    response.headers.update(_billing_header("planetary_return"))
    return _run(params)


@app.post("/chart/navamsa", dependencies=[Depends(get_api_key)])
async def navamsa_chart(request: BirthData, response: Response):
    """Vedic D9 Navamsa chart with vargottama detection."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "navamsa"
    params["systems"] = ["vedic"]
    response.headers.update(_billing_header("navamsa"))
    return _run(params)


@app.post("/chart/varga", dependencies=[Depends(get_api_key)])
async def varga_chart(request: BirthData, response: Response):
    """Any Vedic divisional chart (D2-D60). Set varga field (e.g. D10, D12)."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "varga"
    params["systems"] = ["vedic"]
    response.headers.update(_billing_header("varga"))
    return _run(params)


@app.post("/chart/progressions", dependencies=[Depends(get_api_key)])
async def progressions_chart(request: BirthData, response: Response):
    """Secondary progressions (1 day = 1 year). Set target_age."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "progressions"
    response.headers.update(_billing_header("progressions"))
    return _run(params)


@app.post("/chart/transit-aspects", dependencies=[Depends(get_api_key)])
async def transit_natal_aspects(request: BirthData, response: Response):
    """Detailed transit-to-natal aspects with impact ratings."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "transit_natal_aspects"
    response.headers.update(_billing_header("transit_natal_aspects"))
    return _run(params)


@app.post("/astrocartography", dependencies=[Depends(get_api_key)])
async def astrocartography_chart(request: BirthData, response: Response):
    """Planet lines on the globe for relocation analysis."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "astrocartography"
    response.headers.update(_billing_header("astrocartography"))
    return _run(params)


@app.post("/horary", dependencies=[Depends(get_api_key)])
async def horary_chart(request: BirthData, response: Response):
    """Chart of the moment for a specific question."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "horary"
    response.headers.update(_billing_header("horary"))
    return _run(params)


@app.post("/panchang", dependencies=[Depends(get_api_key)])
async def panchang(request: BirthData, response: Response):
    """Complete Vedic Panchang: Tithi, Nakshatra, Yoga, Karana."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "panchang"
    params["systems"] = ["vedic"]
    response.headers.update(_billing_header("panchang"))
    return _run(params)


@app.post("/moon-phase", dependencies=[Depends(get_api_key)])
async def moon_phase(request: BirthData, response: Response):
    """Moon phase with illumination %, age, and upcoming phases."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "moon_phase"
    response.headers.update(_billing_header("moon_phase"))
    return _run(params)


@app.post("/planetary-hours", dependencies=[Depends(get_api_key)])
async def planetary_hours(request: BirthData, response: Response):
    """Chaldean planetary hours for the day."""
    params = request.model_dump(exclude_none=True)
    params["mode"] = "planetary_hours"
    response.headers.update(_billing_header("planetary_hours"))
    return _run(params)


@app.post("/numerology", dependencies=[Depends(get_api_key)])
async def numerology(request: NumerologyRequest, response: Response):
    """Life Path, Personal Year, Expression, Soul Urge."""
    params = {"year": request.year, "month": request.month, "day": request.day,
              "hour": 12, "minute": 0, "lat": 0, "lng": 0, "tz": "UTC",
              "time_known": False, "systems": ["western"], "mode": "numerology"}
    if request.full_name:
        params["full_name"] = request.full_name
    response.headers.update(_billing_header("numerology"))
    return _run(params)


@app.post("/profile", dependencies=[Depends(get_api_key)])
async def save_profile(request: ProfileRequest, response: Response):
    """Save a user's birth profile to PROFILE_DIR for future sessions."""
    try:
        profiles = {}
        if os.path.exists(PROFILE_PATH):
            with open(PROFILE_PATH, "r") as f:
                profiles = json.load(f)
        profiles[request.name] = request.model_dump()
        with open(PROFILE_PATH, "w") as f:
            json.dump(profiles, f, indent=2)
        response.headers.update(_billing_header("profile"))
        return {"status": "success", "message": f"Profile '{request.name}' saved.", "path": PROFILE_PATH}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/profile/{name}", dependencies=[Depends(get_api_key)])
async def load_profile(name: str, response: Response):
    """Retrieve a saved birth profile."""
    try:
        if os.path.exists(PROFILE_PATH):
            with open(PROFILE_PATH, "r") as f:
                profiles = json.load(f)
            if name in profiles:
                response.headers.update(_billing_header("profile"))
                return profiles[name]
        raise HTTPException(status_code=404, detail=f"Profile '{name}' not found.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/profile/{name}", dependencies=[Depends(get_api_key)])
async def delete_profile(name: str, response: Response):
    """Delete a saved profile. GDPR-friendly."""
    try:
        if os.path.exists(PROFILE_PATH):
            with open(PROFILE_PATH, "r") as f:
                profiles = json.load(f)
            if name in profiles:
                del profiles[name]
                with open(PROFILE_PATH, "w") as f:
                    json.dump(profiles, f, indent=2)
                response.headers.update(_billing_header("profile"))
                return {"status": "deleted", "name": name}
        raise HTTPException(status_code=404, detail=f"Profile '{name}' not found.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/geocode", dependencies=[Depends(get_api_key)])
async def geocode(city: str, response: Response):
    """Retrieve latitude, longitude, and timezone for a city name.

    Uses the public open-meteo geocoding API. If the network is unavailable
    in your environment, pass lat/lng directly to chart endpoints instead."""
    import urllib.request, json as j, urllib.parse
    query = urllib.parse.quote(city)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=1&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Astro-API'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = j.loads(resp.read().decode())
            if not data.get("results"):
                raise HTTPException(status_code=404, detail=f"City '{city}' not found.")
            res = data["results"][0]
            response.headers.update(_billing_header("geocode"))
            return {"city": res.get("name"), "country": res.get("country"),
                    "lat": res.get("latitude"), "lng": res.get("longitude"),
                    "timezone": res.get("timezone")}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Geocoding service unavailable: {e}")


@app.get("/reference/{system}", dependencies=[Depends(get_api_key)])
async def get_reference(system: str, response: Response):
    """Retrieve interpretation guidelines for a given astrological system."""
    allowed = ["bazi", "consultation", "health", "specialty-systems",
               "synastry-and-timing", "tibetan", "vedic", "western"]
    if system not in allowed:
        raise HTTPException(status_code=400, detail=f"System must be one of {allowed}")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ref_path = os.path.join(script_dir, "..", "references", f"{system}.md")
    try:
        with open(ref_path, "r") as f:
            response.headers.update(_billing_header("reference"))
            return {"content": f.read()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading reference: {e}")


# ── /interact — chat-style poke endpoint ───────────────────────────────────
INTENT_KEYWORDS = {
    "natal": ["natal", "birth chart", "my chart", "born", "birthday", "who am i"],
    "transit": ["transit", "what's happening", "current sky", "today's sky", "this week", "this month"],
    "synastry": ["synastry", "compare", "between us", "my partner and i"],
    "compatibility": ["compatible", "compatibility", "love match", "relationship score", "should we"],
    "composite": ["composite", "relationship chart", "us as one"],
    "solar_return": ["solar return", "year ahead", "birthday forecast", "next year"],
    "lunar_return": ["lunar return", "monthly forecast", "next month"],
    "planetary_return": ["saturn return", "jupiter return", "chiron return", "uranus return", "neptune return", "pluto return"],
    "navamsa": ["navamsa", "d9", "d-9", "vargottama"],
    "varga": ["d10", "d12", "d60", "divisional", "varga", "dashamsa", "dwadashamsa"],
    "astrocartography": ["astrocartography", "relocate", "where should i live", "planet lines"],
    "horary": ["horary", "should i", "is it a good time", "when should i"],
    "panchang": ["panchang", "tithi", "nakshatra today", "muhurta"],
    "moon_phase": ["moon phase", "moon today", "full moon", "new moon", "illumination"],
    "numerology": ["numerology", "life path", "personal year", "expression number", "soul urge"],
    "progressions": ["progressed", "progressions", "secondary progression"],
    "planetary_hours": ["planetary hour", "chaldean", "electional", "best time to"],
    "transit_natal_aspects": ["transit aspects", "aspects to my", "what's hitting my chart"],
}


def _detect_intent(text: str) -> Optional[str]:
    t = text.lower()
    for mode, kws in INTENT_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                return mode
    return None


def _suggest_mode(text: str, profile: dict) -> dict:
    """Given a user message + their birth profile, return a structured
    `engine_actions` list the model can execute to answer the question.
    This is the *grounding* step: the model calls the engine, then
    interprets the structured output."""
    text_lc = text.lower()
    mode = _detect_intent(text_lc)
    actions = []
    rationale_parts = []

    if mode is None:
        # No clear mode → natal + current transits as a safe default
        mode = "transit"
        actions.append({"mode": "natal", "params": profile})
        rationale_parts.append("No specific mode detected; defaulting to natal + current transits for a general reading.")
    else:
        actions.append({"mode": mode, "params": profile})

    if "transit" not in mode and "return" not in mode and "phase" not in mode and "hour" not in mode and "numerology" not in mode:
        actions.append({"mode": "transit_natal_aspects", "params": profile})
        rationale_parts.append("Added transit-to-natal aspects for live timing context.")

    return {
        "detected_mode": mode,
        "actions": actions,
        "rationale": " ".join(rationale_parts) or f"Single action for mode '{mode}'.",
    }


def _summarize_messages(messages: List[InteractMessage], max_chars: int = 8000) -> str:
    out = []
    total = 0
    for m in messages[::-1]:
        chunk = f"[{m.role}] {m.content}\n"
        if total + len(chunk) > max_chars:
            break
        out.append(chunk)
        total += len(chunk)
    return "".join(reversed(out))


@app.post("/interact", dependencies=[Depends(get_api_key)])
async def interact(request: InteractRequest, response: Response):
    """Chat-style poke/interaction endpoint.

    The host LLM (or any client) sends a natural-language question plus the
    user's birth profile. The endpoint:
      1. Detects the right engine mode(s) from the question
      2. Runs the deterministic engine for each action
      3. Returns structured chart data + a `grounding_packet` the model
         uses to interpret, plus a `mode_used` so the host knows what was
         actually computed.

    This is the endpoint to call when a user "pokes" the agent with a
    follow-up question during a session. The model never has to guess
    positions — it interprets this structured output."""
    # Session handling
    session_id = request.session_id or secrets.token_urlsafe(12)
    if request.profile is not None:
        with _session_lock:
            _profile_sessions[session_id] = request.profile.model_dump(exclude_none=True)
    else:
        with _session_lock:
            stored = _profile_sessions.get(session_id)
        if stored is None:
            raise HTTPException(
                status_code=400,
                detail="No profile in request and no prior session found. Pass `profile` on the first call or set session_id after a profile-bearing call.",
            )
        request.profile = BirthData(**stored)

    last_user_msg = next((m.content for m in reversed(request.messages) if m.role == "user"), "")
    if not last_user_msg:
        raise HTTPException(status_code=400, detail="At least one user message is required.")

    plan = _suggest_mode(last_user_msg, request.profile.model_dump(exclude_none=True))
    results = []
    errors = []
    for action in plan["actions"]:
        try:
            result = _run({**action["params"], "mode": action["mode"]})
            results.append({"mode": action["mode"], "ok": True, "data": result})
        except HTTPException as exc:
            errors.append({"mode": action["mode"], "error": exc.detail})
            results.append({"mode": action["mode"], "ok": False, "error": exc.detail})
        except Exception as exc:
            log.exception("interact action failed: %s", action["mode"])
            errors.append({"mode": action["mode"], "error": str(exc)})
            results.append({"mode": action["mode"], "ok": False, "error": str(exc)})

    response.headers.update(_billing_header("interact"))

    return {
        "session_id": session_id,
        "detected_mode": plan["detected_mode"],
        "rationale": plan["rationale"],
        "actions_run": [a["mode"] for a in plan["actions"]],
        "results": results,
        "errors": errors,
        "conversation_excerpt": _summarize_messages(request.messages),
        "grounding_packet": {
            "instruction": (
                "Interpret the structured chart data above. Do NOT invent positions, "
                "aspects, or houses. Use the references at /reference/{system} to ground "
                "your language. If a mode returned no usable data, say so honestly."
            ),
            "available_references": ["western", "vedic", "bazi", "health", "synastry-and-timing", "consultation"],
        },
    }


@app.delete("/interact/{session_id}", dependencies=[Depends(get_api_key)])
async def clear_interact_session(session_id: str):
    """Clear an interact session. GDPR-friendly."""
    with _session_lock:
        existed = _profile_sessions.pop(session_id, None)
    return {"status": "cleared" if existed else "no_such_session", "session_id": session_id}


# ── MCP endpoints ────────────────────────────────────────────────────────────
import skills.astrology.scripts.mcp_server as _mcp_mod

_mcp_sse_app = _mcp_mod.mcp.sse_app()
app.mount("/mcp", _mcp_sse_app)
log.info("MCP SSE endpoint mounted at /mcp/sse")


# ── Entrypoint ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level=os.getenv("ASTRO_LOG_LEVEL", "info").lower())
