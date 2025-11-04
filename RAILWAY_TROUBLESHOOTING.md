# Railway Healthcheck Troubleshooting

## Current Issue: Service Unavailable

The healthcheck is failing because the server isn't responding. This means either:
1. The server isn't starting
2. The server is crashing on startup
3. The server is binding to wrong port/host

## Steps to Debug

### Step 1: Check Railway Logs

1. Go to Railway dashboard → Your service
2. Click **Deployments** → Latest deployment
3. Click **Logs** tab
4. Look for error messages

### Step 2: Common Issues

#### Issue A: Import Errors
**Symptoms**: Logs show `ModuleNotFoundError` or `ImportError`

**Solution**: Check `requirements.txt` has all dependencies:
```txt
mcp>=1.0.0
httpx>=0.25.0
typing-extensions>=4.0.0
fastapi>=0.110.0
uvicorn[standard]>=0.23.0
```

#### Issue B: API Key Missing
**Symptoms**: Logs show "WEATHER_API_KEY environment variable is required"

**Solution**: 
1. Go to Railway → Your service → **Variables**
2. Add: `WEATHER_API_KEY` = `56e3a9b721d94a8fac8101345252510`
3. Redeploy

#### Issue C: Port Binding
**Symptoms**: Logs show port already in use or binding errors

**Solution**: The `main.py` now handles this correctly with `PORT` env var

#### Issue D: Python Version
**Symptoms**: Build fails or runtime errors

**Solution**: Railway should auto-detect Python 3.11. If not, add `runtime.txt`:
```
python-3.11
```

### Step 3: Test Locally First

Before deploying, test the exact Railway setup locally:

```bash
# Set environment like Railway
export PORT=8000
export WEATHER_API_KEY="56e3a9b721d94a8fac8101345252510"

# Start with main.py (like Railway will)
python main.py

# In another terminal, test healthcheck
curl http://localhost:8000/
curl http://localhost:8000/healthz
```

If this works locally but fails on Railway, check Railway logs for differences.

### Step 4: Alternative Start Command

If `main.py` doesn't work, try direct uvicorn in Railway:

1. Go to Railway → Settings → Deploy
2. Change **Start Command** to:
   ```
   uvicorn http_bridge:app --host 0.0.0.0 --port $PORT --log-level info
   ```
3. Redeploy

### Step 5: Check Build Process

1. Go to Railway → Deployments → Latest
2. Check **Build Logs** for errors during build
3. Common build issues:
   - Missing dependencies in requirements.txt
   - Python version mismatch
   - File not found errors

### Step 6: Verify Files Are Deployed

Make sure all files are in GitHub and Railway can see them:
- `main.py`
- `http_bridge.py`
- `weather_mcp_server.py`
- `requirements.txt`
- `railway.json` or `Procfile`

## Quick Fix Checklist

- [ ] `WEATHER_API_KEY` is set in Railway Variables
- [ ] All files are pushed to GitHub
- [ ] `requirements.txt` has all dependencies
- [ ] `main.py` exists and is executable
- [ ] Railway logs don't show import errors
- [ ] Railway logs don't show port binding errors
- [ ] Healthcheck path is set to `/` in railway.json

## Still Not Working?

Share the Railway logs output and I can help debug further!

