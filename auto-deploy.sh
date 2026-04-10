#!/bin/bash

# Auto Deploy Script
# This script automates the entire deployment process

set -e

echo "🚀 Liquid Launch Bot - Automated Deployment"
echo "==========================================="
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not found. Install from: https://cli.github.com/"
    exit 1
fi

# Get repository info
read -p "Enter GitHub username: " GITHUB_USER
read -p "Enter repository name (default: liquid-launch-bot): " REPO_NAME
REPO_NAME=${REPO_NAME:-liquid-launch-bot}

read -p "Enter server IP/domain: " SERVER_HOST
read -p "Enter server SSH username (default: ubuntu): " SERVER_USER
SERVER_USER=${SERVER_USER:-ubuntu}

echo ""
echo "📝 Adding GitHub Secrets..."

# Add environment secrets
gh secret set BASE_RPC_URL -b "https://mainnet.base.org" -R "$GITHUB_USER/$REPO_NAME"
gh secret set LIQUID_FACTORY_ADDRESS -b "0x04f1a284168743759be6554f607a10cebdb77760" -R "$GITHUB_USER/$REPO_NAME"
gh secret set START_BLOCK -b "42266500" -R "$GITHUB_USER/$REPO_NAME"
gh secret set TELEGRAM_BOT_TOKEN -b "8546165371:AAFXXRtj42oQwfaKgMwgubhWI-_8jfryb1E" -R "$GITHUB_USER/$REPO_NAME"
gh secret set TELEGRAM_CHAT_ID -b "@Liquid_tokens" -R "$GITHUB_USER/$REPO_NAME"
gh secret set IPFS_GATEWAY -b "https://ipfs.io/ipfs/" -R "$GITHUB_USER/$REPO_NAME"
gh secret set POLL_INTERVAL -b "12" -R "$GITHUB_USER/$REPO_NAME"

# Add server secrets
gh secret set SERVER_HOST -b "$SERVER_HOST" -R "$GITHUB_USER/$REPO_NAME"
gh secret set SERVER_USER -b "$SERVER_USER" -R "$GITHUB_USER/$REPO_NAME"

# Check if SSH key exists
if [ ! -f ~/.ssh/github_deploy ]; then
    echo "🔑 Generating SSH key..."
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/github_deploy -N ""
fi

# Add SSH key to GitHub
SSH_KEY=$(cat ~/.ssh/github_deploy)
gh secret set SERVER_SSH_KEY -b "$SSH_KEY" -R "$GITHUB_USER/$REPO_NAME"

echo "✅ GitHub Secrets added!"
echo ""
echo "📦 Setting up server..."

# Copy public key to server
echo "Adding public key to server..."
ssh-copy-id -i ~/.ssh/github_deploy.pub "$SERVER_USER@$SERVER_HOST" 2>/dev/null || {
    echo "⚠️  Could not auto-add SSH key. Please add manually:"
    echo "cat ~/.ssh/github_deploy.pub | ssh $SERVER_USER@$SERVER_HOST 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'"
}

# Setup server
ssh -i ~/.ssh/github_deploy "$SERVER_USER@$SERVER_HOST" << 'SERVEREOF'
echo "Installing Docker and dependencies..."
sudo apt-get update
sudo apt-get install -y docker.io docker-compose git curl

echo "Creating project directory..."
sudo mkdir -p /app/liquid-launch-bot
cd /app/liquid-launch-bot

echo "Cloning repository..."
sudo git clone https://github.com/$GITHUB_USER/$REPO_NAME.git .
sudo chown -R $USER:$USER /app/liquid-launch-bot

echo "Creating data directory..."
mkdir -p data

echo "✅ Server setup complete!"
SERVEREOF

echo ""
echo "🔄 Pushing to GitHub..."
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git" 2>/dev/null || true
git branch -M main
git push -u origin main

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "📊 Monitoring:"
echo "  - GitHub Actions: https://github.com/$GITHUB_USER/$REPO_NAME/actions"
echo "  - Server logs: ssh $SERVER_USER@$SERVER_HOST 'cd /app/liquid-launch-bot && docker-compose logs -f bot'"
echo ""
echo "🎉 Bot is now deploying to production!"
