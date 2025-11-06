#!/usr/bin/env python3
"""
HTTP bridge for Weather MCP Server tools so they can be used from
platforms that require HTTP/OpenAPI (e.g., OpenAI Agent Builder Actions).

Exposes REST endpoints that mirror the MCP tools and reuse the same
formatting logic from WeatherMCPServer.
"""

import os
import asyncio
import logging
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

import httpx
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import weather server - delay import to avoid startup errors
try:
    from weather_mcp_server import WeatherMCPServer  # type: ignore
except ImportError as e:
    logger.error(f"Failed to import WeatherMCPServer: {e}")
    WeatherMCPServer = None


def get_api_key() -> str:
    """Get API key from environment, with better error message"""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "WEATHER_API_KEY environment variable is required. "
            "Please set it in Railway Variables section."
        )
    return api_key


app = FastAPI(
    title="Weather Tools HTTP Bridge",
    version="1.0.0",
    description="HTTP wrapper for Weather MCP tools, suitable for OpenAI Agent Builder Actions.",
    servers=[
        {
            "url": "https://web-production-73dc9.up.railway.app",
            "description": "Production server"
        }
    ]
)

# Customize OpenAPI schema for OpenAI Agent Builder
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    from fastapi.openapi.utils import get_openapi
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        servers=app.servers,
    )
    
    # Ensure all endpoints have proper operationId and tags
    for path, methods in openapi_schema.get("paths", {}).items():
        for method, details in methods.items():
            if isinstance(details, dict):
                # Add tags if missing
                if "tags" not in details:
                    details["tags"] = ["weather"]
                # Ensure operationId exists
                if "operationId" not in details:
                    details["operationId"] = f"{method}_{path.replace('/', '_').replace('-', '_')}"
                # Add better descriptions
                if "summary" not in details:
                    details["summary"] = details.get("description", "Weather API endpoint")
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Add CORS middleware for OpenAI Agent Builder
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models for OpenAI Agent Builder
class WeatherRequest(BaseModel):
    location: str = Field(..., description="City name, coordinates (lat,lon), or postal code")
    include_air_quality: Optional[bool] = Field(False, description="Include air quality data")

class ForecastRequest(BaseModel):
    location: str = Field(..., description="City name, coordinates (lat,lon), or postal code")
    days: Optional[int] = Field(3, ge=1, le=10, description="Number of forecast days (1-10)")
    include_air_quality: Optional[bool] = Field(False, description="Include air quality data")

class HistoryRequest(BaseModel):
    location: str = Field(..., description="City name, coordinates (lat,lon), or postal code")
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    end_date: Optional[str] = Field(None, description="End date in YYYY-MM-DD format (optional)")

class SearchRequest(BaseModel):
    query: str = Field(..., description="Location name to search for")

class AstronomyRequest(BaseModel):
    location: str = Field(..., description="City name, coordinates (lat,lon), or postal code")
    date: Optional[str] = Field(None, description="Date in YYYY-MM-DD format (optional, defaults to today)")


async def fetch(server, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Call the upstream weather API using the same method the MCP server uses."""
    if server is None:
        raise HTTPException(
            status_code=503,
            detail="Weather server not initialized. Check server logs."
        )
    try:
        return await server._make_api_request(endpoint, params)  # noqa: SLF001
    except Exception as exc:  # pragma: no cover - passthrough to HTTP error
        raise HTTPException(status_code=502, detail=str(exc))


def create_server() -> WeatherMCPServer:
    """Create weather server instance, with error handling"""
    if WeatherMCPServer is None:
        raise HTTPException(
            status_code=503,
            detail="Weather server module not available. Check server logs."
        )
    try:
        return WeatherMCPServer(api_key=get_api_key())
    except RuntimeError as e:
        logger.error(f"Failed to create server: {e}")
        raise HTTPException(
            status_code=503,
            detail=str(e)
        )


@app.get("/", include_in_schema=False)
async def root() -> JSONResponse:
    """Root endpoint for health checks - doesn't require API key"""
    api_key_set = bool(os.getenv("WEATHER_API_KEY"))
    return JSONResponse({
        "status": "ok",
        "service": "Weather MCP Server",
        "version": "1.0.0",
        "api_key_configured": api_key_set
    })


@app.get("/healthz", include_in_schema=False)
async def healthz() -> JSONResponse:
    """Health check endpoint - doesn't require API key"""
    return JSONResponse({"status": "ok"})


@app.post(
    "/get_current_weather",
    summary="Get Current Weather",
    description="Get current weather conditions for any location",
    tags=["weather"],
    response_description="Current weather data for the specified location"
)
async def get_current_weather(request: WeatherRequest = Body(...)):
    server = create_server()
    params: Dict[str, Any] = {"q": request.location}
    if request.include_air_quality:
        params["aqi"] = "yes"
    data = await fetch(server, "current.json", params)
    return JSONResponse(server._format_current_weather(data))  # noqa: SLF001


@app.post(
    "/get_weather_forecast",
    summary="Get Weather Forecast",
    description="Get weather forecast for 1-10 days",
    tags=["weather"],
    response_description="Weather forecast data"
)
async def get_weather_forecast(request: ForecastRequest = Body(...)):
    server = create_server()
    params: Dict[str, Any] = {"q": request.location, "days": request.days}
    if request.include_air_quality:
        params["aqi"] = "yes"
    data = await fetch(server, "forecast.json", params)
    return JSONResponse(server._format_forecast(data))  # noqa: SLF001


@app.post(
    "/get_weather_history",
    summary="Get Weather History",
    description="Get historical weather data for specific dates",
    tags=["weather"],
    response_description="Historical weather data"
)
async def get_weather_history(request: HistoryRequest = Body(...)):
    server = create_server()
    params: Dict[str, Any] = {"q": request.location, "dt": request.date}
    if request.end_date:
        params["end_dt"] = request.end_date
    data = await fetch(server, "history.json", params)
    return JSONResponse(server._format_history(data))  # noqa: SLF001


@app.post(
    "/search_locations",
    summary="Search Locations",
    description="Search for locations by name",
    tags=["weather"],
    response_description="List of matching locations"
)
async def search_locations(request: SearchRequest = Body(...)):
    server = create_server()
    params: Dict[str, Any] = {"q": request.query}
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


@app.post(
    "/get_astronomy_data",
    summary="Get Astronomy Data",
    description="Get sunrise, sunset, moon phase, and other astronomy data",
    tags=["weather"],
    response_description="Astronomy data for the specified location"
)
async def get_astronomy_data(request: AstronomyRequest = Body(...)):
    from datetime import datetime  # local import to avoid polluting module

    server = create_server()
    actual_date = request.date or datetime.now().strftime("%Y-%m-%d")
    params: Dict[str, Any] = {"q": request.location, "dt": actual_date}
    data = await fetch(server, "astronomy.json", params)
    return JSONResponse(server._format_astronomy(data))  # noqa: SLF001


# Entrypoint for local dev: uvicorn http_bridge:app --host 0.0.0.0 --port 8000



