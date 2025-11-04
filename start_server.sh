#!/bin/bash
# Simple startup script for Weather MCP Server HTTP Bridge

# Check if API key is set
if [ -z "$WEATHER_API_KEY" ]; then
    echo "Error: WEATHER_API_KEY environment variable is not set"
    echo "Please set it with: export WEATHER_API_KEY='your_key_here'"
    exit 1
fi

# Check if port is already in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "Port 8000 is already in use. Please stop the other service or use a different port."
    exit 1
fi

echo "Starting Weather MCP Server HTTP Bridge..."
echo "Server will be available at: http://localhost:8000"
echo "Health check: http://localhost:8000/healthz"
echo "OpenAPI schema: http://localhost:8000/openapi.json"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn http_bridge:app --host 0.0.0.0 --port 8000

