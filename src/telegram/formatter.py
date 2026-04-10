import logging
import json
from src.models.token import TokenLaunch
from src.utils.dexscreener import DEXScreenerHelper

logger = logging.getLogger(__name__)


class MessageFormatter:
    """Format token launch messages for Telegram"""

    @staticmethod
    def format_launch_message(token: TokenLaunch) -> str:
        """Format token launch into Telegram message"""

        dex_link = DEXScreenerHelper.generate_dexscreener_link(token.address)
        basescan_link = DEXScreenerHelper.generate_basescan_link(token.address)
        tx_link = DEXScreenerHelper.generate_basescan_tx_link(token.transaction_hash)

        # Parse description from JSON metadata
        description = "No description"
        if token.description:
            try:
                # Try to parse as JSON
                metadata = json.loads(token.description)
                if isinstance(metadata, dict) and "description" in metadata:
                    description = metadata["description"]
                else:
                    description = token.description
            except (json.JSONDecodeError, TypeError):
                # If not JSON, use as-is
                description = token.description

        # Truncate if too long
        if len(description) > 150:
            description = description[:147] + "..."

        message = f"""🚀 <b>New Token Launch on Liquid Protocol!</b>

📛 <b>Name:</b> {token.name} ({token.symbol})
📝 <b>Description:</b> {description}
👨‍💻 <b>Creator:</b> <code>{token.deployer}</code>
📦 <b>Block:</b> {token.block_number}

<b>Contract Address:</b>
<code>{token.address}</code>

💎 <a href="https://app.liquidprotocol.org/tokens/{token.address}">Liquid Protocol</a>
🔍 <a href="{dex_link}">DEXScreener</a>
📄 <a href="{basescan_link}">Contract</a>
📋 <a href="{tx_link}">Transaction</a>"""

        return message

    @staticmethod
    def format_error_message(error: str) -> str:
        """Format error message"""
        return f"❌ <b>Error:</b> {error}"
