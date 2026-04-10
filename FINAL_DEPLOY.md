# Final Deployment Instructions

## Step 1: Add GitHub Secrets

Go to: `https://github.com/Ml0cker/liquid-launch-bot/settings/secrets/actions`

Add these secrets:

### Environment Secrets
```
BASE_RPC_URL = https://mainnet.base.org
LIQUID_FACTORY_ADDRESS = 0x04f1a284168743759be6554f607a10cebdb77760
START_BLOCK = 42266500
TELEGRAM_BOT_TOKEN = 8546165371:AAFXXRtj42oQwfaKgMwgubhWI-_8jfryb1E
TELEGRAM_CHAT_ID = @Liquid_tokens
IPFS_GATEWAY = https://ipfs.io/ipfs/
POLL_INTERVAL = 12
```

### Server Secrets (Add your values)
```
SERVER_HOST = your_server_ip_or_domain
SERVER_USER = ubuntu (or your ssh username)
SERVER_SSH_KEY = (paste your private SSH key content)
```

## Step 2: Generate SSH Key (if you don't have one)

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github_deploy -N ""

# Get private key content
cat ~/.ssh/github_deploy
# Copy entire output to SERVER_SSH_KEY secret

# Get public key
cat ~/.ssh/github_deploy.pub
# Add to server: ~/.ssh/authorized_keys
```

## Step 3: Setup Server (One-time)

SSH into your server and run:

```bash
sudo apt-get update && sudo apt-get install -y docker.io docker-compose git
sudo mkdir -p /app/liquid-launch-bot
cd /app/liquid-launch-bot
sudo git clone https://github.com/Ml0cker/liquid-launch-bot.git .
sudo chown -R $USER:$USER /app/liquid-launch-bot
mkdir -p data
```

## Step 4: Deploy

Push to main branch:
```bash
git push origin main
```

Or manually trigger in GitHub Actions:
- Go to: https://github.com/Ml0cker/liquid-launch-bot/actions
- Click "Deploy Liquid Launch Bot"
- Click "Run workflow"

## Step 5: Monitor

Check deployment:
```bash
# GitHub Actions logs
https://github.com/Ml0cker/liquid-launch-bot/actions

# Server logs
ssh user@server "cd /app/liquid-launch-bot && docker-compose logs -f bot"

# Check Telegram channel
@Liquid_tokens
```

Done! Bot will auto-deploy on every push to main! 🚀
