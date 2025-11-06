# Using MCP Server in OpenAI Agent Builder

## Your Server URL for MCP

**MCP Endpoint:** `https://web-production-73dc9.up.railway.app/mcp`

## Step-by-Step Setup

### Step 1: Open OpenAI Agent Builder

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Navigate to **Assistants** (Agent Builder)
3. Create a new agent or edit an existing one

### Step 2: Add MCP Server

1. In your agent settings, find the **Tools** section
2. Click **"Add Tool"**
3. Select **"MCP Server"**

### Step 3: Configure MCP Server

1. Click **"+ Server"** to add a new MCP server
2. Enter the following:
   - **URL**: `https://web-production-73dc9.up.railway.app/mcp`
   - **Name**: `weather-mcp-server` (or any name you prefer)
   - **Authentication**: Select **"No Auth"** (or configure if needed)

### Step 4: Connect

1. Click **"Connect"** to establish connection
2. Wait for Agent Builder to connect to your MCP server
3. You should see the available tools appear:
   - `get_current_weather`
   - `get_weather_forecast`
   - `get_weather_history`
   - `search_locations`
   - `get_astronomy_data`

### Step 5: Select Tools

1. Select which tools you want your agent to use
2. Click **"Save"** to save your agent configuration

## Alternative: REST Endpoints

If SSE doesn't work, you can also use the REST endpoints:

### List Tools
```bash
curl https://web-production-73dc9.up.railway.app/mcp/list_tools
```

### Call a Tool
```bash
curl -X POST https://web-production-73dc9.up.railway.app/mcp/call_tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "get_current_weather",
    "arguments": {"location": "Nahavand"}
  }'
```

## Troubleshooting

### Error: "Failed to connect"

1. Check that the server is running:
   ```bash
   curl https://web-production-73dc9.up.railway.app/
   ```

2. Verify the MCP endpoint:
   ```bash
   curl https://web-production-73dc9.up.railway.app/mcp
   ```

3. Check Railway logs for errors

### Error: "424 Failed Dependency"

- Make sure you're using the `/mcp` endpoint, not the root URL
- Verify `WEATHER_API_KEY` is set in Railway Variables
- Check that the server has redeployed after changes

## Server Information

- **Server URL**: `https://web-production-73dc9.up.railway.app/`
- **MCP Endpoint**: `https://web-production-73dc9.up.railway.app/mcp`
- **List Tools**: `https://web-production-73dc9.up.railway.app/mcp/list_tools`
- **Call Tool**: `https://web-production-73dc9.up.railway.app/mcp/call_tool`

## Test Your Setup

```bash
# Test health
curl https://web-production-73dc9.up.railway.app/

# Test list tools
curl https://web-production-73dc9.up.railway.app/mcp/list_tools

# Test calling a tool
curl -X POST https://web-production-73dc9.up.railway.app/mcp/call_tool \
  -H "Content-Type: application/json" \
  -d '{"name": "get_current_weather", "arguments": {"location": "Nahavand"}}'
```

