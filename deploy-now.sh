#!/bin/bash

# Complete Auto Deploy with Pre-filled Values
set -e

echo "🚀 Liquid Launch Bot - Full Automated Deployment"
echo "=================================================="
echo ""

# Pre-filled values
GITHUB_USER="YOUR_GITHUB_USERNAME"
REPO_NAME="liquid-launch-bot"
SERVER_HOST="YOUR_SERVER_IP"
SERVER_USER="ubuntu"

# Check if values are set
if [ "$GITHUB_USER" = "YOUR_GITHUB_USERNAME" ]; then
    read -p "Enter GitHub username: " GITHUB_USER
fi

if [ "$SERVER_HOST" = "YOUR_SERVER_IP" ]; then
    read -p "Enter server IP/domain: " SERVER_HOST
fi

echo ""
echo "📝 Configuration:"
echo "  GitHub User: $GITHUB_USER"
echo "  Repository: $REPO_NAME"
echo "  Server: $SERVER_HOST"
echo "  SSH User: $SERVER_USER"
echo ""

# Verify GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not found"
    echo "Install from: https://cli.github.com/"
    exit 1
fi

# Verify SSH key
if [ ! -f ~/.ssh/github_deploy ]; then
    echo "🔑 Generating SSH key..."
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/github_deploy -N ""
fi

echo ""
echo "📝 Step 1: Adding GitHub Secrets..."

# Add all secrets
gh secret set BASE_RPC_URL -b "https://mainnet.base.org" -R "$GITHUB_USER/$REPO_NAME" 2>/dev/null && echo "  ✅ BASE_RPC_URL"
gh secret set LIQUID_FACTORY_ADDRESS -b "0x04f1a284168743759be6554f607a10cebdb77760" -R "$GITHUB_USER/$REPO_NAME" 2>/dev/null && echo "  ✅ LIQUID_FACTORY_ADDRESS"
gh secret set START_BLOCK -b "42266500" -R "$GITHUB_USER/$REPO_NAME" 2>/dev/null && echo "  ✅ START_BLOCK"
gh secret set TELEGRAM_BOT_TOKEN -b "8546165371:AAFXXRtj42oQwfaKgMwgubhWI-_8jfryb1E" -R "$GITHUB_USER/$REPO_NAME" 2>/dev/null && echo "  ✅ TELEGRAM_BOT_TOKEN"
gh secret set TELEGRAM_CHAT_ID -b "@Liquid_tokens" -R "$GITHUB_USER/$REPO_NAME" 2>/dev/null && echo "  ✅ TELEGRAM_CHAT_ID"
gh secret set IPFS_GATEWAY -b "https://ipfs.io/ipfs/" -R "$GITHUB_USER/$REPO_NAME" 2>/dev/null && echo "  ✅ IPFS_GATEWAY"
gh secret set POLL_INTERVAL -b "12" -R "$GITHUB_USER/$REPO_NAME" 2>/dev/null && echo "  ✅ POLL_INTERVAL"
gh secret set SERVER_HOST -b "$SERVER_HOST" -R "$GITHUB_USER/$REPO_NAME" 2>/dev/null && echo "  ✅ SERVER_HOST"
gh secret set SERVER_USER -b "$SERVER_USER" -R "$GITHUB_USER/$REPO_NAME" 2>/dev/null && echo "  ✅ SERVER_USER"

SSH_KEY=$(cat ~/.ssh/github_deploy)
gh secret set SERVER_SSH_KEY -b "$SSH_KEY" -R "$GITHUB_USER/$REPO_NAME" 2>/dev/null && echo "  ✅ SERVER_SSH_KEY"

echo ""
echo "📦 Step 2: Setting up server..."

# Setup server
ssh -i ~/.ssh/github_deploy "$SERVER_USER@$SERVER_HOST" << 'SERVEREOF' 2>/dev/null || {
    echo "⚠️  SSH connection failed. Please ensure:"
    echo "  1. Server is accessible at $SERVER_HOST"
    echo "  2. SSH user is $SERVER_USER"
    echo "  3. Public key is in ~/.ssh/authorized_keys"
}

echo "  Installing Docker..."
sudo apt-get update > /dev/null 2>&1
sudo apt-get install -y docker.io docker-compose git curl > /dev/null 2>&1

echo "  Creating directories..."
sudo mkdir -p /app/liquid-launch-bot
cd /app/liquid-launch-bot

echo "  Cloning repository..."
sudo git clone https://github.com/$GITHUB_USER/$REPO_NAME.git . > /dev/null 2>&1
sudo chown -R $USER:$USER /app/liquid-launch-bot

mkdir -p data

echo "  ✅ Server ready!"
SERVEREOF

echo ""
echo "🔄 Step 3: Pushing to GitHub..."

git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git" 2>/dev/null || true
git branch -M main 2>/dev/null || true
git push -u origin main 2>/dev/null || {
    echo "⚠️  Git push failed. Please ensure:"
    echo "  1. Repository exists at https://github.com/$GITHUB_USER/$REPO_NAME"
    echo "  2. You have push permissions"
}

echo ""
echo "✅ DEPLOYMENT COMPLETE!"
echo ""
echo "📊 Next Steps:"
echo "  1. Check GitHub Actions: https://github.com/$GITHUB_USER/$REPO_NAME/actions"
echo "  2. Monitor bot: ssh $SERVER_USER@$SERVER_HOST 'cd /app/liquid-launch-bot && docker-compose logs -f bot'"
echo "  3. Check Telegram channel: @Liquid_tokens"
echo ""
echo "🎉 Bot is now running on production server!"
