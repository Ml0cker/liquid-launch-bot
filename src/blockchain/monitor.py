import asyncio
import logging
import time
from typing import List, Callable, Optional
from web3 import Web3
from src.config import Config
from src.blockchain.contract_abi import LIQUID_FACTORY_ABI
from src.blockchain.token_parser import TokenParser

logger = logging.getLogger(__name__)


class LiquidMonitor:
    """Monitor Liquid Protocol for new token launches"""

    def __init__(self, w3: Web3):
        self.w3 = w3
        self.config = Config
        self.parser = TokenParser(w3)
        self.contract = self._init_contract()
        self.last_block = self.config.START_BLOCK
        self.callbacks: List[Callable] = []

    def _init_contract(self):
        """Initialize contract instance"""
        factory_address = Web3.to_checksum_address(self.config.LIQUID_FACTORY_ADDRESS)
        return self.w3.eth.contract(address=factory_address, abi=LIQUID_FACTORY_ABI)

    def add_callback(self, callback: Callable):
        """Add callback to be called when new token is found"""
        self.callbacks.append(callback)

    def get_latest_block(self) -> int:
        """Get latest block number"""
        try:
            return self.w3.eth.block_number
        except Exception as e:
            logger.error(f"Error getting latest block: {e}")
            return self.last_block

    def fetch_token_created_events(
        self,
        from_block: int,
        to_block: int
    ) -> List[dict]:
        """Fetch TokenCreated events from blockchain"""
        try:
            # Получаем ВСЕ логи с контракта без фильтра по topic
            logs = self.w3.eth.get_logs({
                'address': self.contract.address,
                'fromBlock': from_block,
                'toBlock': to_block
            })

            logger.info(f"Found {len(logs)} total logs from block {from_block} to {to_block}")

            events = []
            for i, log in enumerate(logs):
                try:
                    # Пытаемся декодировать как TokenCreated
                    event = self.contract.events.TokenCreated().process_log(log)
                    events.append(event)
                    logger.info(f"✓ TokenCreated #{i+1}: {event['args'].get('name', 'N/A')} ({event['args'].get('symbol', 'N/A')})")
                except Exception as e:
                    # Если не получилось, выводим информацию для отладки
                    logger.debug(f"Log #{i+1} decode error: {str(e)[:100]}")
                    logger.debug(f"  TX: {log['transactionHash'].hex()}")
                    logger.debug(f"  Topics: {len(log['topics'])}, Data: {len(log['data'])} bytes")
                    continue

            logger.info(f"Successfully decoded {len(events)} events")
            return events
        except Exception as e:
            logger.error(f"Error fetching events: {e}")
            return []

    async def process_events(self, events: List[dict]):
        """Process token created events"""
        for event in events:
            try:
                token = self.parser.parse_token_created_event(event)
                logger.info(f"Processing token: {token.name} ({token.symbol}) at {token.address}")

                # Call all registered callbacks
                for callback in self.callbacks:
                    try:
                        await callback(token)
                    except Exception as e:
                        logger.error(f"Error in callback: {e}")

            except Exception as e:
                logger.error(f"Error processing event: {e}")

    async def start(self):
        """Start monitoring loop"""
        logger.info(f"Starting Liquid Protocol monitor from block {self.last_block}")

        # If we're far behind, scan in batches of 1000 blocks
        batch_size = 1000
        current_block = self.get_latest_block()

        if current_block - self.last_block > batch_size:
            logger.info(f"Scanning {current_block - self.last_block} blocks in batches of {batch_size}")

            while self.last_block < current_block:
                try:
                    to_block = min(self.last_block + batch_size, current_block)
                    logger.debug(f"Batch scanning blocks {self.last_block + 1} to {to_block}")

                    events = self.fetch_token_created_events(
                        from_block=self.last_block + 1,
                        to_block=to_block
                    )

                    if events:
                        await self.process_events(events)

                    self.last_block = to_block

                except Exception as e:
                    logger.error(f"Error in batch scan: {e}")
                    await asyncio.sleep(self.config.POLL_INTERVAL)

        # Now switch to normal polling
        logger.info("Batch scan complete, switching to real-time polling")

        while True:
            try:
                current_block = self.get_latest_block()

                if current_block > self.last_block:
                    logger.debug(f"Checking blocks {self.last_block + 1} to {current_block}")

                    events = self.fetch_token_created_events(
                        from_block=self.last_block + 1,
                        to_block=current_block
                    )

                    if events:
                        await self.process_events(events)

                    self.last_block = current_block

                # Wait before next poll
                await asyncio.sleep(self.config.POLL_INTERVAL)

            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                await asyncio.sleep(self.config.POLL_INTERVAL)
