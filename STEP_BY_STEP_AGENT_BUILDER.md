# Step-by-Step: Using Your Server in OpenAI Agent Builder

## Your Server Information

- **Server URL**: `https://web-production-73dc9.up.railway.app/`
- **OpenAPI Schema URL**: `https://web-production-73dc9.up.railway.app/openapi.json`

## Step-by-Step Instructions

### Step 1: Open OpenAI Agent Builder

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign in to your account
3. Navigate to **Assistants** (Agent Builder)

### Step 2: Create or Edit an Agent

1. Click **"Create"** to create a new agent, OR
2. Click on an existing agent to edit it

### Step 3: Go to Actions Section

1. In your agent settings, find the **"Actions"** section
2. Look for **"Add Action"** or **"Import"** button
3. Click **"Import from OpenAPI URL"** or **"Add OpenAPI Action"**

### Step 4: Enter the OpenAPI URL

In the URL field, paste:
```
https://web-production-73dc9.up.railway.app/openapi.json
```

### Step 5: Import

1. Click **"Import"** or **"Add"**
2. Wait for OpenAI to fetch and parse the OpenAPI schema
3. You should see 5 weather tools appear:
   - `get_current_weather`
   - `get_weather_forecast`
   - `get_weather_history`
   - `search_locations`
   - `get_astronomy_data`

### Step 6: Save Your Agent

1. Click **"Save"** to save your agent configuration
2. Your agent is now ready to use weather tools!

## Visual Guide

```
OpenAI Platform
  └─> Assistants (Agent Builder)
      └─> Create/Edit Agent
          └─> Actions Tab
              └─> "Import from OpenAPI URL"
                  └─> Paste: https://web-production-73dc9.up.railway.app/openapi.json
                      └─> Click Import
                          └─> 5 tools appear ✅
```

## Testing Your Setup

### Test 1: Verify OpenAPI Schema is Accessible

```bash
curl https://web-production-73dc9.up.railway.app/openapi.json
```

Should return JSON with OpenAPI schema.

### Test 2: Test an Endpoint

```bash
curl -X POST https://web-production-73dc9.up.railway.app/get_current_weather \
  -H "Content-Type: application/json" \
  -d '{"location": "Nahavand"}'
```

Should return weather data for Nahavand.

### Test 3: Use in Agent

Once imported, try asking your agent:
- "What's the weather in Nahavand?"
- "Get a 5-day forecast for Tehran"
- "When is sunrise in London?"

## Troubleshooting

### Problem: "Failed to import" or "Invalid schema"

**Solution:**
1. Check that the OpenAPI URL is accessible:
   ```bash
   curl https://web-production-73dc9.up.railway.app/openapi.json
   ```
2. Make sure you're using the `/openapi.json` endpoint, not just the root URL
3. Check Railway logs to ensure server is running

### Problem: "No tools found"

**Solution:**
1. Verify the OpenAPI schema includes the POST endpoints
2. Check that endpoints have proper `operationId` and `tags`
3. Make sure you're importing in **Actions**, not MCP servers

### Problem: "Server not responding"

**Solution:**
1. Check Railway dashboard - is the service running?
2. Test the health endpoint:
   ```bash
   curl https://web-production-73dc9.up.railway.app/
   ```
3. Verify `WEATHER_API_KEY` is set in Railway Variables

## Quick Reference

| What | URL |
|------|-----|
| Server Root | `https://web-production-73dc9.up.railway.app/` |
| OpenAPI Schema | `https://web-production-73dc9.up.railway.app/openapi.json` |
| Health Check | `https://web-production-73dc9.up.railway.app/` |

## Example Agent Prompts

After setup, your agent can answer:

- "What's the current weather in Nahavand?"
- "Get me a 3-day forecast for Tehran"
- "What was the weather in London on January 1st, 2024?"
- "Search for weather information about Paris"
- "When does the sun rise in Tokyo today?"

The agent will automatically call the appropriate weather endpoints!

