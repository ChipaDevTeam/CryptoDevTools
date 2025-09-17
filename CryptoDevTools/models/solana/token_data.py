from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal

@dataclass
class HoldersData:
    """A structured class to hold token holder information."""
    total_holders: int
    top_holders: List[Any]

@dataclass
class TokenMetadata:
    """
    A structured class to hold token metadata information.
    """
    last_indexed_slot: int
    interface: str
    id: str
    content: dict
    authorities: Dict[str, Any]
    compression: List[Any]
    collection: Dict[str, Any]
    royalty: Dict[str, Any]
    creators: List[Dict[str, Any]]
    ownership: Dict[str, Any]
    supply: Dict[str, Any]
    mutable: bool
    burnt: bool
    token_info: Dict[str, Any]

@dataclass
class PumpFunCoin:
    """Represents a PumpFun coin with all its properties."""
    mint: str
    name: str
    symbol: str
    description: str
    image_uri: Optional[str] = None
    metadata_uri: Optional[str] = None
    twitter: Optional[str] = None
    telegram: Optional[str] = None
    website: Optional[str] = None
    bonding_curve: Optional[str] = None
    associated_bonding_curve: Optional[str] = None
    creator: Optional[str] = None
    created_timestamp: Optional[int] = None
    raydium_pool: Optional[str] = None
    complete: bool = False
    virtual_sol_reserves: Optional[int] = None
    virtual_token_reserves: Optional[int] = None
    total_supply: Optional[int] = None
    show_name: bool = True
    king_of_the_hill_timestamp: Optional[int] = None
    market_cap: Optional[float] = None
    usd_market_cap: Optional[float] = None
    reply_count: int = 0
    last_reply: Optional[int] = None
    nsfw: bool = False
    market_id: Optional[str] = None
    banner_uri: Optional[str] = None
    video_uri: Optional[str] = None
    is_banned: bool = False
    program: Optional[str] = None
    is_currently_live: bool = False

    @property
    def created_datetime(self) -> Optional[datetime]:
        """Convert timestamp to datetime object."""
        if self.created_timestamp:
            return datetime.fromtimestamp(self.created_timestamp / 1000)
        return None

    @property
    def last_reply_datetime(self) -> Optional[datetime]:
        """Convert last reply timestamp to datetime object."""
        if self.last_reply:
            return datetime.fromtimestamp(self.last_reply / 1000)
        return None

    @property
    def king_of_hill_datetime(self) -> Optional[datetime]:
        """Convert king of the hill timestamp to datetime object."""
        if self.king_of_the_hill_timestamp:
            return datetime.fromtimestamp(self.king_of_the_hill_timestamp / 1000)
        return None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PumpFunCoin':
        """Create PumpFunCoin instance from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

@dataclass
class PumpFunToken:
    """Represents a complete PumpFun token entry."""
    coin: PumpFunCoin
    description: str
    modified_by: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PumpFunToken':
        """Create PumpFunToken instance from API response."""
        coin_data = data.get('coin', {})
        return cls(
            coin=PumpFunCoin.from_dict(coin_data),
            description=data.get('description', ''),
            modified_by=data.get('modifiedBy', '')
        )

@dataclass
class TokenPrice:
    """Represents token price information."""
    price_usd: Optional[Decimal] = None
    price_sol: Optional[Decimal] = None
    market_cap_usd: Optional[Decimal] = None
    volume_24h: Optional[Decimal] = None
    price_change_24h: Optional[float] = None
    last_updated: Optional[datetime] = None

@dataclass
class ExchangeInfo:
    """Information about where a token is traded."""
    exchange_name: str
    pair: str
    price: Optional[Decimal] = None
    volume_24h: Optional[Decimal] = None
    liquidity: Optional[Decimal] = None

@dataclass
class TokenSecurity:
    """Token security and risk information."""
    is_mintable: bool = False
    is_freezable: bool = False
    has_freeze_authority: bool = False
    has_mint_authority: bool = False
    top_10_holder_percent: Optional[float] = None
    creator_balance_percent: Optional[float] = None
    is_rugpull_risk: bool = False

@dataclass
class SolanaToken:
    """Comprehensive Solana token model combining all data sources."""
    # Basic token info
    mint_address: str
    name: str
    symbol: str
    decimals: int
    
    # Metadata
    description: Optional[str] = None
    image_uri: Optional[str] = None
    website: Optional[str] = None
    twitter: Optional[str] = None
    telegram: Optional[str] = None
    
    # Supply and economics
    total_supply: Optional[int] = None
    circulating_supply: Optional[int] = None
    max_supply: Optional[int] = None
    
    # Trading data
    price_info: Optional[TokenPrice] = None
    exchanges: List[ExchangeInfo] = None
    
    # Holder information
    holders_data: Optional[HoldersData] = None
    
    # Security analysis
    security_info: Optional[TokenSecurity] = None
    
    # PumpFun specific data (if applicable)
    pumpfun_data: Optional[PumpFunToken] = None
    
    # Metadata from Helius/other APIs
    helius_metadata: Optional[TokenMetadata] = None
    
    # Timestamps
    created_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize default values after creation."""
        if self.exchanges is None:
            self.exchanges = []

    @property
    def is_pumpfun_token(self) -> bool:
        """Check if this is a PumpFun token."""
        return self.pumpfun_data is not None

    @property
    def market_cap_usd(self) -> Optional[Decimal]:
        """Get market cap in USD."""
        if self.price_info and self.price_info.market_cap_usd:
            return self.price_info.market_cap_usd
        elif self.pumpfun_data and self.pumpfun_data.coin.usd_market_cap:
            return Decimal(str(self.pumpfun_data.coin.usd_market_cap))
        return None

    def add_exchange_info(self, exchange: ExchangeInfo):
        """Add exchange information."""
        self.exchanges.append(exchange)

    def update_price_info(self, price_info: TokenPrice):
        """Update price information."""
        self.price_info = price_info
        self.last_updated = datetime.now()

    @classmethod
    def from_pumpfun_data(cls, pumpfun_token: PumpFunToken) -> 'SolanaToken':
        """Create SolanaToken from PumpFun data."""
        coin = pumpfun_token.coin
        
        price_info = TokenPrice(
            market_cap_usd=Decimal(str(coin.usd_market_cap)) if coin.usd_market_cap else None,
            last_updated=datetime.now()
        )
        
        return cls(
            mint_address=coin.mint,
            name=coin.name,
            symbol=coin.symbol,
            decimals=9,  # Standard for PumpFun tokens
            description=coin.description,
            image_uri=coin.image_uri,
            website=coin.website,
            twitter=coin.twitter,
            telegram=coin.telegram,
            total_supply=coin.total_supply,
            price_info=price_info,
            pumpfun_data=pumpfun_token,
            created_at=coin.created_datetime,
            last_updated=datetime.now()
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = {}
        for field in self.__dataclass_fields__:
            value = getattr(self, field)
            if isinstance(value, datetime):
                result[field] = value.isoformat()
            elif isinstance(value, Decimal):
                result[field] = float(value)
            elif hasattr(value, 'to_dict'):
                result[field] = value.to_dict()
            elif isinstance(value, list) and value and hasattr(value[0], 'to_dict'):
                result[field] = [item.to_dict() for item in value]
            else:
                result[field] = value
        return result