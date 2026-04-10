import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Blockchain
    BASE_RPC_URL = os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
    LIQUID_FACTORY_ADDRESS = os.getenv(
        "LIQUID_FACTORY_ADDRESS", "0x04f1a284168743759be6554f607a10cebdb77760"
    )
    START_BLOCK = int(os.getenv("START_BLOCK", "19000000"))

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Может быть @channel или -100123456

    # IPFS
    IPFS_GATEWAY = os.getenv("IPFS_GATEWAY", "https://ipfs.io/ipfs/")

    # Polling
    POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "2"))

    # Database
    DB_PATH = "/app/data/tokens.db"

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        if not cls.TELEGRAM_CHAT_ID:
            raise ValueError("TELEGRAM_CHAT_ID is required")
        return True
