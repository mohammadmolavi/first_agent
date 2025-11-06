# OpenAI Agent Builder Setup - IMPORTANT

## The Error You're Seeing

```
Error retrieving tool list from MCP server: 'my_weather_mcp_server'. 
Http status code: 424 (Failed Dependency).
```

This error means Agent Builder is trying to connect to an **MCP server**, but you need to use **HTTP Actions** instead.

## Two Different Things

### 1. MCP Server (NOT for Agent Builder)
- File: `weather_mcp_server.py`
- Protocol: stdio (not HTTP)
- For: Cursor, Claude Desktop, other MCP clients
- **Does NOT work with OpenAI Agent Builder**

### 2. HTTP Bridge (FOR Agent Builder) ✅
- File: `http_bridge.py`
- Protocol: HTTP/REST
- For: OpenAI Agent Builder Actions
- **This is what you need!**

## Correct Setup for Agent Builder

### Step 1: Use the HTTP Bridge URL

Your HTTP bridge is deployed at:
```
https://web-production-73dc9.up.railway.app/
```

### Step 2: Import as OpenAPI Action (NOT MCP)

1. Go to OpenAI Agent Builder
2. Go to **Actions** (NOT MCP servers)
3. Click **"Import from OpenAPI URL"**
4. Enter:
   ```
   https://web-production-73dc9.up.railway.app/openapi.json
   ```
5. Click **Import**

### Step 3: Verify It Works

After importing, you should see 5 weather tools:
- get_current_weather
- get_weather_forecast
- get_weather_history
- search_locations
- get_astronomy_data

## Common Mistakes

❌ **DON'T** try to add it as an MCP server
❌ **DON'T** use `weather_mcp_server.py` 
❌ **DON'T** use stdio protocol

✅ **DO** use the HTTP bridge (`http_bridge.py`)
✅ **DO** import via OpenAPI URL
✅ **DO** use Actions section, not MCP section

## Test Your Server

```bash
# Test the OpenAPI schema
curl https://web-production-73dc9.up.railway.app/openapi.json

# Test an endpoint
curl -X POST https://web-production-73dc9.up.railway.app/get_current_weather \
  -H "Content-Type: application/json" \
  -d '{"location": "Nahavand"}'
```

## If Still Not Working

1. Make sure you're in **Actions** section, not MCP
2. Use the OpenAPI URL, not the server URL
3. Check Railway logs to ensure server is running
4. Verify API key is set in Railway Variables

