#!/usr/bin/env python3
"""
Weather MCP Server
A Model Context Protocol server for weather data retrieval
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import httpx
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherMCPServer:
    def __init__(self, api_key: str, base_url: str = "http://api.weatherapi.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.server = Server("weather-mcp-server")
        self.setup_handlers()
        
    def setup_handlers(self):
        """Setup MCP server handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            """List available weather tools"""
            return ListToolsResult(
                tools=[
                    Tool(
                        name="get_current_weather",
                        description="Get current weather conditions for a location",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "City name, coordinates (lat,lon), or postal code"
                                },
                                "include_air_quality": {
                                    "type": "boolean",
                                    "description": "Include air quality data",
                                    "default": False
                                }
                            },
                            "required": ["location"]
                        }
                    ),
                    Tool(
                        name="get_weather_forecast",
                        description="Get weather forecast for a location",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "City name, coordinates (lat,lon), or postal code"
                                },
                                "days": {
                                    "type": "integer",
                                    "description": "Number of forecast days (1-10)",
                                    "default": 3,
                                    "minimum": 1,
                                    "maximum": 10
                                },
                                "include_air_quality": {
                                    "type": "boolean",
                                    "description": "Include air quality data",
                                    "default": False
                                }
                            },
                            "required": ["location"]
                        }
                    ),
                    Tool(
                        name="get_weather_history",
                        description="Get historical weather data for a location",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "City name, coordinates (lat,lon), or postal code"
                                },
                                "date": {
                                    "type": "string",
                                    "description": "Date in YYYY-MM-DD format"
                                },
                                "end_date": {
                                    "type": "string",
                                    "description": "End date in YYYY-MM-DD format (optional)"
                                }
                            },
                            "required": ["location", "date"]
                        }
                    ),
                    Tool(
                        name="search_locations",
                        description="Search for locations by name",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Location name to search for"
                                }
                            },
                            "required": ["query"]
                        }
                    ),
                    Tool(
                        name="get_astronomy_data",
                        description="Get astronomy data (sunrise, sunset, moon phase) for a location",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "City name, coordinates (lat,lon), or postal code"
                                },
                                "date": {
                                    "type": "string",
                                    "description": "Date in YYYY-MM-DD format (optional, defaults to today)"
                                }
                            },
                            "required": ["location"]
                        }
                    )
                ]
            )
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls"""
            try:
                if name == "get_current_weather":
                    return await self._get_current_weather(arguments)
                elif name == "get_weather_forecast":
                    return await self._get_weather_forecast(arguments)
                elif name == "get_weather_history":
                    return await self._get_weather_history(arguments)
                elif name == "search_locations":
                    return await self._search_locations(arguments)
                elif name == "get_astronomy_data":
                    return await self._get_astronomy_data(arguments)
                else:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"Unknown tool: {name}")]
                    )
            except Exception as e:
                logger.error(f"Error calling tool {name}: {str(e)}")
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")]
                )
    
    async def _make_api_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request to weather service"""
        params["key"] = self.api_key
        
        # Disable reading proxy settings from environment to avoid errors when
        # SOCKS proxies are configured (e.g., ALL_PROXY=socks://...). OpenAI Agent
        # Builder/containers may inherit such env vars.
        async with httpx.AsyncClient(trust_env=False) as client:
            try:
                response = await client.get(f"{self.base_url}/{endpoint}", params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"API request failed: {e.response.status_code} - {e.response.text}")
            except httpx.RequestError as e:
                raise Exception(f"Request error: {str(e)}")
    
    async def _get_current_weather(self, args: Dict[str, Any]) -> CallToolResult:
        """Get current weather conditions"""
        location = args["location"]
        include_air_quality = args.get("include_air_quality", False)
        
        params = {"q": location}
        if include_air_quality:
            params["aqi"] = "yes"
        
        data = await self._make_api_request("current.json", params)
        
        # Format the response
        weather_info = self._format_current_weather(data)
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(weather_info, indent=2)
                )
            ]
        )
    
    async def _get_weather_forecast(self, args: Dict[str, Any]) -> CallToolResult:
        """Get weather forecast"""
        location = args["location"]
        days = args.get("days", 3)
        include_air_quality = args.get("include_air_quality", False)
        
        params = {"q": location, "days": days}
        if include_air_quality:
            params["aqi"] = "yes"
        
        data = await self._make_api_request("forecast.json", params)
        
        # Format the response
        forecast_info = self._format_forecast(data)
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(forecast_info, indent=2)
                )
            ]
        )
    
    async def _get_weather_history(self, args: Dict[str, Any]) -> CallToolResult:
        """Get historical weather data"""
        location = args["location"]
        date = args["date"]
        end_date = args.get("end_date")
        
        params = {"q": location, "dt": date}
        if end_date:
            params["end_dt"] = end_date
        
        data = await self._make_api_request("history.json", params)
        
        # Format the response
        history_info = self._format_history(data)
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(history_info, indent=2)
                )
            ]
        )
    
    async def _search_locations(self, args: Dict[str, Any]) -> CallToolResult:
        """Search for locations"""
        query = args["query"]
        
        params = {"q": query}
        data = await self._make_api_request("search.json", params)
        
        # Format the response
        locations = []
        for location in data:
            locations.append({
                "id": location.get("id"),
                "name": location.get("name"),
                "region": location.get("region"),
                "country": location.get("country"),
                "lat": location.get("lat"),
                "lon": location.get("lon"),
                "url": location.get("url")
            })
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps({"locations": locations}, indent=2)
                )
            ]
        )
    
    async def _get_astronomy_data(self, args: Dict[str, Any]) -> CallToolResult:
        """Get astronomy data"""
        location = args["location"]
        date = args.get("date", datetime.now().strftime("%Y-%m-%d"))
        
        params = {"q": location, "dt": date}
        data = await self._make_api_request("astronomy.json", params)
        
        # Format the response
        astronomy_info = self._format_astronomy(data)
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=json.dumps(astronomy_info, indent=2)
                )
            ]
        )
    
    def _format_current_weather(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format current weather data"""
        location = data.get("location", {})
        current = data.get("current", {})
        condition = current.get("condition", {})
        
        return {
            "location": {
                "name": location.get("name"),
                "region": location.get("region"),
                "country": location.get("country"),
                "coordinates": {
                    "latitude": location.get("lat"),
                    "longitude": location.get("lon")
                },
                "timezone": location.get("tz_id"),
                "local_time": location.get("localtime")
            },
            "current_weather": {
                "temperature": {
                    "celsius": current.get("temp_c"),
                    "fahrenheit": current.get("temp_f"),
                    "feels_like_c": current.get("feelslike_c"),
                    "feels_like_f": current.get("feelslike_f")
                },
                "condition": {
                    "text": condition.get("text"),
                    "icon": condition.get("icon"),
                    "code": condition.get("code")
                },
                "wind": {
                    "speed_mph": current.get("wind_mph"),
                    "speed_kph": current.get("wind_kph"),
                    "direction": current.get("wind_dir"),
                    "degree": current.get("wind_degree"),
                    "gust_mph": current.get("gust_mph"),
                    "gust_kph": current.get("gust_kph")
                },
                "atmosphere": {
                    "pressure_mb": current.get("pressure_mb"),
                    "pressure_in": current.get("pressure_in"),
                    "humidity": current.get("humidity"),
                    "cloud_cover": current.get("cloud"),
                    "visibility_km": current.get("vis_km"),
                    "visibility_miles": current.get("vis_miles"),
                    "uv_index": current.get("uv")
                },
                "precipitation": {
                    "mm": current.get("precip_mm"),
                    "inches": current.get("precip_in")
                },
                "is_day": current.get("is_day") == 1,
                "last_updated": current.get("last_updated")
            },
            "air_quality": data.get("air_quality", {})
        }
    
    def _format_forecast(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format forecast data"""
        location = data.get("location", {})
        forecast = data.get("forecast", {})
        
        formatted_forecast = {
            "location": {
                "name": location.get("name"),
                "region": location.get("region"),
                "country": location.get("country"),
                "coordinates": {
                    "latitude": location.get("lat"),
                    "longitude": location.get("lon")
                }
            },
            "forecast": []
        }
        
        for day in forecast.get("forecastday", []):
            day_data = {
                "date": day.get("date"),
                "day": {
                    "max_temp_c": day.get("day", {}).get("maxtemp_c"),
                    "max_temp_f": day.get("day", {}).get("maxtemp_f"),
                    "min_temp_c": day.get("day", {}).get("mintemp_c"),
                    "min_temp_f": day.get("day", {}).get("mintemp_f"),
                    "avg_temp_c": day.get("day", {}).get("avgtemp_c"),
                    "avg_temp_f": day.get("day", {}).get("avgtemp_f"),
                    "condition": day.get("day", {}).get("condition", {}),
                    "max_wind_mph": day.get("day", {}).get("maxwind_mph"),
                    "max_wind_kph": day.get("day", {}).get("maxwind_kph"),
                    "total_precip_mm": day.get("day", {}).get("totalprecip_mm"),
                    "total_precip_in": day.get("day", {}).get("totalprecip_in"),
                    "avg_humidity": day.get("day", {}).get("avghumidity"),
                    "avg_visibility_km": day.get("day", {}).get("avgvis_km"),
                    "avg_visibility_miles": day.get("day", {}).get("avgvis_miles"),
                    "uv_index": day.get("day", {}).get("uv")
                },
                "hourly": []
            }
            
            for hour in day.get("hour", []):
                hour_data = {
                    "time": hour.get("time"),
                    "temp_c": hour.get("temp_c"),
                    "temp_f": hour.get("temp_f"),
                    "condition": hour.get("condition", {}),
                    "wind_mph": hour.get("wind_mph"),
                    "wind_kph": hour.get("wind_kph"),
                    "wind_dir": hour.get("wind_dir"),
                    "pressure_mb": hour.get("pressure_mb"),
                    "precip_mm": hour.get("precip_mm"),
                    "humidity": hour.get("humidity"),
                    "cloud": hour.get("cloud"),
                    "feelslike_c": hour.get("feelslike_c"),
                    "feelslike_f": hour.get("feelslike_f"),
                    "will_it_rain": hour.get("will_it_rain"),
                    "chance_of_rain": hour.get("chance_of_rain"),
                    "will_it_snow": hour.get("will_it_snow"),
                    "chance_of_snow": hour.get("chance_of_snow"),
                    "vis_km": hour.get("vis_km"),
                    "vis_miles": hour.get("vis_miles"),
                    "gust_mph": hour.get("gust_mph"),
                    "gust_kph": hour.get("gust_kph"),
                    "uv": hour.get("uv")
                }
                day_data["hourly"].append(hour_data)
            
            formatted_forecast["forecast"].append(day_data)
        
        return formatted_forecast
    
    def _format_history(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format historical weather data"""
        location = data.get("location", {})
        forecast = data.get("forecast", {})
        
        return {
            "location": {
                "name": location.get("name"),
                "region": location.get("region"),
                "country": location.get("country")
            },
            "historical_data": forecast.get("forecastday", [])
        }
    
    def _format_astronomy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format astronomy data"""
        location = data.get("location", {})
        astronomy = data.get("astronomy", {})
        astro = astronomy.get("astro", {})
        
        return {
            "location": {
                "name": location.get("name"),
                "region": location.get("region"),
                "country": location.get("country")
            },
            "astronomy": {
                "sunrise": astro.get("sunrise"),
                "sunset": astro.get("sunset"),
                "moonrise": astro.get("moonrise"),
                "moonset": astro.get("moonset"),
                "moon_phase": astro.get("moon_phase"),
                "moon_illumination": astro.get("moon_illumination")
            }
        }
    
    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    capabilities={"tools": {}},
                    server_name="weather-mcp-server",
                    server_version="1.0.0"
                )
            )

async def main():
    """Main entry point"""
    import os
    
    # Get API key from environment variable
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        logger.error("WEATHER_API_KEY environment variable is required")
        return
    
    server = WeatherMCPServer(api_key)
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
