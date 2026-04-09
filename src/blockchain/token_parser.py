import logging
from typing import Optional
from web3 import Web3
from src.models.token import TokenLaunch
from src.blockchain.contract_abi import ERC20_ABI

logger = logging.getLogger(__name__)


class TokenParser:
    """Parse token data from blockchain events"""

    def __init__(self, w3: Web3):
        self.w3 = w3

    def parse_token_created_event(self, event: dict) -> TokenLaunch:
        """Parse TokenCreated event into TokenLaunch model"""
        try:
            args = event["args"]

            # Helper to safely normalize addresses (skip 0x0)
            def safe_address(addr):
                if addr == "0x0" or addr == "0x0000000000000000000000000000000000000000":
                    return None
                try:
                    return Web3.to_checksum_address(addr)
                except:
                    return None

            # Extract extensions list
            extensions_list = args.get("extensions", [])
            extensions_list = [safe_address(ext) for ext in extensions_list if safe_address(ext)]

            token = TokenLaunch(
                address=Web3.to_checksum_address(args["tokenAddress"]),
                name=args.get("tokenName", "Unknown"),
                symbol=args.get("tokenSymbol", "???"),
                description=args.get("tokenMetadata", ""),
                image_uri=args.get("tokenImage", ""),
                market_cap=0.0,
                dev_buy=0.0,
                block_number=event["blockNumber"],
                transaction_hash=event["transactionHash"].hex(),
                pool_address=safe_address(args.get("pairedToken", "0x0")),
                deployer=Web3.to_checksum_address(args["tokenAdmin"]),
                hook_address=safe_address(args.get("poolHook", "0x0")),
                locker_address=safe_address(args.get("locker", "0x0")),
                pool_id=args.get("poolId", "").hex() if args.get("poolId") else None,
                starting_tick=args.get("startingTick"),
                mev_module=safe_address(args.get("mevModule", "0x0")),
                extensions_supply=args.get("extensionsSupply"),
                extensions_list=extensions_list if extensions_list else None,
            )

            return token
        except Exception as e:
            logger.error(f"Error parsing token event: {e}")
            raise

    def fetch_token_metadata(self, token_address: str) -> dict:
        """Fetch ERC20 token metadata from blockchain"""
        try:
            token_address = Web3.to_checksum_address(token_address)
            contract = self.w3.eth.contract(address=token_address, abi=ERC20_ABI)

            metadata = {
                "name": contract.functions.name().call(),
                "symbol": contract.functions.symbol().call(),
                "decimals": contract.functions.decimals().call(),
                "total_supply": contract.functions.totalSupply().call(),
            }

            return metadata
        except Exception as e:
            logger.warning(f"Error fetching metadata for {token_address}: {e}")
            return {}

    def calculate_market_cap(
        self,
        token_address: str,
        pool_address: Optional[str],
        eth_price: float = 3000.0  # Default ETH price in USD
    ) -> float:
        """
        Calculate market cap based on pool liquidity
        For now, returns 0 as we need pool contract interaction
        """
        try:
            if not pool_address or pool_address == "0x0000000000000000000000000000000000000000":
                return 0.0

            # TODO: Implement pool interaction to get token price
            # This would require Uniswap V4 pool contract interaction
            return 0.0
        except Exception as e:
            logger.warning(f"Error calculating market cap: {e}")
            return 0.0
