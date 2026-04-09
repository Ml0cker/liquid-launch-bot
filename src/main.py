import asyncio
import logging
import signal
import sys
from web3 import Web3
from src.config import Config
from src.blockchain.monitor import LiquidMonitor
from src.telegram.bot import TelegramNotifier
from src.utils.database import TokenDatabase
from src.utils.ipfs import IPFSHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LiquidLaunchBot:
    """Main bot orchestrator"""

    def __init__(self):
        logger.info("Initializing Liquid Launch Bot...")

        # Validate config
        Config.validate()

        # Initialize components
        self.w3 = Web3(Web3.HTTPProvider(Config.BASE_RPC_URL))
        self.monitor = LiquidMonitor(self.w3)
        self.notifier = TelegramNotifier()
        self.database = TokenDatabase()
        self.ipfs = IPFSHandler()

        # Register callback
        self.monitor.add_callback(self.on_token_launch)

        logger.info("Bot initialized successfully")

    async def on_token_launch(self, token):
        """Callback when new token is launched"""
        logger.info(f"New token launch detected: {token.name} ({token.symbol})")

        # Check if already processed
        if self.database.is_token_processed(token.address):
            logger.debug(f"Token {token.address} already processed, skipping")
            return

        # Download image if available
        image_path = None
        if token.image_uri:
            image_path = self.ipfs.get_image_path(token.image_uri, token.address)

        # Send notification
        success = await self.notifier.send_launch_notification(token, image_path)

        if success:
            # Mark as processed with full token data
            self.database.mark_token_processed(
                token_address=token.address,
                block_number=token.block_number,
                transaction_hash=token.transaction_hash,
                token_name=token.name,
                token_symbol=token.symbol,
                token_description=token.description,
                token_image_uri=token.image_uri,
                deployer_address=token.deployer,
                pool_hook_address=token.hook_address,
                locker_address=token.locker_address,
                paired_token_address=token.pool_address,
                pool_id=getattr(token, 'pool_id', None),
                starting_tick=getattr(token, 'starting_tick', None),
                extensions_supply=getattr(token, 'extensions_supply', None),
                extensions_list=getattr(token, 'extensions_list', None),
                mev_module_address=getattr(token, 'mev_module', None)
            )
            logger.info(f"Successfully processed token {token.address}")
        else:
            logger.error(f"Failed to send notification for {token.address}")

    async def start(self):
        """Start the bot"""
        logger.info("Starting Liquid Launch Bot...")

        # Send test message
        await self.notifier.send_test_message()

        # Start monitoring
        try:
            await self.monitor.start()
        except KeyboardInterrupt:
            logger.info("Bot interrupted by user")
        except Exception as e:
            logger.error(f"Bot error: {e}")
            raise

    def shutdown(self):
        """Graceful shutdown"""
        logger.info("Shutting down bot...")
        sys.exit(0)


async def main():
    """Main entry point"""
    bot = LiquidLaunchBot()

    # Handle signals
    def signal_handler(sig, frame):
        bot.shutdown()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start bot
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
