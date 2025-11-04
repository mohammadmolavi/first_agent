# Railway Healthcheck Fix Guide

## Changes Made

1. **Added root endpoint `/`** - Railway often checks the root endpoint
2. **Updated healthcheck path** - Changed from `/healthz` to `/` in railway.json
3. **Improved error handling** - Root endpoints don't require API key

## Steps to Fix in Railway

### Option 1: Redeploy (Recommended)

1. **Push your changes to GitHub**:
   ```bash
   git add .
   git commit -m "Fix Railway healthcheck"
   git push origin main
   ```

2. Railway will automatically redeploy

3. **Check Railway logs** to see if it starts successfully

### Option 2: Manual Fix in Railway Dashboard

1. Go to your Railway project
2. Click on your service
3. Go to **Settings** → **Deploy**
4. Update **Start Command** to:
   ```
   uvicorn http_bridge:app --host 0.0.0.0 --port ${PORT:-8000}
   ```
5. Set **Healthcheck Path** to: `/`
6. Click **Redeploy**

### Option 3: Check Environment Variables

Make sure `WEATHER_API_KEY` is set:
1. Go to your service → **Variables**
2. Add: `WEATHER_API_KEY` = `56e3a9b721d94a8fac8101345252510`

### Option 4: Check Logs

1. Go to your service → **Deployments** → Click on latest deployment
2. Check **Logs** tab for errors
3. Common issues:
   - Missing `WEATHER_API_KEY` → Add it in Variables
   - Port binding error → Should be fixed now
   - Import errors → Check requirements.txt

## Test Locally First

Before deploying, test locally:

```bash
# Set port like Railway does
export PORT=8000
export WEATHER_API_KEY="56e3a9b721d94a8fac8101345252510"

# Start server
uvicorn http_bridge:app --host 0.0.0.0 --port $PORT

# Test healthcheck
curl http://localhost:8000/
curl http://localhost:8000/healthz
```

## If Still Failing

1. **Check Railway logs** for specific error messages
2. **Verify requirements.txt** has all dependencies
3. **Try Procfile instead** - Railway might prefer it:
   ```
   web: uvicorn http_bridge:app --host 0.0.0.0 --port ${PORT:-8000}
   ```

