# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (Python)
python -m src.main

# Run with Docker
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f bot

# Stop
docker-compose down
```

### Server Deployment
Deployment is automated via GitHub Actions. Pushing to `main` branch triggers deployment to the server configured in `.github/workflows/deploy.yml`.

Manual deployment:
- Go to Actions → "Deploy Liquid Launch Bot" → "Run workflow"

### Monitoring & Debugging
```bash
# Check container status
docker-compose ps

# Query database - count processed tokens
docker-compose exec -T bot python3 -c "
import sqlite3
conn = sqlite3.connect('/app/data/tokens.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM processed_tokens')
print(f'Total tokens: {cursor.fetchone()[0]}')
conn.close()
"

# Check specific token in DB
sqlite3 data/tokens.db "SELECT * FROM processed_tokens WHERE token_address = '0x...';"
```

## Architecture

This is a Telegram bot that monitors `TokenCreated` events from the Liquid Protocol Factory contract on Base chain and posts notifications to a Telegram channel.

### Component Flow
```
Base RPC → LiquidMonitor → TokenParser → TokenLaunch model
                                            ↓
                                    TokenDatabase (duplicate check)
                                            ↓
                                    IPFSHandler (image download)
                                            ↓
                                    TelegramNotifier → Telegram Channel
                                            ↓
                                    TokenDatabase (save record)
```

### Key Modules

- **src/main.py** - Entry point, orchestrates all components via `LiquidLaunchBot` class
- **src/blockchain/monitor.py** - `LiquidMonitor` polls Base RPC for new blocks and `TokenCreated` events
- **src/blockchain/token_parser.py** - `TokenParser` extracts token data from events
- **src/telegram/bot.py** - `TelegramNotifier` sends messages/photos to Telegram
- **src/telegram/formatter.py** - `MessageFormatter` formats notification messages
- **src/utils/database.py** - `TokenDatabase` (SQLite) prevents duplicate notifications
- **src/utils/ipfs.py** - `IPFSHandler` downloads token images from IPFS
- **src/config.py** - `Config` loads and validates environment variables

### Database Schema
SQLite at `data/tokens.db` with `processed_tokens` table storing full token metadata including addresses, pool info, and transaction details.

## Configuration

All configuration via `.env` file. Required for local development:
- `BASE_RPC_URL` - Base chain RPC endpoint
- `TELEGRAM_BOT_TOKEN` - From @BotFather
- `TELEGRAM_CHAT_ID` - Channel ID (use @channel for public, -100ID for private)
- `LIQUID_FACTORY_ADDRESS` - Factory contract address
- `START_BLOCK` - Starting block for historical scanning

## GitHub Actions

The deployment workflow uses `appleboy/ssh-action@v1.0.3` to connect to the production server via SSH. Required GitHub Secrets:
- `SERVER_HOST`, `SERVER_USER`, `SERVER_PASSWORD` - Server connection
- `BASE_RPC_URL`, `TELEGRAM_BOT_TOKEN`, etc. - Application config

Workflow: SSH → `git pull` → rebuild Docker → restart container → show logs
