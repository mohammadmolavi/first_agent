#!/usr/bin/env python3
"""
Main entry point for Railway deployment
This ensures the server starts even if API key is missing initially
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import app - this might fail but we'll handle it
try:
    from http_bridge import app
except Exception as e:
    print(f"Error importing app: {e}", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    
    # Get port from Railway environment variable
    # Railway sets PORT automatically, default to 8000 if not set
    port_str = os.getenv("PORT", "8000")
    try:
        port = int(port_str)
    except ValueError:
        print(f"Invalid PORT value: {port_str}, using 8000", file=sys.stderr)
        port = 8000
    
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting server on {host}:{port}", file=sys.stderr)
    print(f"API Key configured: {bool(os.getenv('WEATHER_API_KEY'))}", file=sys.stderr)
    
    # Start server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

