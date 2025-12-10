#!/bin/bash

# Fly.io Deployment Script
# This script sets secrets and deploys the application

set -e  # Exit on error

echo "🚀 Starting Fly.io deployment..."

# Navigate to project directory
cd "$(dirname "$0")"
echo "📁 Current directory: $(pwd)"

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null && ! command -v fly &> /dev/null; then
    echo "❌ Error: flyctl is not installed"
    echo "📥 Please install it from: https://fly.io/docs/getting-started/installing-flyctl/"
    exit 1
fi

# Use flyctl or fly command
FLY_CMD=$(command -v flyctl || command -v fly)
echo "✅ Using: $FLY_CMD"

# Check if logged in
echo "🔐 Checking authentication..."
if ! $FLY_CMD auth whoami &> /dev/null; then
    echo "⚠️  Not logged in. Please run: $FLY_CMD auth login"
    exit 1
fi

echo "✅ Authenticated as: $($FLY_CMD auth whoami)"

# Set CORS origins (update with your actual frontend domain)
echo ""
echo "🔧 Setting CORS_ORIGINS secret..."
$FLY_CMD secrets set CORS_ORIGINS="https://algofolks.com,https://www.algofolks.com" --app lucky-draw || echo "⚠️  CORS_ORIGINS might already be set"

# Deploy the application
echo ""
echo "🚀 Deploying application..."
$FLY_CMD deploy --app lucky-draw

echo ""
echo "✅ Deployment complete!"
echo "📊 View logs with: $FLY_CMD logs --app lucky-draw"

