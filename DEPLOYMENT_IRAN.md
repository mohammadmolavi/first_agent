# Deployment Guide for Restricted Regions (Iran)

Since ngrok and Cloudflare Tunnel are blocked, here are working alternatives:

## ✅ Option 1: Railway.app (Recommended - Usually Works)

Railway is more accessible and often works from restricted regions:

1. **Go to [railway.app](https://railway.app)** and sign up (free trial with $5 credit)
2. **Click "New Project"** → **"Deploy from GitHub repo"**
3. **Select your repository**: `mohammadmolavi/first_agent`
4. Railway will auto-detect the Python app
5. **Add Environment Variable**:
   - Click on your service → **Variables** tab
   - Add: `WEATHER_API_KEY` = `56e3a9b721d94a8fac8101345252510`
6. Railway will automatically deploy
7. **Your server will be at**: `https://your-app-name.up.railway.app`

**Time**: 5-10 minutes
**Cost**: Free trial ($5 credit), then pay-as-you-go

---

## ✅ Option 2: PythonAnywhere (Free Tier)

If you can access PythonAnywhere:

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com)
2. **Upload your code**:
   - Go to **Files** tab
   - Click **Upload a file** or use **Bash console**:
     ```bash
     git clone https://github.com/mohammadmolavi/first_agent.git
     cd first_agent
     ```
3. **Create a Web App**:
   - Go to **Web** tab
   - Click **Add a new web app**
   - Choose **Manual configuration** → **Python 3.11**
4. **Edit WSGI file** (click on the file link):
   ```python
   import sys
   path = '/home/yourusername/first_agent'
   if path not in sys.path:
       sys.path.append(path)
   
   from http_bridge import app
   application = app
   ```
5. **Set environment variable**:
   - Go to **Files** tab
   - Create/edit `.env` file in your project directory:
     ```
     WEATHER_API_KEY=56e3a9b721d94a8fac8101345252510
     ```
   - Or set in Web app → **Environment variables**
6. **Reload** your web app
7. **Your server**: `https://yourusername.pythonanywhere.com`

**Time**: 15-20 minutes
**Cost**: Free tier (limited hours/day)

---

## ✅ Option 3: Fly.io (May Work)

Try Fly.io - sometimes works from restricted regions:

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login (may need to use browser)
fly auth login

# Launch app
cd ~/weather_mcp_server
fly launch

# Set API key
fly secrets set WEATHER_API_KEY=56e3a9b721d94a8fac8101345252510

# Deploy
fly deploy
```

**Your server**: `https://your-app-name.fly.dev`

---

## ✅ Option 4: Use a VPS (Most Reliable)

If you have access to a VPS outside Iran:

1. **SSH into your VPS**
2. **Clone and setup**:
   ```bash
   git clone https://github.com/mohammadmolavi/first_agent.git
   cd first_agent
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Create systemd service**:
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
   WorkingDirectory=/home/yourusername/first_agent
   Environment="WEATHER_API_KEY=56e3a9b721d94a8fac8101345252510"
   ExecStart=/home/yourusername/first_agent/venv/bin/uvicorn http_bridge:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
4. **Start service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable weather-server
   sudo systemctl start weather-server
   ```
5. **Use your VPS IP** or domain: `http://your-vps-ip:8000`

**Cost**: $5-10/month (Hetzner, DigitalOcean, etc.)

---

## ✅ Option 5: LocalTunnel (Alternative to ngrok)

LocalTunnel might work where ngrok doesn't:

```bash
# Install
npm install -g localtunnel

# Start your server
export WEATHER_API_KEY="56e3a9b721d94a8fac8101345252510"
uvicorn http_bridge:app --host 0.0.0.0 --port 8000

# In another terminal
lt --port 8000
```

---

## ✅ Option 6: Serveo (SSH Tunneling)

If you have SSH access:

```bash
# Start your server
export WEATHER_API_KEY="56e3a9b721d94a8fac8101345252510"
uvicorn http_bridge:app --host 0.0.0.0 --port 8000

# In another terminal
ssh -R 80:localhost:8000 serveo.net
```

---

## 🎯 Recommended: Railway.app

Railway is the easiest and most likely to work:
- Free trial with $5 credit
- Auto-deploys from GitHub
- Usually accessible from restricted regions
- Takes 5-10 minutes to setup

---

## Quick Test After Deployment

Once you have a URL, test it:

```bash
# Health check
curl https://your-url/healthz

# OpenAPI schema (for Agent Builder)
curl https://your-url/openapi.json
```

Then use in OpenAI Agent Builder:
1. Go to Actions → "Import from OpenAPI URL"
2. Enter: `https://your-url/openapi.json`

