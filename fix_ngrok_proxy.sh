#!/bin/bash
# Fix ngrok proxy issue by removing proxy settings

NGROK_CONFIG="/home/fu/snap/ngrok/315/.config/ngrok/ngrok.yml"

echo "Checking ngrok configuration..."

if [ -f "$NGROK_CONFIG" ]; then
    # Check if proxy_url exists in config
    if grep -q "proxy_url" "$NGROK_CONFIG"; then
        echo "Found proxy_url in ngrok config. Removing it..."
        # Create backup
        cp "$NGROK_CONFIG" "${NGROK_CONFIG}.backup"
        # Remove proxy_url line
        sed -i '/proxy_url/d' "$NGROK_CONFIG"
        echo "Proxy removed. Backup saved to ${NGROK_CONFIG}.backup"
    else
        echo "No proxy_url found in ngrok config."
    fi
    
    echo ""
    echo "Current ngrok config:"
    cat "$NGROK_CONFIG"
else
    echo "ngrok config file not found at $NGROK_CONFIG"
fi

echo ""
echo "Also unsetting environment proxy variables..."
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY
echo "Proxy environment variables unset for this session."

echo ""
echo "To make proxy unset permanent, add to your ~/.bashrc:"
echo "unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY"

