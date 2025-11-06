# Fix for OpenAI Agent Builder "No Tools" Issue

## Problem
OpenAI Agent Builder shows "This server does not expose any tools" when importing the OpenAPI schema.

## Solution Applied

I've updated the OpenAPI schema to be compatible with OpenAI Agent Builder:

1. **Added server URL** to OpenAPI schema
2. **Added proper tags** to all weather endpoints
3. **Added summaries and descriptions** to all endpoints
4. **Excluded health check endpoints** from schema (they're not "tools")
5. **Custom OpenAPI function** to ensure proper formatting

## Changes Made

- All weather endpoints now have:
  - `summary` - Short description
  - `description` - Detailed description
  - `tags` - Grouped under "weather"
  - `response_description` - What the response contains

- Health check endpoints (`/` and `/healthz`) are excluded from schema

- Server URL is included in OpenAPI spec

## Next Steps

1. **Push changes to GitHub**:
   ```bash
   git add .
   git commit -m "Fix OpenAPI schema for OpenAI Agent Builder compatibility"
   git push origin main
   ```

2. **Wait for Railway to redeploy** (1-2 minutes)

3. **Test the OpenAPI schema**:
   ```bash
   curl https://web-production-73dc9.up.railway.app/openapi.json | python3 -m json.tool | grep -A 5 "paths"
   ```

4. **Try importing again in OpenAI Agent Builder**:
   - Go to Actions → Import from OpenAPI URL
   - Enter: `https://web-production-73dc9.up.railway.app/openapi.json`
   - Should now show 5 weather tools

## Expected Tools

After fix, OpenAI Agent Builder should see:
1. `get_current_weather` - Get current weather
2. `get_weather_forecast` - Get forecast
3. `get_weather_history` - Get historical data
4. `search_locations` - Search locations
5. `get_astronomy_data` - Get astronomy data

## If Still Not Working

1. Check Railway logs for errors
2. Verify OpenAPI schema is accessible
3. Try importing the schema manually to validate it
4. Check OpenAI Agent Builder documentation for any specific requirements

