#!/usr/bin/env python3
"""
Model Context Protocol (MCP) server wrapper for the Astrology Engine.
This allows the astrology engine to be used natively by MCP-compatible
clients like Claude Desktop, Cursor, Zed, Devin, and Antigravity.

Requires the `mcp` SDK:
  pip install mcp
"""

import sys
import json
import logging
from typing import Any, Sequence

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("ERROR: The 'mcp' package is required. Install it with: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Import the core engine
import astro_engine

# Initialize the MCP server
mcp = FastMCP("Astrology Engine")

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

if __name__ == "__main__":
    # Ensure sys.stdout is cleanly reserved for the MCP protocol when running locally.
    # To monetize and host this as an API, change transport to "sse" or run via FastMCP CLI:
    # fastmcp dev mcp_server.py:mcp
    mcp.run(transport="stdio")
