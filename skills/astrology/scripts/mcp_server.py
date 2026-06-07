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

if __name__ == "__main__":
    # Ensure sys.stdout is cleanly reserved for the MCP protocol when running stdio
    mcp.run(transport="stdio")
