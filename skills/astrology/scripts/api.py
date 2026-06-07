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
    params = request.dict(exclude_none=True)
    try:
        # Call the core programmatic engine
        result = astro_engine.calculate_full_profile(params)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run the server locally
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
