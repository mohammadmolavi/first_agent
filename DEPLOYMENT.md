# Deployment Guide

This guide shows you how to deploy the Weather MCP Server to various cloud platforms.

## Prerequisites

- A GitHub account with this repository
- A WeatherAPI.com API key
- (Optional) An account on your chosen deployment platform

## Quick Deploy Options

### Option 1: Render (Recommended - Free Tier)

1. Go to [Render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `weather-mcp-server`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn http_bridge:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variable:
   - **Key**: `WEATHER_API_KEY`
   - **Value**: Your WeatherAPI.com API key
6. Click "Create Web Service"
7. Your server will be available at: `https://weather-mcp-server.onrender.com`

**Note**: Render's free tier spins down after 15 minutes of inactivity. The first request after spin-down may take ~30 seconds.

### Option 2: Fly.io (Free Tier)

1. Install Fly CLI:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. Login to Fly.io:
   ```bash
   fly auth login
   ```

3. Launch your app:
   ```bash
   fly launch
   ```
   - Follow the prompts
   - When asked about the app name, choose one or use the default
   - Don't deploy yet (we need to set the API key first)

4. Set your API key:
   ```bash
   fly secrets set WEATHER_API_KEY=your_api_key_here
   ```

5. Deploy:
   ```bash
   fly deploy
   ```

6. Your server will be available at: `https://your-app-name.fly.dev`

### Option 3: Railway (Free Tier Available)

1. Go to [Railway.app](https://railway.app) and sign up/login
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect the Python app
5. Add Environment Variable:
   - Click on your service → Variables
   - Add `WEATHER_API_KEY` with your API key value
6. Railway will automatically deploy
7. Your server will be available at: `https://your-app-name.up.railway.app`

### Option 4: Google Cloud Run

1. Install Google Cloud SDK
2. Build and push container:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/weather-mcp-server
   ```
3. Deploy:
   ```bash
   gcloud run deploy weather-mcp-server \
     --image gcr.io/YOUR_PROJECT_ID/weather-mcp-server \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars WEATHER_API_KEY=your_api_key_here
   ```

### Option 5: Docker (Any Platform)

Build and run locally or push to any Docker-compatible platform:

```bash
# Build
docker build -t weather-mcp-server .

# Run locally
docker run -p 8000:8000 -e WEATHER_API_KEY=your_key weather-mcp-server

# Push to Docker Hub (then deploy anywhere)
docker tag weather-mcp-server yourusername/weather-mcp-server
docker push yourusername/weather-mcp-server
```

## Setting Up OpenAI Agent Builder

Once your server is deployed and accessible:

1. Get your public URL (e.g., `https://weather-mcp-server.onrender.com`)
2. Test the OpenAPI schema:
   ```bash
   curl https://your-server-url/openapi.json
   ```
3. In OpenAI Agent Builder:
   - Go to **Actions** section
   - Click **"Import from OpenAPI URL"**
   - Enter: `https://your-server-url/openapi.json`
   - The weather tools will be available as Actions

## Health Check

After deployment, verify your server is running:

```bash
curl https://your-server-url/healthz
```

Should return: `{"status":"ok"}`

## Environment Variables

All platforms require the `WEATHER_API_KEY` environment variable. Set it in your platform's dashboard or via CLI.

## Troubleshooting

### Server not responding
- Check that the port is correctly configured (most platforms use `$PORT`)
- Verify environment variables are set
- Check platform logs for errors

### API key errors
- Ensure `WEATHER_API_KEY` is set in your platform's environment variables
- Check that the variable name matches exactly (case-sensitive)

### CORS issues
If you need to add CORS support, update `http_bridge.py`:

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

## Cost Considerations

- **Render**: Free tier available (spins down after inactivity)
- **Fly.io**: Free tier with 3 shared VMs
- **Railway**: $5/month credit, pay-as-you-go after
- **Google Cloud Run**: Free tier: 2 million requests/month
- **AWS Lambda**: Free tier: 1 million requests/month

Choose based on your usage needs!

