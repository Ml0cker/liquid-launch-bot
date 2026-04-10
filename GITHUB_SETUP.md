# GitHub Setup Instructions

## Step 1: Create Repository on GitHub

1. Go to: https://github.com/new
2. Fill in:
   - Repository name: `liquid-launch-bot`
   - Description: `Automated Telegram bot for Liquid Protocol token launches`
   - Visibility: **Public**
   - Initialize with: **None** (we already have code)
3. Click "Create repository"

## Step 2: Push Code to GitHub

After creating the repository, run these commands:

```bash
cd "c:/2026/Liquid deploys"

# Add remote
git remote add origin https://github.com/Ml0cker/liquid-launch-bot.git

# Push to main branch
git branch -M main
git push -u origin main
```

When prompted for password, use your GitHub Personal Access Token:
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `workflow`
4. Copy token and paste when prompted

## Step 3: Add GitHub Secrets

After code is pushed:

1. Go to: https://github.com/Ml0cker/liquid-launch-bot/settings/secrets/actions
2. Click "New repository secret"
3. Add these secrets:

### Environment Secrets
- `BASE_RPC_URL` = `https://mainnet.base.org`
- `LIQUID_FACTORY_ADDRESS` = `0x04f1a284168743759be6554f607a10cebdb77760`
- `START_BLOCK` = `42266500`
- `TELEGRAM_BOT_TOKEN` = `8546165371:AAFXXRtj42oQwfaKgMwgubhWI-_8jfryb1E`
- `TELEGRAM_CHAT_ID` = `@Liquid_tokens`
- `IPFS_GATEWAY` = `https://ipfs.io/ipfs/`
- `POLL_INTERVAL` = `12`

### Server Secrets
- `SERVER_HOST` = Your server IP/domain
- `SERVER_USER` = SSH username (e.g., ubuntu)
- `SERVER_SSH_KEY` = Your private SSH key

## Step 4: Deploy

After secrets are added, trigger deployment:

```bash
# Push any change to main
git commit --allow-empty -m "Trigger deployment"
git push origin main
```

Or manually trigger in GitHub Actions:
- Go to: https://github.com/Ml0cker/liquid-launch-bot/actions
- Click "Deploy Liquid Launch Bot"
- Click "Run workflow"

Done! 🚀
