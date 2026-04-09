from dataclasses import dataclass
from typing import Optional, List


@dataclass
class TokenLaunch:
    """Model for token launch data"""
    address: str
    name: str
    symbol: str
    description: Optional[str]
    image_uri: Optional[str]
    market_cap: float
    dev_buy: float
    block_number: int
    transaction_hash: str
    pool_address: Optional[str]
    deployer: str
    hook_address: Optional[str] = None
    locker_address: Optional[str] = None
    pool_id: Optional[str] = None
    starting_tick: Optional[int] = None
    mev_module: Optional[str] = None
    extensions_supply: Optional[int] = None
    extensions_list: Optional[List[str]] = None
