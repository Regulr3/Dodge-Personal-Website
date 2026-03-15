#!/bin/bash
# ==========================================
# TTS Proxy Worker — Deployment Script
# ==========================================
# This deploys your ElevenLabs TTS proxy to Cloudflare Workers.
#
# Prerequisites:
#   - Node.js 18+ installed
#   - A Cloudflare account (free tier works)
#
# Usage:
#   cd tts-worker
#   chmod +x deploy.sh
#   ./deploy.sh
# ==========================================

set -e

echo "🚀 Deploying TTS Proxy Worker to Cloudflare..."
echo ""

# Check if wrangler is installed
if ! npx wrangler --version > /dev/null 2>&1; then
  echo "Installing wrangler..."
  npm install wrangler --save-dev
fi

# Login to Cloudflare (opens browser)
echo "Step 1: Authenticating with Cloudflare..."
npx wrangler login

# Deploy the worker
echo ""
echo "Step 2: Deploying worker..."
npx wrangler deploy

# Set the API key as a secret (not stored in code)
echo ""
echo "Step 3: Setting ElevenLabs API key as a secret..."
echo "When prompted, paste your ElevenLabs API key:"
npx wrangler secret put ELEVENLABS_API_KEY

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Your worker URL is: https://tts-proxy.<your-subdomain>.workers.dev"
echo ""
echo "Next steps:"
echo "  1. Copy your worker URL from the deploy output above"
echo "  2. Open index.html and about.html"
echo "  3. Find the TTS_CONFIG section near the bottom"
echo "  4. Set workerUrl to your worker URL"
echo "  5. Remove the apiKey line (it's no longer needed)"
echo ""
