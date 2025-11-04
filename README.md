# Weather MCP Server

A Model Context Protocol (MCP) server that provides weather data retrieval capabilities for AI agents. Includes both MCP (stdio) and HTTP bridge modes for compatibility with different platforms.

## Features

This server provides the following weather-related tools:

- **get_current_weather**: Get current weather conditions for any location
- **get_weather_forecast**: Get weather forecast for 1-10 days
- **get_weather_history**: Get historical weather data for specific dates
- **search_locations**: Search for locations by name
- **get_astronomy_data**: Get sunrise, sunset, moon phase, and other astronomy data

## Installation

### Prerequisites

- Python 3.8 or higher
- A WeatherAPI.com API key ([Get one here](https://www.weatherapi.com/signup.aspx))

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Environment Variable

Set your WeatherAPI.com API key as an environment variable:

**Option A: For current session only**
```bash
export WEATHER_API_KEY="your_api_key_here"
```

**Option B: For all future sessions (Linux/macOS)**
```bash
echo 'export WEATHER_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Option C: For Windows**
```powershell
setx WEATHER_API_KEY "your_api_key_here"
```

**Verify it's set:**
```bash
echo $WEATHER_API_KEY
```

## Usage

### Mode 1: MCP Server (stdio) - For MCP-Compatible Clients

For clients that support MCP protocol directly (like Cursor, Claude Desktop):

```bash
python weather_mcp_server.py
```

The server will start and listen for MCP client connections via stdio.

**MCP Configuration Example** (for Cursor/Claude Desktop):

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["weather_mcp_server.py"],
      "env": {
        "WEATHER_API_KEY": "your_api_key_here"
      },
      "cwd": "/path/to/weather_mcp_server"
    }
  }
}
```

### Mode 2: HTTP Bridge - For OpenAI Agent Builder

For OpenAI Agent Builder and other platforms that require HTTP/OpenAPI endpoints:

#### Step 1: Start the HTTP Server

```bash
uvicorn http_bridge:app --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`.

#### Step 2: Test the Endpoints

```bash
# Health check
curl http://localhost:8000/healthz

# Get current weather
curl "http://localhost:8000/get_current_weather?location=London&include_air_quality=true"

# Get forecast
curl "http://localhost:8000/get_weather_forecast?location=New+York&days=5"

# Search locations
curl "http://localhost:8000/search_locations?query=Paris"
```

#### Step 3: Expose Publicly (Required for OpenAI Agent Builder)

OpenAI Agent Builder needs a publicly accessible URL. Use one of these options:

**Option A: Using ngrok (Quick Testing)**
```bash
# Install ngrok: https://ngrok.com/download
ngrok http 8000
# Copy the HTTPS URL (e.g., https://abcd-1234.ngrok-free.app)
```

**Option B: Deploy to Cloud (Production)**

Deploy the FastAPI app to:
- **Render**: `render.yaml` with FastAPI service
- **Fly.io**: `fly.toml` configuration
- **Google Cloud Run**: Container deployment
- **AWS Lambda**: Using Mangum adapter

#### Step 4: Register in OpenAI Agent Builder

1. Go to your OpenAI Agent Builder dashboard
2. Navigate to **Actions** section
3. Click **"Import from OpenAPI URL"**
4. Enter your public OpenAPI URL: `https://your-domain.com/openapi.json`
5. The endpoints will be available as Actions

**Available HTTP Endpoints:**

- `GET /healthz` - Health check endpoint
- `GET /get_current_weather` - Current weather conditions
- `GET /get_weather_forecast` - Weather forecast
- `GET /get_weather_history` - Historical weather data
- `GET /search_locations` - Search for locations
- `GET /get_astronomy_data` - Astronomy data

## API Endpoints Supported

The server supports the following WeatherAPI.com endpoints:

- Current weather data (`current.json`)
- Weather forecasts (`forecast.json`)
- Historical weather data (`history.json`)
- Location search (`search.json`)
- Astronomy data (`astronomy.json`)

## Configuration

The server can be configured by modifying the `WeatherMCPServer` class initialization:

- `api_key`: Your weather API key (required, from `WEATHER_API_KEY` env var)
- `base_url`: Base URL for the weather API (defaults to `"http://api.weatherapi.com/v1"`)

## Example Usage

### MCP Client Example

```json
{
  "name": "get_current_weather",
  "arguments": {
    "location": "London",
    "include_air_quality": true
  }
}
```

### HTTP API Example

```bash
curl "http://localhost:8000/get_current_weather?location=London&include_air_quality=true"
```

Response:
```json
{
  "location": {
    "name": "London",
    "region": "City of London, Greater London",
    "country": "United Kingdom",
    "coordinates": {
      "latitude": 51.52,
      "longitude": -0.11
    },
    "timezone": "Europe/London",
    "local_time": "2024-01-15 14:30"
  },
  "current_weather": {
    "temperature": {
      "celsius": 8.0,
      "fahrenheit": 46.4,
      "feels_like_c": 6.2,
      "feels_like_f": 43.2
    },
    "condition": {
      "text": "Partly cloudy",
      "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
      "code": 1003
    },
    "wind": {
      "speed_mph": 10.5,
      "speed_kph": 16.9,
      "direction": "SW",
      "degree": 230
    }
  }
}
```

## Error Handling

The server includes comprehensive error handling for:
- API request failures
- Invalid parameters
- Network connectivity issues
- Malformed responses
- Missing API keys

## Data Formatting

All weather data is formatted into a consistent, structured JSON format that includes:
- Location information (name, coordinates, timezone)
- Weather conditions (temperature, humidity, wind, etc.)
- Air quality data (when requested)
- Astronomy data (sunrise/sunset times, moon phases)

## Troubleshooting

### Proxy Errors

If you encounter errors like:
```
{"detail":"Unknown scheme for proxy URL URL('socks://127.0.0.1:2080/')"}
```

This happens when your environment has proxy variables set but httpx doesn't support SOCKS proxies by default. The server is configured to ignore proxy environment variables, but if you still see issues:

**Solution 1: Unset proxy variables**
```bash
unset ALL_PROXY HTTPS_PROXY HTTP_PROXY
```

**Solution 2: Install SOCKS support** (if you need proxy support)
```bash
pip install "httpx[socks]"
```

### API Key Not Found

If you get: `WEATHER_API_KEY environment variable is required`

Make sure the environment variable is set:
```bash
export WEATHER_API_KEY="your_key"
echo $WEATHER_API_KEY  # Verify it's set
```

### Port Already in Use

If port 8000 is already in use when starting the HTTP bridge:
```bash
uvicorn http_bridge:app --host 0.0.0.0 --port 8001
```

### CORS Issues (for web deployments)

If deploying the HTTP bridge and encountering CORS errors, add CORS middleware to `http_bridge.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Project Structure

```
weather_mcp_server/
├── weather_mcp_server.py  # MCP server (stdio mode)
├── http_bridge.py         # HTTP bridge (for OpenAI Agent Builder)
├── requirements.txt       # Python dependencies
├── mcp_config.json        # Example MCP configuration
├── test_weather_server.py # Test script
└── README.md              # This file
```

## License

This project is provided as-is for use with WeatherAPI.com services.
