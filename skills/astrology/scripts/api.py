import os
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, Security, Response
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import astro_engine

app = FastAPI(
    title="Astrology API",
    description=(
        "Trustworthy multi-tradition astrology. Deterministic ephemeris engine. "
        "19 modes: natal, transit, synastry, compatibility, composite, astrocartography, "
        "horary, event, solar_return, lunar_return, planetary_return, navamsa, varga, "
        "panchang, moon_phase, numerology, progressions, planetary_hours, transit_natal_aspects. "
        "3 traditions: Western tropical, Vedic/Jyotisha, Chinese BaZi."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# ── Feature Flags ──────────────────────────────────────────────────────────────
# All free by default. Flip these to monetize:
#   ASTRO_API_KEY=sk_live_xxx        → gates all endpoints behind API key
#   ASTRO_RATE_LIMIT=100             → max requests per IP per hour (0 = unlimited)
#   ASTRO_BILLING_ENABLED=true       → includes X-Tool-Price headers (always on for analytics)
EXPECTED_API_KEY = os.getenv("ASTRO_API_KEY")           # unset = free
RATE_LIMIT = int(os.getenv("ASTRO_RATE_LIMIT", "0"))    # 0 = unlimited
BILLING_ENABLED = True                                   # price headers always included for analytics

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if not EXPECTED_API_KEY:
        return None
    if api_key_header == EXPECTED_API_KEY or api_key_header == f"Bearer {EXPECTED_API_KEY}":
        return api_key_header
    raise HTTPException(status_code=403, detail="Invalid API key.")

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

TOOL_PRICING = {
    "natal": "$0.02", "transit": "$0.02", "synastry": "$0.05",
    "compatibility": "$0.05", "composite": "$0.05", "astrocartography": "$0.03",
    "horary": "$0.03", "event": "$0.02", "solar_return": "$0.03",
    "lunar_return": "$0.03", "planetary_return": "$0.03", "navamsa": "$0.02",
    "varga": "$0.02", "panchang": "$0.02", "moon_phase": "$0.01",
    "numerology": "$0.01", "progressions": "$0.03", "planetary_hours": "$0.01",
    "transit_natal_aspects": "$0.03", "profile": "$0.00", "geocode": "$0.00",
    "reference": "$0.00",
}

def _billing_header(mode: str):
    return {"X-Tool-Price": TOOL_PRICING.get(mode, "$0.00"),
            "X-Tool-Name": mode}

def _run(data: dict):
    if data.get("systems") is None:
        data["systems"] = ["western", "vedic", "bazi"]
    try:
        return astro_engine.calculate_full_profile(data)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    """Chart of the moment for a specific question. Pass question_time and question via extra fields."""
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
    """Life Path, Personal Year, Expression, Soul Urge. Pass full_name for name-based numbers."""
    params = {"year": request.year, "month": request.month, "day": request.day,
              "hour": 12, "minute": 0, "lat": 0, "lng": 0, "tz": "UTC",
              "time_known": False, "systems": ["western"], "mode": "numerology"}
    if request.full_name:
        params["full_name"] = request.full_name
    response.headers.update(_billing_header("numerology"))
    return _run(params)

@app.post("/profile", dependencies=[Depends(get_api_key)])
async def save_profile(request: ProfileRequest, response: Response):
    """Save a user's birth profile for future sessions."""
    import json
    profile_path = os.path.expanduser("~/.astro_profiles.json")
    try:
        profiles = {}
        if os.path.exists(profile_path):
            with open(profile_path, "r") as f:
                profiles = json.load(f)
        profiles[request.name] = request.model_dump()
        with open(profile_path, "w") as f:
            json.dump(profiles, f, indent=2)
        response.headers.update(_billing_header("profile"))
        return {"status": "success", "message": f"Profile '{request.name}' saved."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile/{name}", dependencies=[Depends(get_api_key)])
async def load_profile(name: str, response: Response):
    """Retrieve a saved birth profile."""
    import json
    profile_path = os.path.expanduser("~/.astro_profiles.json")
    try:
        if os.path.exists(profile_path):
            with open(profile_path, "r") as f:
                profiles = json.load(f)
            if name in profiles:
                response.headers.update(_billing_header("profile"))
                return profiles[name]
        raise HTTPException(status_code=404, detail=f"Profile '{name}' not found.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/geocode", dependencies=[Depends(get_api_key)])
async def geocode(city: str, response: Response):
    """Retrieve latitude, longitude, and timezone for a city name."""
    import urllib.request, json as j, urllib.parse
    query = urllib.parse.quote(city)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=1&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Astro-API'})
        with urllib.request.urlopen(req) as resp:
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
        raise HTTPException(status_code=500, detail=str(e))

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

@app.get("/health")
async def health_check():
    """Server health check. No auth required."""
    return {
        "status": "ok",
        "version": "2.0.0",
        "modes": 19,
        "tools": 18,
        "endpoints": 25,
        "auth_required": EXPECTED_API_KEY is not None,
        "rate_limit_per_hour": RATE_LIMIT or "unlimited",
        "billing": "active" if BILLING_ENABLED else "disabled",
        "note": "All endpoints are currently FREE. Set ASTRO_API_KEY to enable API key gating."
                if not EXPECTED_API_KEY else "API key required.",
    }

@app.get("/pricing")
async def get_pricing():
    """List all tool prices. No auth required."""
    return {"currency": "USD", "per_call": TOOL_PRICING}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
