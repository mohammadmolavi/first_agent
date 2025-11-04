#!/usr/bin/env python3
"""
Test script for Weather MCP Server
"""

import asyncio
import json
import os
from weather_mcp_server import WeatherMCPServer

async def test_server():
    """Test the weather MCP server functionality"""
    
    # Get API key from environment
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        print("Please set WEATHER_API_KEY environment variable")
        return
    
    # Create server instance
    server = WeatherMCPServer(api_key)
    
    print("Testing Weather MCP Server...")
    print("=" * 50)
    
    # Test current weather
    print("\n1. Testing get_current_weather...")
    try:
        result = await server._get_current_weather({"location": "London"})
        print("✓ Current weather test passed")
        print(f"Response length: {len(result.content[0].text)} characters")
    except Exception as e:
        print(f"✗ Current weather test failed: {e}")
    
    # Test weather forecast
    print("\n2. Testing get_weather_forecast...")
    try:
        result = await server._get_weather_forecast({"location": "London", "days": 3})
        print("✓ Weather forecast test passed")
        print(f"Response length: {len(result.content[0].text)} characters")
    except Exception as e:
        print(f"✗ Weather forecast test failed: {e}")
    
    # Test location search
    print("\n3. Testing search_locations...")
    try:
        result = await server._search_locations({"query": "London"})
        print("✓ Location search test passed")
        print(f"Response length: {len(result.content[0].text)} characters")
    except Exception as e:
        print(f"✗ Location search test failed: {e}")
    
    # Test astronomy data
    print("\n4. Testing get_astronomy_data...")
    try:
        result = await server._get_astronomy_data({"location": "London"})
        print("✓ Astronomy data test passed")
        print(f"Response length: {len(result.content[0].text)} characters")
    except Exception as e:
        print(f"✗ Astronomy data test failed: {e}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    asyncio.run(test_server())
