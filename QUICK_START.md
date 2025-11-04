# Quick Start: Deploy for OpenAI Agent Builder

This guide shows you the fastest way to get a globally accessible URL for OpenAI Agent Builder.

## 🚀 Option 1: Self-Hosted + ngrok (WORKS FROM ANYWHERE - 5 minutes)

This creates a **global HTTPS URL** that OpenAI Agent Builder can use.

### Step 1: Install ngrok

```bash
# Download ngrok (Linux)
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar xvzf ngrok-v3-stable-linux-amd64.tgz
sudo mv ngrok /usr/local/bin/

# Or use snap
sudo snap install ngrok

# Or download from: https://ngrok.com/download
```

### Step 2: Start Your Server

```bash
# Set your API key
export WEATHER_API_KEY="your_api_key_here"

# Start the server
./start_server.sh
# Or manually: uvicorn http_bridge:app --host 0.0.0.0 --port 8000
```

### Step 3: Expose with ngrok

**In a new terminal**, run:
```bash
ngrok http 8000
```

You'll see output like:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok-free.app`)

### Step 4: Use in OpenAI Agent Builder

1. Go to OpenAI Agent Builder → Actions
2. Click "Import from OpenAPI URL"
3. Enter: `https://abc123.ngrok-free.app/openapi.json`
4. Done! Your weather tools are now available

### Keep It Running

**Option A: Use screen (recommended)**
```bash
# Terminal 1: Start server
screen -S weather-server
export WEATHER_API_KEY="your_key"
uvicorn http_bridge:app --host 0.0.0.0 --port 8000
# Press Ctrl+A then D to detach

# Terminal 2: Start ngrok
screen -S ngrok
ngrok http 8000
# Press Ctrl+A then D to detach

# To reattach later:
screen -r weather-server
screen -r ngrok
```

**Option B: Use tmux**
```bash
# Start tmux session
tmux new -s weather

# Split window: Ctrl+B then "
# In top pane: uvicorn http_bridge:app --host 0.0.0.0 --port 8000
# In bottom pane: ngrok http 8000

# Detach: Ctrl+B then D
# Reattach: tmux attach -t weather
```

**Note**: ngrok free tier gives you a random URL each time. For a permanent URL, sign up for ngrok account (free) and use authtoken.

---

## 🌐 Option 2: Cloudflare Tunnel (FREE, PERMANENT URL)

Cloudflare Tunnel is free and gives you a permanent subdomain.

### Step 1: Install cloudflared

```bash
# Linux
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
```

### Step 2: Start Your Server

```bash
export WEATHER_API_KEY="your_key"
uvicorn http_bridge:app --host 0.0.0.0 --port 8000
```

### Step 3: Create Tunnel

```bash
# Login to Cloudflare (free account)
cloudflared tunnel login

# Create a tunnel
cloudflared tunnel create weather-server

# Run the tunnel (in another terminal or screen)
cloudflared tunnel --url http://localhost:8000
```

This gives you a permanent URL like: `https://weather-server-xxxxx.trycloudflare.com`

---

## ☁️ Option 3: PythonAnywhere (Free Tier)

If you can access PythonAnywhere:

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your code via Git or Files tab
3. Create a Web App (Manual configuration)
4. Set environment variable for API key
5. Your server will be at: `https://yourusername.pythonanywhere.com`

See DEPLOYMENT.md for detailed instructions.

---

## 🚂 Option 4: Railway (May Work)

1. Go to [railway.app](https://railway.app)
2. Deploy from GitHub
3. Add `WEATHER_API_KEY` environment variable
4. Get your URL: `https://your-app.up.railway.app`

---

## 🐳 Option 5: Fly.io (May Work)

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login and deploy
fly auth login
fly launch
fly secrets set WEATHER_API_KEY=your_key
fly deploy
```

Your server: `https://your-app.fly.dev`

---

## ✅ Verify Your Deployment

Test your global URL:

```bash
# Health check
curl https://your-url/healthz

# Should return: {"status":"ok"}

# OpenAPI schema (for Agent Builder)
curl https://your-url/openapi.json
```

---

## 🎯 Recommended: ngrok or Cloudflare Tunnel

Both create **globally accessible HTTPS URLs** that work perfectly with OpenAI Agent Builder, even from restricted regions.

**ngrok pros**: 
- Very easy setup
- Works immediately
- Free tier available

**Cloudflare Tunnel pros**:
- Free forever
- Permanent URL (if you want)
- No account needed for basic use

**For 24/7 operation**: Use a VPS (see DEPLOYMENT.md Option 5) or keep ngrok/Cloudflare running on your local machine.

