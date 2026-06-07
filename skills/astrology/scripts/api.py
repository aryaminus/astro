import os
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import astro_engine

app = FastAPI(
    title="Astrology API",
    description="Deterministic ephemeris API for multi-tradition astrology.",
    version="1.0.0"
)

# Optional API Key configuration for Monetization
API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
EXPECTED_API_KEY = os.getenv("ASTRO_API_KEY") # e.g. set via Stripe/Zuplo if monetizing

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if not EXPECTED_API_KEY:
        # If no key is set in the environment, the API is free/public
        return None
    if api_key_header == EXPECTED_API_KEY or api_key_header == f"Bearer {EXPECTED_API_KEY}":
        return api_key_header
    raise HTTPException(
        status_code=403, detail="Could not validate credentials. A valid API key is required."
    )

class ChartRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int = 12
    minute: int = 0
    lat: float = 0.0
    lng: float = 0.0
    tz: str = "UTC"
    time_known: bool = False
    systems: List[str] = ["western", "vedic", "bazi"]
    gender: Optional[str] = None
    mode: str = "natal"
    transit_date: Optional[str] = None

@app.post("/chart", dependencies=[Depends(get_api_key)])
async def generate_chart(request: ChartRequest):
    """
    Generate an astrological chart based on the provided inputs.
    Requires a valid API key in the Authorization header if ASTRO_API_KEY is configured.
    """
    params = request.model_dump(exclude_none=True)
    try:
        # Call the core programmatic engine
        result = astro_engine.calculate_full_profile(params)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

def get_profile_path():
    import os
    return os.path.expanduser("~/.astro_profiles.json")

@app.post("/profile", dependencies=[Depends(get_api_key)])
async def save_profile(request: ProfileRequest):
    """Save a user's birth profile to memory."""
    import json, os
    profile_path = get_profile_path()
    try:
        profiles = {}
        if os.path.exists(profile_path):
            with open(profile_path, "r") as f:
                profiles = json.load(f)
        profiles[request.name] = request.model_dump()
        with open(profile_path, "w") as f:
            json.dump(profiles, f, indent=2)
        return {"status": "success", "message": f"Profile '{request.name}' saved."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile/{name}", dependencies=[Depends(get_api_key)])
async def load_profile(name: str):
    """Retrieve a saved birth profile."""
    import json, os
    profile_path = get_profile_path()
    try:
        if os.path.exists(profile_path):
            with open(profile_path, "r") as f:
                profiles = json.load(f)
            if name in profiles:
                return profiles[name]
        raise HTTPException(status_code=404, detail=f"Profile '{name}' not found.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/geocode", dependencies=[Depends(get_api_key)])
async def geocode(city: str):
    """Retrieve latitude and longitude for a city name."""
    import urllib.request, json, urllib.parse
    query = urllib.parse.quote(city)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=1&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Astro-API'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if not data.get("results"):
                raise HTTPException(status_code=404, detail=f"City '{city}' not found.")
            res = data["results"][0]
            return {
                "city": res.get("name"),
                "country": res.get("country"),
                "lat": res.get("latitude"),
                "lng": res.get("longitude"),
                "timezone": res.get("timezone")
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reference/{system}", dependencies=[Depends(get_api_key)])
async def get_reference(system: str):
    """Retrieve the astrology interpretation guidelines for a given system."""
    import os
    # system should be one of the files in references/ without the .md extension
    allowed = ["bazi", "consultation", "health", "specialty-systems", "synastry-and-timing", "vedic", "western"]
    if system not in allowed:
        raise HTTPException(status_code=400, detail=f"System must be one of {allowed}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ref_path = os.path.join(script_dir, "..", "references", f"{system}.md")
    try:
        with open(ref_path, "r") as f:
            return {"content": f.read()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading reference: {e}")

if __name__ == "__main__":
    import uvicorn
    # Run the server locally
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
