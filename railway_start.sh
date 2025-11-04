#!/bin/bash
# Railway startup script that handles PORT environment variable

# Get port from Railway or default to 8000
PORT=${PORT:-8000}

# Start uvicorn with proper configuration
exec uvicorn http_bridge:app --host 0.0.0.0 --port $PORT

