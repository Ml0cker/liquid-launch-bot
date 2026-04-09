# Liquid Protocol Launch Bot

Automated Telegram bot that monitors new token launches on Liquid Protocol (Base chain) and sends real-time notifications to a public Telegram channel.

## Features

✅ Real-time monitoring of TokenCreated events on Liquid Protocol  
✅ Historical block scanning (configurable range)  
✅ Complete token data collection (creator, addresses, pool info)  
✅ IPFS image retrieval and display  
✅ Duplicate prevention via SQLite database  
✅ English-only notifications with copyable contract addresses  
✅ Docker containerization for 24/7 operation  
✅ GitHub Actions CI/CD deployment  

## Quick Start

### Local Development

1. Clone repository:
```bash
git clone https://github.com/YOUR_USERNAME/liquid-launch-bot.git
cd liquid-launch-bot
```

2. Create .env file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start bot with Docker:
```bash
docker-compose up --build
```

### Server Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for GitHub Actions setup and server configuration.

## Configuration

Edit `.env` file:

```env
# Blockchain RPC
BASE_RPC_URL=https://mainnet.base.org

# Liquid Protocol Factory Contract
LIQUID_FACTORY_ADDRESS=0x04f1a284168743759be6554f607a10cebdb77760

# Starting block for historical scanning
START_BLOCK=42266500

# Telegram Bot Token (get from @BotFather)
TELEGRAM_BOT_TOKEN=your_token_here

# Telegram Channel (use @channel_name for public, -100ID for private)
TELEGRAM_CHAT_ID=@your_channel

# IPFS Gateway for image retrieval
IPFS_GATEWAY=https://ipfs.io/ipfs/

# Polling interval in seconds
POLL_INTERVAL=12
```

## Database Schema

SQLite database stores complete token information:

- `token_address` - Token contract address (PRIMARY KEY)
- `token_name` - Token name
- `token_symbol` - Token symbol
- `token_description` - Token metadata/description
- `token_image_uri` - IPFS image URI
- `deployer_address` - Token creator address
- `pool_hook_address` - Pool hook contract
- `locker_address` - Locker contract
- `paired_token_address` - Paired token address
- `mev_module_address` - MEV module address
- `pool_id` - Uniswap V4 pool ID
- `starting_tick` - Pool starting tick
- `extensions_supply` - Extensions supply amount
- `extensions_list` - List of extension addresses
- `block_number` - Launch block
- `transaction_hash` - Launch transaction hash
- `timestamp` - Processing timestamp

## Notification Format

```
🚀 New Token Launch on Liquid Protocol!

📛 Name: Token Name (SYMBOL)
📝 Description: Token description...
👨‍💻 Creator: 0x...
📦 Block: 12345678

Contract Address:
0x...

🔍 DEXScreener
📄 Contract
📋 Transaction
```

## Project Structure

```
liquid-launch-bot/
├── .github/workflows/
│   └── deploy.yml              # GitHub Actions deployment
├── src/
│   ├── main.py                 # Bot orchestrator
│   ├── config.py               # Configuration loader
│   ├── blockchain/
│   │   ├── monitor.py          # Event monitoring
│   │   ├── contract_abi.py     # Contract ABI
│   │   └── token_parser.py     # Event parsing
│   ├── telegram/
│   │   ├── bot.py              # Telegram integration
│   │   └── formatter.py        # Message formatting
│   ├── utils/
│   │   ├── database.py         # SQLite operations
│   │   ├── ipfs.py             # IPFS image handling
│   │   └── dexscreener.py      # Link generation
│   └── models/
│       └── token.py            # Token data model
├── docker-compose.yml          # Docker Compose config
├── Dockerfile                  # Docker image
├── requirements.txt            # Python dependencies
├── .env.example                # Configuration template
├── DEPLOYMENT.md               # Deployment guide
└── README.md                   # This file
```

## Monitoring

Check bot status:
```bash
docker-compose ps
docker-compose logs -f bot
```

Query database:
```bash
docker-compose exec -T bot python3 -c "
import sqlite3
conn = sqlite3.connect('/app/data/tokens.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM processed_tokens')
print(f'Total tokens: {cursor.fetchone()[0]}')
conn.close()
"
```

## Troubleshooting

### Bot not finding events
- Check `LIQUID_FACTORY_ADDRESS` is correct
- Verify `BASE_RPC_URL` is accessible
- Check `START_BLOCK` is valid

### Telegram messages not sending
- Verify `TELEGRAM_BOT_TOKEN` is valid
- Check `TELEGRAM_CHAT_ID` format (@channel or -100ID)
- Ensure bot has permissions in channel

### Docker issues
- Rebuild: `docker-compose down && docker-compose up --build`
- Check logs: `docker-compose logs bot`
- Clear data: `rm -f data/tokens.db`

## License

MIT

## Support

For issues and questions, open a GitHub issue.
