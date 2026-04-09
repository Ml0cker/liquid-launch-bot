#!/bin/bash

# GitHub Secrets Setup Script
# Usage: ./setup-github-secrets.sh <GITHUB_TOKEN> <REPO_OWNER> <REPO_NAME>

if [ $# -lt 3 ]; then
    echo "Usage: $0 <GITHUB_TOKEN> <REPO_OWNER> <REPO_NAME>"
    echo "Example: $0 ghp_xxxx myusername liquid-launch-bot"
    exit 1
fi

GITHUB_TOKEN=$1
REPO_OWNER=$2
REPO_NAME=$3

echo "Setting up GitHub Secrets for $REPO_OWNER/$REPO_NAME..."

# Function to add secret
add_secret() {
    local secret_name=$1
    local secret_value=$2
    
    echo "Adding secret: $secret_name"
    
    # Encode value in base64
    encoded_value=$(echo -n "$secret_value" | base64)
    
    # Get public key for repo
    public_key=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/secrets/public-key" \
        | jq -r '.key')
    
    key_id=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/secrets/public-key" \
        | jq -r '.key_id')
    
    # Encrypt value using public key (requires libsodium)
    # For simplicity, using GitHub CLI if available
    if command -v gh &> /dev/null; then
        gh secret set "$secret_name" -b "$secret_value" -R "$REPO_OWNER/$REPO_NAME"
    else
        echo "GitHub CLI not found. Please install it or use GitHub web interface."
        echo "Secret: $secret_name = $secret_value"
    fi
}

# Add secrets from .env
if [ -f ".env" ]; then
    # Extract and add blockchain secrets
    BASE_RPC_URL=$(grep "^BASE_RPC_URL=" .env | cut -d'=' -f2)
    LIQUID_FACTORY_ADDRESS=$(grep "^LIQUID_FACTORY_ADDRESS=" .env | cut -d'=' -f2)
    START_BLOCK=$(grep "^START_BLOCK=" .env | cut -d'=' -f2)
    TELEGRAM_BOT_TOKEN=$(grep "^TELEGRAM_BOT_TOKEN=" .env | cut -d'=' -f2)
    TELEGRAM_CHAT_ID=$(grep "^TELEGRAM_CHAT_ID=" .env | cut -d'=' -f2)
    IPFS_GATEWAY=$(grep "^IPFS_GATEWAY=" .env | cut -d'=' -f2)
    POLL_INTERVAL=$(grep "^POLL_INTERVAL=" .env | cut -d'=' -f2)
    
    add_secret "BASE_RPC_URL" "$BASE_RPC_URL"
    add_secret "LIQUID_FACTORY_ADDRESS" "$LIQUID_FACTORY_ADDRESS"
    add_secret "START_BLOCK" "$START_BLOCK"
    add_secret "TELEGRAM_BOT_TOKEN" "$TELEGRAM_BOT_TOKEN"
    add_secret "TELEGRAM_CHAT_ID" "$TELEGRAM_CHAT_ID"
    add_secret "IPFS_GATEWAY" "$IPFS_GATEWAY"
    add_secret "POLL_INTERVAL" "$POLL_INTERVAL"
    
    echo "✅ Environment secrets added!"
else
    echo "❌ .env file not found"
    exit 1
fi

echo ""
echo "Now add these secrets manually via GitHub web interface:"
echo "1. Go to: https://github.com/$REPO_OWNER/$REPO_NAME/settings/secrets/actions"
echo "2. Add SERVER_HOST - Your server IP or domain"
echo "3. Add SERVER_USER - SSH username (e.g., ubuntu)"
echo "4. Add SERVER_SSH_KEY - Private SSH key content"
echo ""
echo "Setup complete!"
