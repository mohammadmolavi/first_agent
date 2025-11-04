#!/bin/bash
# Script to start server with Cloudflare Tunnel (free alternative to ngrok)

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Weather MCP Server with Cloudflare Tunnel...${NC}"
echo ""

# Check if API key is set
if [ -z "$WEATHER_API_KEY" ]; then
    echo -e "${YELLOW}Warning: WEATHER_API_KEY not set${NC}"
    echo "Please set it with: export WEATHER_API_KEY='your_key_here'"
    echo ""
    read -p "Enter your WEATHER_API_KEY now (or Ctrl+C to exit): " api_key
    export WEATHER_API_KEY="$api_key"
fi

# Check if cloudflared is installed
if ! command -v cloudflared &> /dev/null; then
    echo "cloudflared is not installed."
    echo "Installing cloudflared..."
    
    # Download cloudflared
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /tmp/cloudflared
    chmod +x /tmp/cloudflared
    sudo mv /tmp/cloudflared /usr/local/bin/cloudflared
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}cloudflared installed successfully!${NC}"
    else
        echo "Failed to install cloudflared. Please install manually:"
        echo "wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
        echo "chmod +x cloudflared-linux-amd64"
        echo "sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared"
        exit 1
    fi
fi

# Check if port is in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}Port 8000 is already in use.${NC}"
    echo "Please stop the other service first."
    exit 1
fi

echo "Starting server in background..."
# Start server in background
nohup uvicorn http_bridge:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
SERVER_PID=$!

echo "Waiting for server to start..."
sleep 3

# Check if server started
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "Failed to start server. Check server.log for errors."
    exit 1
fi

echo -e "${GREEN}Server started! (PID: $SERVER_PID)${NC}"
echo ""
echo "Starting Cloudflare Tunnel..."
echo ""
echo -e "${YELLOW}Your global URL will appear below. Copy it for OpenAI Agent Builder!${NC}"
echo ""
echo "Press Ctrl+C to stop both server and tunnel"
echo ""

# Start Cloudflare Tunnel
cloudflared tunnel --url http://localhost:8000

# Cleanup on exit
echo ""
echo "Stopping server..."
kill $SERVER_PID 2>/dev/null
echo "Done!"

