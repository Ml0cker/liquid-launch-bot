# GitHub Actions Deployment Setup

## Required GitHub Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

### 1. SERVER_HOST
- **Description**: IP address or domain of your server
- **Example**: `123.45.67.89` or `bot.example.com`

### 2. SERVER_USER
- **Description**: SSH username for server connection
- **Example**: `ubuntu` or `root`

### 3. SERVER_SSH_KEY
- **Description**: Private SSH key for server authentication
- **How to generate**:
  ```bash
  ssh-keygen -t rsa -b 4096 -f ~/.ssh/github_deploy
  # Copy contents of ~/.ssh/github_deploy (private key)
  # Add ~/.ssh/github_deploy.pub to server ~/.ssh/authorized_keys
  ```

## Server Setup

Execute on your server:

```bash
# 1. Install Docker and Docker Compose
sudo apt-get update
sudo apt-get install -y docker.io docker-compose git

# 2. Create project directory
sudo mkdir -p /app/liquid-launch-bot
cd /app/liquid-launch-bot

# 3. Clone repository
sudo git clone https://github.com/YOUR_USERNAME/liquid-launch-bot.git .

# 4. Create .env file with configuration
sudo nano .env
# Add:
# BASE_RPC_URL=https://mainnet.base.org
# LIQUID_FACTORY_ADDRESS=0x04f1a284168743759be6554f607a10cebdb77760
# START_BLOCK=42266500
# TELEGRAM_BOT_TOKEN=your_token_here
# TELEGRAM_CHAT_ID=@your_channel
# IPFS_GATEWAY=https://ipfs.io/ipfs/
# POLL_INTERVAL=12

# 5. Set permissions
sudo chown -R $USER:$USER /app/liquid-launch-bot

# 6. Start bot
docker-compose up -d
```

## Deployment Flow

1. Push to main branch
2. GitHub Actions automatically:
   - Connects to server via SSH
   - Updates code (git pull)
   - Rebuilds Docker image
   - Restarts container
   - Shows logs

## Manual Deployment

Use workflow_dispatch to deploy manually:
- Go to Actions → Deploy Liquid Launch Bot → Run workflow

## Monitoring

Check bot status on server:
```bash
ssh user@server
cd /app/liquid-launch-bot
docker-compose ps
docker-compose logs -f bot
```

## Troubleshooting

### SSH connection failed
- Check SERVER_HOST and SERVER_USER
- Ensure public key is in ~/.ssh/authorized_keys on server

### Docker not found
- Install Docker: `sudo apt-get install docker.io docker-compose`

### Permission denied
- Add user to docker group: `sudo usermod -aG docker $USER`
