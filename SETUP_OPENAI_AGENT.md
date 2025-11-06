# Setup for OpenAI Agent Builder

Your server is now running! 🎉

## Step 1: Set API Key in Railway

1. Go to your Railway dashboard
2. Click on your service (weather-mcp-server)
3. Go to **Variables** tab
4. Click **+ New Variable**
5. Add:
   - **Key**: `WEATHER_API_KEY`
   - **Value**: `56e3a9b721d94a8fac8101345252510`
6. Railway will automatically redeploy

Wait for redeploy to complete (about 1-2 minutes).

## Step 2: Get Your Server URL

From Railway dashboard, copy your service URL:
- It should be something like: `https://your-app-name.up.railway.app`
- Or check your Railway service settings for the custom domain

## Step 3: Test Your Server

After setting the API key and redeploy, test:

```bash
# Health check (should show api_key_configured: true now)
curl https://your-url.up.railway.app/

# Test an endpoint
curl "https://your-url.up.railway.app/get_current_weather?location=London"

# Get OpenAPI schema (for Agent Builder)
curl https://your-url.up.railway.app/openapi.json
```

## Step 4: Add to OpenAI Agent Builder

1. Go to [OpenAI Agent Builder](https://platform.openai.com/assistants)
2. Navigate to your agent
3. Go to **Actions** section
4. Click **"Import from OpenAPI URL"**
5. Enter your OpenAPI URL:
   ```
   https://your-url.up.railway.app/openapi.json
   ```
6. Click **Import**

The weather tools will now be available as Actions in your agent!

## Available Endpoints

Your server provides these endpoints:

- `GET /` - Health check
- `GET /healthz` - Health check
- `GET /get_current_weather?location=London` - Current weather
- `GET /get_weather_forecast?location=London&days=5` - Forecast
- `GET /get_weather_history?location=London&date=2024-01-01` - History
- `GET /search_locations?query=Paris` - Search locations
- `GET /get_astronomy_data?location=London` - Astronomy data
- `GET /openapi.json` - OpenAPI schema (for Agent Builder)

## Example Usage in Agent Builder

Once imported, your agent can use:

- "What's the weather in London?"
- "Get a 5-day forecast for New York"
- "When is sunrise in Tokyo?"
- "Search for weather in Paris"

The agent will automatically call the appropriate weather endpoints!


