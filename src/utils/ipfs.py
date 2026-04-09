import logging
import requests
import os
from typing import Optional
from src.config import Config

logger = logging.getLogger(__name__)


class IPFSHandler:
    """Handle IPFS image downloads"""

    def __init__(self, gateway: str = None):
        self.gateway = gateway or Config.IPFS_GATEWAY
        self.temp_dir = "/app/data/images"
        self._ensure_temp_dir()

    def _ensure_temp_dir(self):
        """Ensure temp directory exists"""
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir, exist_ok=True)

    def download_image(self, ipfs_hash: str, timeout: int = 10) -> Optional[bytes]:
        """Download image from IPFS"""
        if not ipfs_hash:
            return None

        try:
            # Handle both full IPFS URIs and just hashes
            if ipfs_hash.startswith("ipfs://"):
                ipfs_hash = ipfs_hash.replace("ipfs://", "")

            url = f"{self.gateway}{ipfs_hash}"
            logger.debug(f"Downloading image from {url}")

            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            return response.content
        except Exception as e:
            logger.warning(f"Error downloading image from IPFS: {e}")
            return None

    def save_temp_image(
        self,
        image_data: bytes,
        token_address: str
    ) -> Optional[str]:
        """Save image to temporary file"""
        try:
            filename = f"{token_address.lower()}.jpg"
            filepath = os.path.join(self.temp_dir, filename)

            with open(filepath, "wb") as f:
                f.write(image_data)

            logger.debug(f"Saved image to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving image: {e}")
            return None

    def get_image_path(self, ipfs_hash: str, token_address: str) -> Optional[str]:
        """Download and save image, return path"""
        if not ipfs_hash:
            return None

        image_data = self.download_image(ipfs_hash)
        if image_data:
            return self.save_temp_image(image_data, token_address)

        return None
