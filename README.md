# Weather MCP Server

A Model Context Protocol (MCP) server that provides weather data retrieval capabilities for AI agents.

## Features

This MCP server provides the following weather-related tools:

- **get_current_weather**: Get current weather conditions for any location
- **get_weather_forecast**: Get weather forecast for 1-10 days
- **get_weather_history**: Get historical weather data for specific dates
- **search_locations**: Search for locations by name
- **get_astronomy_data**: Get sunrise, sunset, moon phase, and other astronomy data

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set your weather API key as an environment variable:
```bash
export WEATHER_API_KEY="your_api_key_here"
```

## Usage

Run the MCP server:
```bash
python weather_mcp_server.py
```

The server will start and listen for MCP client connections via stdio.

## API Endpoints Supported

Based on the weather API structure provided, this server supports:

- Current weather data (`current.json`)
- Weather forecasts (`forecast.json`)
- Historical weather data (`history.json`)
- Location search (`search.json`)
- Astronomy data (`astronomy.json`)

## Configuration

The server can be configured by modifying the `WeatherMCPServer` class initialization:

- `api_key`: Your weather API key (required)
- `base_url`: Base URL for the weather API (defaults to "http://api.weatherapi.com/v1")

## Error Handling

The server includes comprehensive error handling for:
- API request failures
- Invalid parameters
- Network connectivity issues
- Malformed responses

## Data Formatting

All weather data is formatted into a consistent, structured JSON format that includes:
- Location information (name, coordinates, timezone)
- Weather conditions (temperature, humidity, wind, etc.)
- Air quality data (when requested)
- Astronomy data (sunrise/sunset times, moon phases)

## Example Usage

Once connected to an MCP client, you can use the tools like this:

```json
{
  "name": "get_current_weather",
  "arguments": {
    "location": "London",
    "include_air_quality": true
  }
}
```

This will return current weather conditions for London including air quality data.
# first_agent
