#!/usr/bin/env python3
"""
HTTP/SSE bridge for MCP server to work with OpenAI Agent Builder
Exposes MCP server over HTTP using Server-Sent Events (SSE)
"""

import os
import json
import asyncio
import logging
from typing import Any, Dict

# Configure logging early so it's available for import-time warnings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mcp.server import Server
from mcp.server.models import InitializationOptions
# MCP SSE transport - check if available
try:
    from mcp.server.sse import SseServerTransport
    SSE_AVAILABLE = True
except ImportError:
    SSE_AVAILABLE = False
    logger.warning("MCP SSE transport not available, using REST endpoints only")
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)

from weather_mcp_server import WeatherMCPServer

# Also import HTTP bridge endpoints for OpenAPI Actions
try:
    from http_bridge import app as http_app
    # Import the weather endpoints from http_bridge
    HTTP_BRIDGE_AVAILABLE = True
except ImportError:
    HTTP_BRIDGE_AVAILABLE = False
    logger.warning("HTTP bridge not available")

app = FastAPI(
    title="Weather MCP Server HTTP Bridge",
    version="1.0.0",
    description="HTTP/SSE bridge for Weather MCP Server to work with OpenAI Agent Builder"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global server instance
weather_server: WeatherMCPServer = None


def get_api_key() -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("WEATHER_API_KEY environment variable is required")
    return api_key


@app.on_event("startup")
async def startup():
    """Initialize the weather server on startup"""
    global weather_server
    try:
        api_key = get_api_key()
        weather_server = WeatherMCPServer(api_key)
        logger.info("Weather MCP Server initialized")
    except Exception as e:
        logger.error(f"Failed to initialize server: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse({
        "status": "ok",
        "service": "Weather MCP Server HTTP Bridge",
        "version": "1.0.0",
        "mcp_endpoint": "/mcp"
    })


@app.get("/healthz")
async def healthz():
    """Health check"""
    return JSONResponse({"status": "ok"})


@app.get("/mcp")
async def mcp_sse_endpoint(request: Request):
    """
    MCP Server-Sent Events endpoint for OpenAI Agent Builder
    This exposes the MCP server over HTTP/SSE
    """
    if weather_server is None:
        return JSONResponse(
            {"error": "Server not initialized"},
            status_code=503
        )
    
    if not SSE_AVAILABLE:
        return JSONResponse(
            {"error": "SSE transport not available. Use /mcp/list_tools and /mcp/call_tool endpoints instead."},
            status_code=501
        )
    
    async def event_stream():
        """Stream MCP events using SSE"""
        try:
            # Create SSE transport
            transport = SseServerTransport("/mcp")
            
            # Initialize the server
            init_options = InitializationOptions(
                capabilities={"tools": {}},
                server_name="weather-mcp-server",
                server_version="1.0.0"
            )
            
            # Run the server with SSE transport
            async with transport.connect_sse(request) as streams:
                await weather_server.server.run(
                    streams[0],
                    streams[1],
                    init_options
                )
                
        except Exception as e:
            logger.error(f"MCP SSE error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.post("/mcp/list_tools")
async def list_tools():
    """List available tools (REST endpoint for convenience)"""
    if weather_server is None:
        return JSONResponse(
            {"error": "Server not initialized"},
            status_code=503
        )
    
    try:
        # Get tools from the server
        tools_result = await weather_server.server.list_tools()
        return JSONResponse({
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema
                }
                for tool in tools_result.tools
            ]
        })
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )


@app.post("/mcp/call_tool")
async def call_tool(request_data: Dict[str, Any]):
    """Call a tool (REST endpoint for convenience)"""
    if weather_server is None:
        return JSONResponse(
            {"error": "Server not initialized"},
            status_code=503
        )
    
    try:
        tool_name = request_data.get("name")
        arguments = request_data.get("arguments", {})
        
        if not tool_name:
            return JSONResponse(
                {"error": "Tool name is required"},
                status_code=400
            )
        
        # Call the tool
        result = await weather_server.server.call_tool(tool_name, arguments)
        
        # Extract text content
        content = []
        for item in result.content:
            if hasattr(item, 'text'):
                content.append(item.text)
            elif isinstance(item, dict) and 'text' in item:
                content.append(item['text'])
        
        return JSONResponse({
            "content": content,
            "isError": result.isError if hasattr(result, 'isError') else False
        })
    except Exception as e:
        logger.error(f"Error calling tool: {e}")
        return JSONResponse(
            {"error": str(e)},
            status_code=500
        )


# Include HTTP bridge endpoints for OpenAPI Actions compatibility
if HTTP_BRIDGE_AVAILABLE:
    # Mount HTTP bridge routes (but exclude root/healthz to avoid conflicts)
    from fastapi import APIRouter
    http_router = APIRouter()
    
    # Get routes from http_app that we want to include
    for route in http_app.routes:
        if hasattr(route, 'path') and route.path not in ['/', '/healthz']:
            # Add the route to our app
            app.add_api_route(
                route.path,
                route.endpoint,
                methods=route.methods if hasattr(route, 'methods') else ['GET'],
                name=route.name if hasattr(route, 'name') else None,
                include_in_schema=True
            )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

