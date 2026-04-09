import logging

logger = logging.getLogger(__name__)


class DEXScreenerHelper:
    """Generate DEXScreener links"""

    @staticmethod
    def generate_dexscreener_link(token_address: str, chain: str = "base") -> str:
        """Generate DEXScreener link for token"""
        return f"https://dexscreener.com/{chain}/{token_address}"

    @staticmethod
    def generate_basescan_link(token_address: str) -> str:
        """Generate BaseScan link for token"""
        return f"https://basescan.org/address/{token_address}"

    @staticmethod
    def generate_basescan_tx_link(tx_hash: str) -> str:
        """Generate BaseScan transaction link"""
        return f"https://basescan.org/tx/{tx_hash}"
