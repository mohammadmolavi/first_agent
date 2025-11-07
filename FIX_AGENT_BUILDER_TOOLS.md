# Quick Fix: Agent Builder Can't Use Tools

## Problem
OpenAI Agent Builder can't see the tools because the server is using the MCP bridge instead of the HTTP bridge.

## Solution
The server needs to use `http_bridge.py` (not `mcp_http_bridge.py`) to expose weather endpoints in the OpenAPI schema.

## What Was Fixed

1. **Changed `main.py`** to use `http_bridge.py` first (for OpenAPI Actions)
2. **HTTP bridge** exposes these endpoints in OpenAPI:
   - `/get_current_weather` ✅
   - `/get_weather_forecast` ✅
   - `/get_weather_history` ✅
   - `/search_locations` ✅
   - `/get_astronomy_data` ✅

3. **MCP bridge** is still available but not used by default

## After Deploy

1. **Push to GitHub** (if not already done)
2. **Wait for Railway to redeploy** (1-2 minutes)
3. **Test OpenAPI schema**:
   ```bash
   curl https://web-production-73dc9.up.railway.app/openapi.json | python3 -c "import sys, json; d=json.load(sys.stdin); print('Weather endpoints:', [p for p in d.get('paths', {}) if 'weather' in p or 'forecast' in p or 'astronomy' in p or 'location' in p])"
   ```

4. **In Agent Builder**:
   - Go to Actions → Import from OpenAPI URL
   - Use: `https://web-production-73dc9.up.railway.app/openapi.json`
   - Should now see 5 weather tools!

## Expected Result

After redeploy, the OpenAPI schema should show:
- `/get_current_weather` (POST)
- `/get_weather_forecast` (POST)
- `/get_weather_history` (POST)
- `/search_locations` (POST)
- `/get_astronomy_data` (POST)

These will appear as tools in Agent Builder!

