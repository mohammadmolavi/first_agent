#!/usr/bin/env python3
"""
HTTP bridge for Weather MCP Server tools so they can be used from
platforms that require HTTP/OpenAPI (e.g., OpenAI Agent Builder Actions).

Exposes REST endpoints that mirror the MCP tools and reuse the same
formatting logic from WeatherMCPServer.
"""

import os
import asyncio
from typing import Any, Dict, Optional

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

# Local import of the existing MCP server to reuse formatting logic
from weather_mcp_server import WeatherMCPServer  # type: ignore


def get_api_key() -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("WEATHER_API_KEY environment variable is required")
    return api_key


app = FastAPI(
    title="Weather Tools HTTP Bridge",
    version="1.0.0",
    description="HTTP wrapper for Weather MCP tools, suitable for OpenAI Agent Builder Actions."
)


async def fetch(server: WeatherMCPServer, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Call the upstream weather API using the same method the MCP server uses."""
    try:
        return await server._make_api_request(endpoint, params)  # noqa: SLF001
    except Exception as exc:  # pragma: no cover - passthrough to HTTP error
        raise HTTPException(status_code=502, detail=str(exc))


def create_server() -> WeatherMCPServer:
    return WeatherMCPServer(api_key=get_api_key())


@app.get("/healthz")
async def healthz() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.get("/get_current_weather")
async def get_current_weather(
    location: str = Query(..., description="City name, coordinates (lat,lon), or postal code"),
    include_air_quality: bool = Query(False, description="Include air quality data"),
):
    server = create_server()
    params: Dict[str, Any] = {"q": location}
    if include_air_quality:
        params["aqi"] = "yes"
    data = await fetch(server, "current.json", params)
    return JSONResponse(server._format_current_weather(data))  # noqa: SLF001


@app.get("/get_weather_forecast")
async def get_weather_forecast(
    location: str = Query(..., description="City name, coordinates (lat,lon), or postal code"),
    days: int = Query(3, ge=1, le=10, description="Number of forecast days (1-10)"),
    include_air_quality: bool = Query(False, description="Include air quality data"),
):
    server = create_server()
    params: Dict[str, Any] = {"q": location, "days": days}
    if include_air_quality:
        params["aqi"] = "yes"
    data = await fetch(server, "forecast.json", params)
    return JSONResponse(server._format_forecast(data))  # noqa: SLF001


@app.get("/get_weather_history")
async def get_weather_history(
    location: str = Query(..., description="City name, coordinates (lat,lon), or postal code"),
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format (optional)"),
):
    server = create_server()
    params: Dict[str, Any] = {"q": location, "dt": date}
    if end_date:
        params["end_dt"] = end_date
    data = await fetch(server, "history.json", params)
    return JSONResponse(server._format_history(data))  # noqa: SLF001


@app.get("/search_locations")
async def search_locations(
    query: str = Query(..., description="Location name to search for"),
):
    server = create_server()
    params: Dict[str, Any] = {"q": query}
    data = await fetch(server, "search.json", params)
    # Keep response consistent with MCP formatting for locations list
    locations = []
    for loc in data:
        locations.append({
            "id": loc.get("id"),
            "name": loc.get("name"),
            "region": loc.get("region"),
            "country": loc.get("country"),
            "lat": loc.get("lat"),
            "lon": loc.get("lon"),
            "url": loc.get("url"),
        })
    return JSONResponse({"locations": locations})


@app.get("/get_astronomy_data")
async def get_astronomy_data(
    location: str = Query(..., description="City name, coordinates (lat,lon), or postal code"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format (optional, defaults to today)"),
):
    from datetime import datetime  # local import to avoid polluting module

    server = create_server()
    actual_date = date or datetime.now().strftime("%Y-%m-%d")
    params: Dict[str, Any] = {"q": location, "dt": actual_date}
    data = await fetch(server, "astronomy.json", params)
    return JSONResponse(server._format_astronomy(data))  # noqa: SLF001


# Entrypoint for local dev: uvicorn http_bridge:app --host 0.0.0.0 --port 8000


