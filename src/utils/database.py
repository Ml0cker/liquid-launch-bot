import sqlite3
import logging
import os
from datetime import datetime
from src.config import Config

logger = logging.getLogger(__name__)


class TokenDatabase:
    """SQLite database for tracking processed tokens"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DB_PATH
        self._ensure_db_dir()
        self.init_db()

    def _ensure_db_dir(self):
        """Ensure database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    def init_db(self):
        """Initialize database schema"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processed_tokens (
                    token_address TEXT PRIMARY KEY,
                    token_name TEXT,
                    token_symbol TEXT,
                    token_description TEXT,
                    token_image_uri TEXT,
                    deployer_address TEXT,
                    pool_hook_address TEXT,
                    locker_address TEXT,
                    paired_token_address TEXT,
                    mev_module_address TEXT,
                    pool_id TEXT,
                    starting_tick INTEGER,
                    extensions_supply INTEGER,
                    extensions_list TEXT,
                    block_number INTEGER NOT NULL,
                    transaction_hash TEXT NOT NULL,
                    timestamp INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            conn.close()
            logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise

    def is_token_processed(self, token_address: str) -> bool:
        """Check if token has already been processed"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT 1 FROM processed_tokens WHERE token_address = ?",
                (token_address.lower(),)
            )

            result = cursor.fetchone() is not None
            conn.close()
            return result
        except Exception as e:
            logger.error(f"Error checking token: {e}")
            return False

    def mark_token_processed(
        self,
        token_address: str,
        block_number: int,
        transaction_hash: str,
        token_name: str = None,
        token_symbol: str = None,
        token_description: str = None,
        token_image_uri: str = None,
        deployer_address: str = None,
        pool_hook_address: str = None,
        locker_address: str = None,
        paired_token_address: str = None,
        mev_module_address: str = None,
        pool_id: str = None,
        starting_tick: int = None,
        extensions_supply: int = None,
        extensions_list: str = None
    ):
        """Mark token as processed with full data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            timestamp = int(datetime.now().timestamp())

            cursor.execute("""
                INSERT OR IGNORE INTO processed_tokens
                (token_address, token_name, token_symbol, token_description, token_image_uri,
                 deployer_address, pool_hook_address, locker_address, paired_token_address,
                 mev_module_address, pool_id, starting_tick, extensions_supply, extensions_list,
                 block_number, transaction_hash, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                token_address.lower(),
                token_name,
                token_symbol,
                token_description,
                token_image_uri,
                deployer_address,
                pool_hook_address,
                locker_address,
                paired_token_address,
                mev_module_address,
                pool_id,
                starting_tick,
                extensions_supply,
                extensions_list,
                block_number,
                transaction_hash,
                timestamp
            ))

            conn.commit()
            conn.close()
            logger.debug(f"Marked token {token_address} as processed with full data")
        except Exception as e:
            logger.error(f"Error marking token as processed: {e}")

    def get_processed_count(self) -> int:
        """Get count of processed tokens"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM processed_tokens")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            logger.error(f"Error getting processed count: {e}")
            return 0
