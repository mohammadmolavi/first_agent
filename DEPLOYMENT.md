# Deployment Guide

This guide shows you how to deploy the Weather MCP Server to various cloud platforms.

## Prerequisites

- A GitHub account with this repository
- A WeatherAPI.com API key
- (Optional) An account on your chosen deployment platform

## Quick Deploy Options

### Option 1: Self-Hosted with ngrok/Cloudflare Tunnel (Works Everywhere - Recommended)

If you can't access cloud platforms, host locally and expose publicly:

**Step 1: Run Server Locally**

```bash
# Set your API key
export WEATHER_API_KEY="your_api_key_here"

# Start the server
uvicorn http_bridge:app --host 0.0.0.0 --port 8000
```

**Step 2: Expose with ngrok**

1. Install ngrok: https://ngrok.com/download
2. Run: `ngrok http 8000`
3. Copy the HTTPS URL (e.g., `https://abcd-1234.ngrok-free.app`)
4. Use this URL in OpenAI Agent Builder

**Step 3: Use Cloudflare Tunnel (Alternative to ngrok)**

```bash
# Install cloudflared
# Linux:
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared

# Run tunnel
cloudflared tunnel --url http://localhost:8000
```

**Keep it running**: Use `screen` or `tmux` to keep the server running:
```bash
# Install screen
sudo apt install screen  # or: sudo yum install screen

# Start server in screen
screen -S weather-server
export WEATHER_API_KEY="your_key"
uvicorn http_bridge:app --host 0.0.0.0 --port 8000

# Press Ctrl+A then D to detach
# Reattach later: screen -r weather-server
```

### Option 2: PythonAnywhere (Free Tier - May Work)

1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com) and sign up
2. Upload your code via:
   - **Files tab** → Upload files
   - Or use Git: `git clone https://github.com/yourusername/repo.git`
3. Set up a Web App:
   - Go to **Web** tab
   - Click **Add a new web app**
   - Choose **Manual configuration** → **Python 3.11**
4. Edit WSGI file:
   ```python
   import sys
   path = '/home/yourusername/weather_mcp_server'
   if path not in sys.path:
       sys.path.append(path)
   
   from http_bridge import app
   application = app
   ```
5. Add environment variable:
   - Go to **Files** → `env` file (or create it)
   - Add: `WEATHER_API_KEY=your_key`
   - In your code, load it or set in Web app settings
6. Reload web app

### Option 3: Railway (May Work - Free Trial)

1. Go to [Railway.app](https://railway.app) and sign up/login
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect the Python app
5. Add Environment Variable:
   - Click on your service → Variables
   - Add `WEATHER_API_KEY` with your API key value
6. Railway will automatically deploy
7. Your server will be available at: `https://your-app-name.up.railway.app`

### Option 4: Fly.io (Free Tier - May Work)

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

### Option 5: VPS (Hetzner, DigitalOcean, etc.)

If you have access to a VPS:

1. **SSH into your VPS**
2. **Clone repository**:
   ```bash
   git clone https://github.com/yourusername/repo.git
   cd weather_mcp_server
   ```
3. **Set up Python environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. **Create systemd service** (for auto-start):
   ```bash
   sudo nano /etc/systemd/system/weather-server.service
   ```
   Add:
   ```ini
   [Unit]
   Description=Weather MCP Server
   After=network.target

   [Service]
   Type=simple
   User=yourusername
   WorkingDirectory=/home/yourusername/weather_mcp_server
   Environment="WEATHER_API_KEY=your_key_here"
   ExecStart=/home/yourusername/weather_mcp_server/venv/bin/uvicorn http_bridge:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
5. **Start service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable weather-server
   sudo systemctl start weather-server
   ```
6. **Set up reverse proxy** (Nginx):
   ```bash
   sudo apt install nginx
   sudo nano /etc/nginx/sites-available/weather-server
   ```
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```
   Enable:
   ```bash
   sudo ln -s /etc/nginx/sites-available/weather-server /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### Option 6: Docker + Docker Hub + Any Platform

Build and push to Docker Hub, then deploy anywhere:

```bash
# Build
docker build -t yourusername/weather-mcp-server .

# Push to Docker Hub
docker push yourusername/weather-mcp-server

# Run anywhere
docker run -p 8000:8000 -e WEATHER_API_KEY=your_key yourusername/weather-mcp-server
```

### Option 7: Render (May Not Work in Some Regions)

**Note**: Render may not be accessible from all regions. Try the options above first.

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

### Option 8: Google Cloud Run

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

### Option 9: Docker (Standalone)

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

1. Get your public URL (e.g., from ngrok, Railway, or your VPS)
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

- **Self-hosted with ngrok**: Free tier available (limited hours/month)
- **Self-hosted with Cloudflare Tunnel**: Free
- **PythonAnywhere**: Free tier available (limited hours/day)
- **Railway**: $5/month credit, pay-as-you-go after
- **Fly.io**: Free tier with 3 shared VMs
- **VPS**: $5-10/month (Hetzner, DigitalOcean, etc.)
- **Render**: Free tier (may not be accessible in all regions)
- **Google Cloud Run**: Free tier: 2 million requests/month
- **AWS Lambda**: Free tier: 1 million requests/month

**Recommendation for restricted regions**: Use self-hosted with ngrok/Cloudflare Tunnel, or a VPS if you have access.

## Tips for Running 24/7

If you need the server running constantly:

1. **Use a VPS** (most reliable)
2. **Use systemd** (see Option 5 above) to auto-restart on failure
3. **Use a process manager** like PM2 or supervisor
4. **Monitor with uptime monitoring** services

## Keeping Server Running (Local)

If running locally and want it always available:

```bash
# Option 1: Use systemd (Linux)
# See Option 5 above

# Option 2: Use screen/tmux
screen -S weather
# or
tmux new -s weather

# Option 3: Use nohup
nohup uvicorn http_bridge:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

