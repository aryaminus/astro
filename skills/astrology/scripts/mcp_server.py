#!/usr/bin/env python3
"""
Model Context Protocol (MCP) server wrapper for the Astrology Engine.
This allows the astrology engine to be used natively by MCP-compatible
clients like Claude Desktop, Cursor, Zed, Devin, and Antigravity, as well
as cloud MCP hosts (Smithery, Cloudflare, Render) over HTTP+SSE.

Requires the `mcp` SDK:
  pip install mcp

Transport selection via env var ASTRO_MCP_TRANSPORT:
  - stdio (default): local Claude Desktop / Cursor
  - sse:              cloud MCP hosts (HTTP + Server-Sent Events)
  - http:             Streamable HTTP (modern MCP transport)

Set ASTRO_MCP_HOST (default 0.0.0.0) and ASTRO_MCP_PORT (default 8765) for network mode.
"""

import os
import sys
import json
import logging
from typing import Any, Sequence

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("ERROR: The 'mcp' package is required. Install it with: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Make this script's directory importable for `import astro_engine` so the
# same code works whether invoked as `python -m skills.astrology.scripts.mcp_server`
# or `python skills/astrology/scripts/mcp_server.py`.
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

# Import the core engine
import astro_engine  # noqa: E402

# Network bind config. Cloud hosts (Render, Cloudflare) inject the port to bind
# via $PORT, so prefer it; ASTRO_MCP_PORT lets you override explicitly for local
# runs. host/port are set on the FastMCP constructor (its `run()` does NOT accept
# them as kwargs — they live in mcp.settings).
_MCP_HOST = os.environ.get("ASTRO_MCP_HOST", "0.0.0.0")
_MCP_PORT = int(os.environ.get("ASTRO_MCP_PORT") or os.environ.get("PORT") or "8765")

# Initialize the MCP server
mcp = FastMCP(
    "Astrology Engine",
    host=_MCP_HOST,
    port=_MCP_PORT,
)

@mcp.tool()
def get_astrology_chart(
    year: int,
    month: int,
    day: int,
    hour: int = 12,
    minute: int = 0,
    lat: float = 0.0,
    lng: float = 0.0,
    tz: str = "UTC",
    time_known: bool = False,
    systems: list[str] = None,
    gender: str = None,
    mode: str = "natal",
    transit_date: str = None
) -> str:
    """
    Calculate an astrological chart (Western, Vedic, BaZi) based on birth data.
    All inputs feed directly into the deterministic ephemeris engine.
    """
    if systems is None:
        systems = ["western", "vedic", "bazi"]
        
    params = {
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "lat": lat,
        "lng": lng,
        "tz": tz,
        "time_known": time_known,
        "systems": systems,
        "mode": mode,
    }
    
    if gender:
        params["gender"] = gender
    if transit_date:
        params["transit_date"] = transit_date

    try:
        # astro_engine.calculate_chart is the core computation block
        # We need to call the engine's programmatic interface
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_astrology_reference(system: str) -> str:
    """
    Retrieve authentic interpretation guidelines for a specific astrological system.
    Use this to ground your readings instead of hallucinating meanings.
    Valid systems: 'western', 'vedic', 'bazi', 'health', 'synastry', 'consultation'.
    """
    import os
    # Assume references are in skills/astrology/references/
    ref_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")
    # Mapping system names to standard files
    file_map = {
        "western": "western.md",
        "vedic": "vedic.md",
        "bazi": "bazi.md",
        "health": "health.md",
        "synastry": "synastry-and-timing.md",
        "consultation": "consultation.md"
    }
    target = file_map.get(system.lower())
    if not target:
        return f"Error: Reference for '{system}' not found. Available: {list(file_map.keys())}"
    
    path = os.path.join(ref_dir, target)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading reference: {e}"

@mcp.tool()
def save_profile(name: str, year: int, month: int, day: int, hour: int = 12, minute: int = 0, lat: float = 0.0, lng: float = 0.0, tz: str = "UTC") -> str:
    """
    Save a user's birth profile to local memory for future sessions.
    """
    import os, json
    profile_path = os.path.expanduser("~/.astro_profiles.json")
    try:
        if os.path.exists(profile_path):
            with open(profile_path, "r") as f:
                profiles = json.load(f)
        else:
            profiles = {}
            
        profiles[name] = {
            "year": year, "month": month, "day": day,
            "hour": hour, "minute": minute,
            "lat": lat, "lng": lng, "tz": tz
        }
        with open(profile_path, "w") as f:
            json.dump(profiles, f, indent=2)
        return f"Profile '{name}' saved successfully."
    except Exception as e:
        return f"Error saving profile: {e}"

@mcp.tool()
def get_profile(name: str) -> str:
    """
    Retrieve a saved birth profile.
    """
    import os, json
    profile_path = os.path.expanduser("~/.astro_profiles.json")
    try:
        if os.path.exists(profile_path):
            with open(profile_path, "r") as f:
                profiles = json.load(f)
            if name in profiles:
                return json.dumps(profiles[name], indent=2)
        return f"Profile '{name}' not found."
    except Exception as e:
        return f"Error loading profile: {e}"

@mcp.tool()
def geocode_city(city_name: str) -> str:
    """
    Retrieve the latitude and longitude for a given city name.
    Use this to look up coordinates if the user only provides a city name.
    """
    import urllib.request, json, urllib.parse
    query = urllib.parse.quote(city_name)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=1&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Astro-MCP'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if not data.get("results"):
                return f"Error: City '{city_name}' not found."
            res = data["results"][0]
            return json.dumps({
                "city": res.get("name"),
                "country": res.get("country"),
                "lat": res.get("latitude"),
                "lng": res.get("longitude"),
                "timezone": res.get("timezone")
            }, indent=2)
    except Exception as e:
        return f"Error geocoding city: {e}"

@mcp.tool()
def get_solar_return(
    year: int, month: int, day: int, hour: int = 12, minute: int = 0,
    lat: float = 0.0, lng: float = 0.0, tz: str = "UTC",
    target_year: int = None
) -> str:
    """
    Calculate a solar return chart — the moment the Sun returns to its natal position.
    Essential for annual birthday forecasts and year-ahead readings.
    """
    params = {"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
              "lat": lat, "lng": lng, "tz": tz, "time_known": True,
              "systems": ["western"], "mode": "solar_return"}
    if target_year:
        params["target_year"] = target_year
    try:
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_lunar_return(
    year: int, month: int, day: int, hour: int = 12, minute: int = 0,
    lat: float = 0.0, lng: float = 0.0, tz: str = "UTC",
    target_year: int = None, target_month: int = None
) -> str:
    """
    Calculate a lunar return chart — the moment the Moon returns to its natal position.
    Used for monthly forecasts and emotional cycle tracking.
    """
    params = {"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
              "lat": lat, "lng": lng, "tz": tz, "time_known": True,
              "systems": ["western"], "mode": "lunar_return"}
    if target_year:
        params["target_year"] = target_year
    if target_month:
        params["target_month"] = target_month
    try:
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_compatibility(
    year: int, month: int, day: int, hour: int = 12, minute: int = 0,
    lat: float = 0.0, lng: float = 0.0, tz: str = "UTC",
    partner_year: int = None, partner_month: int = None, partner_day: int = None,
    partner_hour: int = 12, partner_minute: int = 0,
    partner_lat: float = 0.0, partner_lng: float = 0.0, partner_tz: str = "UTC"
) -> str:
    """
    Calculate detailed compatibility scoring (0-100) between two people.
    Returns overall score plus romantic, emotional, intellectual, physical, and spiritual subscores.
    """
    params = {"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
              "lat": lat, "lng": lng, "tz": tz, "time_known": True,
              "systems": ["western"], "mode": "compatibility",
              "partner": {"year": partner_year, "month": partner_month, "day": partner_day,
                          "hour": partner_hour, "minute": partner_minute,
                          "lat": partner_lat, "lng": partner_lng, "tz": partner_tz,
                          "time_known": True}}
    try:
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_navamsa(
    year: int, month: int, day: int, hour: int = 12, minute: int = 0,
    lat: float = 0.0, lng: float = 0.0, tz: str = "UTC"
) -> str:
    """
    Calculate the Vedic Navamsa (D9) divisional chart.
    Reveals soul-level strengths, relationship potential, and vargottama status.
    """
    params = {"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
              "lat": lat, "lng": lng, "tz": tz, "time_known": True,
              "systems": ["vedic"], "mode": "navamsa"}
    try:
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_panchang(
    year: int, month: int, day: int, hour: int = 12, minute: int = 0,
    lat: float = 0.0, lng: float = 0.0, tz: str = "UTC"
) -> str:
    """
    Calculate complete Vedic Panchang elements: Tithi, Nakshatra, Yoga, and Karana.
    Essential for muhurta (auspicious timing) and daily Vedic guidance.
    """
    params = {"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
              "lat": lat, "lng": lng, "tz": tz, "time_known": True,
              "systems": ["vedic"], "mode": "panchang"}
    try:
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_moon_phase(
    year: int = None, month: int = None, day: int = None,
    hour: int = 12, minute: int = 0, tz: str = "UTC"
) -> str:
    """
    Get the current moon phase (or for a specific date): name, illumination %, age,
    and the next 4 upcoming lunar phase events (new moons, full moons, quarters).
    """
    from datetime import datetime as dt
    if year and month and day:
        params = {"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
                  "lat": 0, "lng": 0, "tz": tz, "time_known": True,
                  "systems": ["western"], "mode": "moon_phase"}
    else:
        now = dt.utcnow()
        params = {"year": now.year, "month": now.month, "day": now.day,
                  "hour": now.hour, "minute": now.minute,
                  "lat": 0, "lng": 0, "tz": "UTC", "time_known": True,
                  "systems": ["western"], "mode": "moon_phase"}
    try:
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_numerology(
    year: int, month: int, day: int, full_name: str = ""
) -> str:
    """
    Calculate core numerology: Life Path number, Personal Year, and
    (if name provided) Expression and Soul Urge numbers.
    Master numbers 11/22/33 are preserved (not reduced).
    """
    params = {"year": year, "month": month, "day": day,
              "hour": 12, "minute": 0, "lat": 0, "lng": 0, "tz": "UTC",
              "time_known": False, "systems": ["western"], "mode": "numerology"}
    if full_name:
        params["full_name"] = full_name
    try:
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_composite_chart(
    year: int, month: int, day: int, hour: int = 12, minute: int = 0,
    lat: float = 0.0, lng: float = 0.0, tz: str = "UTC",
    partner_year: int = None, partner_month: int = None, partner_day: int = None,
    partner_hour: int = 12, partner_minute: int = 0,
    partner_lat: float = 0.0, partner_lng: float = 0.0, partner_tz: str = "UTC"
) -> str:
    """
    Calculate a midpoint composite chart — the relationship as a third entity.
    Each planet is the midpoint of its positions in both charts.
    """
    params = {"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
              "lat": lat, "lng": lng, "tz": tz, "time_known": True,
              "systems": ["western"], "mode": "composite",
              "partner": {"year": partner_year, "month": partner_month, "day": partner_day,
                          "hour": partner_hour, "minute": partner_minute,
                          "lat": partner_lat, "lng": partner_lng, "tz": partner_tz,
                          "time_known": True}}
    try:
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_progressions(
    year: int, month: int, day: int, hour: int = 12, minute: int = 0,
    lat: float = 0.0, lng: float = 0.0, tz: str = "UTC",
    target_age: int = 30
) -> str:
    """
    Calculate secondary progressions (1 day = 1 year of life).
    Reveals evolving identity, emotional needs, and life direction.
    """
    params = {"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
              "lat": lat, "lng": lng, "tz": tz, "time_known": True,
              "systems": ["western"], "mode": "progressions", "target_age": target_age}
    try:
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_planetary_return(
    year: int, month: int, day: int, hour: int = 12, minute: int = 0,
    lat: float = 0.0, lng: float = 0.0, tz: str = "UTC",
    planet: str = "Jupiter", target_year: int = None
) -> str:
    """
    Calculate a planetary return chart for any planet (Mercury, Venus, Mars, Jupiter, Saturn, etc.).
    The moment the planet returns to its natal position, beginning a new cycle.
    """
    params = {"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
              "lat": lat, "lng": lng, "tz": tz, "time_known": True,
              "systems": ["western"], "mode": "planetary_return",
              "planet": planet, "target_year": target_year or year + 1}
    try:
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_varga(
    year: int, month: int, day: int, hour: int = 12, minute: int = 0,
    lat: float = 0.0, lng: float = 0.0, tz: str = "UTC",
    varga: str = "D10"
) -> str:
    """
    Calculate a Vedic divisional chart (Varga). D2=Hora (wealth), D3=Drekkana (siblings),
    D7=Saptamsa (children), D9=Navamsa (marriage), D10=Dasamsa (career), D12=Dwadashamsa (parents).
    Supports D2 through D60.
    """
    params = {"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
              "lat": lat, "lng": lng, "tz": tz, "time_known": True,
              "systems": ["vedic"], "mode": "varga", "varga": varga}
    try:
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_planetary_hours(
    year: int, month: int, day: int, hour: int = 12, minute: int = 0,
    lat: float = 0.0, lng: float = 0.0, tz: str = "UTC"
) -> str:
    """
    Calculate Chaldean planetary hours for a given day and location.
    Each hour is ruled by a planet in sequence — useful for electional timing.
    """
    params = {"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
              "lat": lat, "lng": lng, "tz": tz, "time_known": True,
              "systems": ["western"], "mode": "planetary_hours"}
    try:
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_transit_aspects(
    year: int, month: int, day: int, hour: int = 12, minute: int = 0,
    lat: float = 0.0, lng: float = 0.0, tz: str = "UTC",
    transit_date: str = None
) -> str:
    """
    Get detailed transit-to-natal aspects with impact ratings (high/moderate/low).
    Shows which transiting planets are affecting which natal planets and how strongly.
    Defaults to today's transits.
    """
    params = {"year": year, "month": month, "day": day, "hour": hour, "minute": minute,
              "lat": lat, "lng": lng, "tz": tz, "time_known": True,
              "systems": ["western"], "mode": "transit_natal_aspects",
              "transit_date": transit_date or ""}
    try:
        result = astro_engine.calculate_full_profile(params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    # Transport is env-driven so the same image works for stdio (local) and
    # sse/http (cloud). Default to stdio for backward compatibility.
    transport = os.environ.get("ASTRO_MCP_TRANSPORT", "stdio").lower()
    # Normalize friendly aliases to the literals FastMCP.run accepts.
    if transport in ("http", "streamable-http", "streamable_http"):
        transport = "streamable-http"
    if transport not in ("stdio", "sse", "streamable-http"):
        print(f"Unknown ASTRO_MCP_TRANSPORT={transport!r}, falling back to stdio", file=sys.stderr)
        transport = "stdio"
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("astrology-mcp").info(
        "Starting Astrology MCP server (transport=%s, host=%s, port=%s)",
        transport, _MCP_HOST, _MCP_PORT,
    )
    # host/port are configured on the FastMCP constructor above (mcp.settings);
    # run() only accepts transport + mount_path.
    mcp.run(transport=transport)
