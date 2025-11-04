#!/bin/bash
# Quick guide for deploying to Railway

echo "🚂 Railway Deployment Guide"
echo ""
echo "Since ngrok and Cloudflare are blocked, Railway is the best option!"
echo ""
echo "Steps:"
echo "1. Go to https://railway.app"
echo "2. Sign up with GitHub (free)"
echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
echo "4. Select: mohammadmolavi/first_agent"
echo "5. Railway will auto-detect and deploy"
echo "6. Add environment variable:"
echo "   - Click on your service → Variables"
echo "   - Add: WEATHER_API_KEY = 56e3a9b721d94a8fac8101345252510"
echo "7. Get your URL from Railway dashboard"
echo "8. Use in OpenAI Agent Builder: https://your-url.up.railway.app/openapi.json"
echo ""
echo "Time: 5-10 minutes"
echo "Cost: Free trial ($5 credit)"
echo ""
echo "All your code is already on GitHub and ready to deploy!"

