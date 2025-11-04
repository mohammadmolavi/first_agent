#!/bin/bash
# Startup script for Railway - ensures PORT is properly handled

# Get port from Railway or default
PORT=${PORT:-8000}

# Export for Python to read
export PORT

# Start the server
exec python main.py

