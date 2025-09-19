from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from enum import Enum

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from enum import Enum

class TradeType(Enum):
    """Enumeration for trade types."""
    BUY = "buy"
    SELL = "sell"

class TradingProgram(Enum):
    """Enumeration for trading programs."""
    PUMP_AMM = "pump_amm"
    RAYDIUM = "raydium"
    ORCA = "orca"
    JUPITER = "jupiter"

@dataclass
class Trade:
    """Represents a single trade transaction."""
    slot_index_id: str
    tx: str  # Transaction hash
    timestamp: str  # ISO timestamp
    user_address: str
    trade_type: TradeType
    program: TradingProgram
    price_usd: Decimal
    price_sol: Decimal
    amount_usd: Decimal
    amount_sol: Decimal
    base_amount: Decimal
    quote_amount: Decimal

    @property
    def timestamp_datetime(self) -> datetime:
        """Convert ISO timestamp string to datetime object."""
        return datetime.fromisoformat(self.timestamp.replace('Z', '+00:00'))

    @property
    def is_buy(self) -> bool:
        """Check if this is a buy trade."""
        return self.trade_type == TradeType.BUY

    @property
    def is_sell(self) -> bool:
        """Check if this is a sell trade."""
        return self.trade_type == TradeType.SELL

    @property
    def transaction_url(self) -> str:
        """Get Solana explorer URL for this transaction."""
        return f"https://solscan.io/tx/{self.tx}"

    @property
    def wallet_url(self) -> str:
        """Get Solana explorer URL for the wallet."""
        return f"https://solscan.io/account/{self.user_address}"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Trade':
        """Create Trade instance from API response."""
        return cls(
            slot_index_id=data.get('slotIndexId', ''),
            tx=data.get('tx', ''),
            timestamp=data.get('timestamp', ''),
            user_address=data.get('userAddress', ''),
            trade_type=TradeType(data.get('type', 'buy')),
            program=TradingProgram(data.get('program', 'pump_amm')),
            price_usd=Decimal(str(data.get('priceUsd', '0'))),
            price_sol=Decimal(str(data.get('priceSol', '0'))),
            amount_usd=Decimal(str(data.get('amountUsd', '0'))),
            amount_sol=Decimal(str(data.get('amountSol', '0'))),
            base_amount=Decimal(str(data.get('baseAmount', '0'))),
            quote_amount=Decimal(str(data.get('quoteAmount', '0')))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Trade to dictionary."""
        return {
            'slotIndexId': self.slot_index_id,
            'tx': self.tx,
            'timestamp': self.timestamp,
            'userAddress': self.user_address,
            'type': self.trade_type.value,
            'program': self.program.value,
            'priceUsd': str(self.price_usd),
            'priceSol': str(self.price_sol),
            'amountUsd': str(self.amount_usd),
            'amountSol': str(self.amount_sol),
            'baseAmount': str(self.base_amount),
            'quoteAmount': str(self.quote_amount)
        }

@dataclass
class TradePagination:
    """Represents pagination information for trade responses."""
    has_next_page: bool = False
    cursor: Optional[str] = None
    total_count: Optional[int] = None
    page_size: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TradePagination':
        """Create TradePagination instance from API response."""
        return cls(
            has_next_page=data.get('hasNextPage', False),
            cursor=data.get('cursor'),
            total_count=data.get('totalCount'),
            page_size=data.get('pageSize')
        )

@dataclass
class TradesResponse:
    """Represents the complete response from the trades API."""
    trades: List[Trade]
    pagination: Optional[TradePagination] = None

    @property
    def trade_count(self) -> int:
        """Get the total number of trades in this response."""
        return len(self.trades)

    @property
    def buy_trades(self) -> List[Trade]:
        """Get only buy trades."""
        return [trade for trade in self.trades if trade.is_buy]

    @property
    def sell_trades(self) -> List[Trade]:
        """Get only sell trades."""
        return [trade for trade in self.trades if trade.is_sell]

    @property
    def total_volume_usd(self) -> Decimal:
        """Calculate total volume in USD."""
        return sum(trade.amount_usd for trade in self.trades)

    @property
    def total_volume_sol(self) -> Decimal:
        """Calculate total volume in SOL."""
        return sum(trade.amount_sol for trade in self.trades)

    @property
    def buy_volume_usd(self) -> Decimal:
        """Calculate buy volume in USD."""
        return sum(trade.amount_usd for trade in self.buy_trades)

    @property
    def sell_volume_usd(self) -> Decimal:
        """Calculate sell volume in USD."""
        return sum(trade.amount_usd for trade in self.sell_trades)

    @property
    def average_trade_size_usd(self) -> Decimal:
        """Calculate average trade size in USD."""
        if self.trade_count == 0:
            return Decimal('0')
        return self.total_volume_usd / self.trade_count

    @property
    def unique_traders(self) -> set:
        """Get set of unique trader addresses."""
        return {trade.user_address for trade in self.trades}

    @property
    def unique_trader_count(self) -> int:
        """Get count of unique traders."""
        return len(self.unique_traders)

    @property
    def buy_sell_ratio(self) -> float:
        """Calculate buy to sell trade ratio."""
        sell_count = len(self.sell_trades)
        if sell_count == 0:
            return float('inf') if len(self.buy_trades) > 0 else 0.0
        return len(self.buy_trades) / sell_count

    def get_trades_by_program(self, program: TradingProgram) -> List[Trade]:
        """Get trades filtered by trading program."""
        return [trade for trade in self.trades if trade.program == program]

    def get_trades_by_user(self, user_address: str) -> List[Trade]:
        """Get trades filtered by user address."""
        return [trade for trade in self.trades if trade.user_address == user_address]

    def get_trades_in_time_range(self, start_time: datetime, end_time: datetime) -> List[Trade]:
        """Get trades within a specific time range."""
        return [trade for trade in self.trades 
                if start_time <= trade.timestamp_datetime <= end_time]

    def get_large_trades(self, min_usd_amount: float) -> List[Trade]:
        """Get trades above a certain USD amount."""
        min_amount = Decimal(str(min_usd_amount))
        return [trade for trade in self.trades if trade.amount_usd >= min_amount]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TradesResponse':
        """Create TradesResponse instance from API response."""
        trades_data = data.get('trades', [])
        trades = [Trade.from_dict(trade) for trade in trades_data]
        
        pagination_data = data.get('pagination')
        pagination = TradePagination.from_dict(pagination_data) if pagination_data else None
        
        return cls(trades=trades, pagination=pagination)

    def to_dict(self) -> Dict[str, Any]:
        """Convert TradesResponse to dictionary."""
        result = {
            'trades': [trade.to_dict() for trade in self.trades]
        }
        if self.pagination:
            result['pagination'] = {
                'hasNextPage': self.pagination.has_next_page,
                'cursor': self.pagination.cursor,
                'totalCount': self.pagination.total_count,
                'pageSize': self.pagination.page_size
            }
        return result

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
class GraduatedTokenHolder:
    """Represents a holder of a graduated token."""
    total_token_amount_held: float
    is_sniper: bool
    owned_percentage: float
    holder_id: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GraduatedTokenHolder':
        """Create GraduatedTokenHolder instance from dictionary."""
        return cls(
            total_token_amount_held=data.get('totalTokenAmountHeld', 0.0),
            is_sniper=data.get('isSniper', False),
            owned_percentage=data.get('ownedPercentage', 0.0),
            holder_id=data.get('holderId', '')
        )

@dataclass
class GraduatedToken:
    """Represents a graduated PumpFun token with comprehensive data."""
    coin_mint: str
    dev: str
    name: str
    ticker: str
    image_url: Optional[str] = None
    creation_time: Optional[int] = None
    num_holders: int = 0
    market_cap: float = 0.0
    volume: float = 0.0
    current_market_price: float = 0.0
    bonding_curve_progress: int = 0
    sniper_count: int = 0
    graduation_date: Optional[int] = None
    holders: List[GraduatedTokenHolder] = None
    all_time_high_market_cap: Optional[float] = None
    pool_address: Optional[str] = None
    twitter: Optional[str] = None
    telegram: Optional[str] = None
    website: Optional[str] = None
    has_twitter: bool = False
    has_telegram: bool = False
    has_website: bool = False
    has_social: bool = False
    twitter_reuse_count: int = 0
    dev_holdings_percentage: float = 0.0
    buy_transactions: int = 0
    sell_transactions: int = 0
    transactions: int = 0
    sniper_owned_percentage: float = 0.0
    top_holders_percentage: float = 0.0

    def __post_init__(self):
        """Initialize default values after creation."""
        if self.holders is None:
            self.holders = []

    @property
    def creation_datetime(self) -> Optional[datetime]:
        """Convert creation timestamp to datetime object."""
        if self.creation_time:
            return datetime.fromtimestamp(self.creation_time / 1000)
        return None

    @property
    def graduation_datetime(self) -> Optional[datetime]:
        """Convert graduation timestamp to datetime object."""
        if self.graduation_date:
            return datetime.fromtimestamp(self.graduation_date / 1000)
        return None

    @property
    def is_fully_graduated(self) -> bool:
        """Check if token has fully graduated (bonding curve progress = 100)."""
        return self.bonding_curve_progress >= 100

    @property
    def total_transactions(self) -> int:
        """Get total number of transactions."""
        return self.buy_transactions + self.sell_transactions

    @property
    def buy_sell_ratio(self) -> float:
        """Calculate buy to sell transaction ratio."""
        if self.sell_transactions == 0:
            return float('inf') if self.buy_transactions > 0 else 0.0
        return self.buy_transactions / self.sell_transactions

    @property
    def graduation_time_hours(self) -> Optional[float]:
        """Calculate hours from creation to graduation."""
        if self.creation_time and self.graduation_date:
            diff_ms = self.graduation_date - self.creation_time
            return diff_ms / (1000 * 60 * 60)  # Convert to hours
        return None

    @property
    def market_cap_growth(self) -> Optional[float]:
        """Calculate market cap growth percentage."""
        if self.all_time_high_market_cap and self.market_cap > 0:
            return ((self.all_time_high_market_cap - self.market_cap) / self.market_cap) * 100
        return None

    @property
    def top_10_holders(self) -> List[GraduatedTokenHolder]:
        """Get top 10 holders by token amount."""
        return sorted(self.holders, key=lambda h: h.total_token_amount_held, reverse=True)[:10]

    @property
    def sniper_holders(self) -> List[GraduatedTokenHolder]:
        """Get all holders marked as snipers."""
        return [holder for holder in self.holders if holder.is_sniper]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GraduatedToken':
        """Create GraduatedToken instance from API response."""
        holders_data = data.get('holders', [])
        holders = [GraduatedTokenHolder.from_dict(holder) for holder in holders_data]
        
        return cls(
            coin_mint=data.get('coinMint', ''),
            dev=data.get('dev', ''),
            name=data.get('name', ''),
            ticker=data.get('ticker', ''),
            image_url=data.get('imageUrl'),
            creation_time=data.get('creationTime'),
            num_holders=data.get('numHolders', 0),
            market_cap=data.get('marketCap', 0.0),
            volume=data.get('volume', 0.0),
            current_market_price=data.get('currentMarketPrice', 0.0),
            bonding_curve_progress=data.get('bondingCurveProgress', 0),
            sniper_count=data.get('sniperCount', 0),
            graduation_date=data.get('graduationDate'),
            holders=holders,
            all_time_high_market_cap=data.get('allTimeHighMarketCap'),
            pool_address=data.get('poolAddress'),
            twitter=data.get('twitter'),
            telegram=data.get('telegram'),
            website=data.get('website'),
            has_twitter=data.get('hasTwitter', False),
            has_telegram=data.get('hasTelegram', False),
            has_website=data.get('hasWebsite', False),
            has_social=data.get('hasSocial', False),
            twitter_reuse_count=data.get('twitterReuseCount', 0),
            dev_holdings_percentage=data.get('devHoldingsPercentage', 0.0),
            buy_transactions=data.get('buyTransactions', 0),
            sell_transactions=data.get('sellTransactions', 0),
            transactions=data.get('transactions', 0),
            sniper_owned_percentage=data.get('sniperOwnedPercentage', 0.0),
            top_holders_percentage=data.get('topHoldersPercentage', 0.0)
        )

@dataclass
class GraduatedTokensResponse:
    """Represents the response from the graduated tokens API."""
    coins: List[GraduatedToken]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GraduatedTokensResponse':
        """Create GraduatedTokensResponse instance from API response."""
        coins_data = data.get('coins', [])
        coins = [GraduatedToken.from_dict(coin) for coin in coins_data]
        return cls(coins=coins)

    @property
    def token_count(self) -> int:
        """Get the total number of graduated tokens."""
        return len(self.coins)

    @property
    def total_market_cap(self) -> float:
        """Calculate total market cap of all graduated tokens."""
        return sum(coin.market_cap for coin in self.coins)

    @property
    def average_market_cap(self) -> float:
        """Calculate average market cap of graduated tokens."""
        if self.token_count == 0:
            return 0.0
        return self.total_market_cap / self.token_count

    @property
    def tokens_with_social(self) -> List[GraduatedToken]:
        """Get tokens that have social media presence."""
        return [coin for coin in self.coins if coin.has_social]

    def get_high_volume_tokens(self, min_volume: float = 1000.0) -> List[GraduatedToken]:
        """Get tokens with high trading volume."""
        return [coin for coin in self.coins if coin.volume >= min_volume]

    def get_tokens_by_market_cap_range(self, min_cap: float, max_cap: float) -> List[GraduatedToken]:
        """Get tokens within a specific market cap range."""
        return [coin for coin in self.coins if min_cap <= coin.market_cap <= max_cap]

    def get_top_tokens_by_market_cap(self, limit: int = 10) -> List[GraduatedToken]:
        """Get top tokens by market cap."""
        return sorted(self.coins, key=lambda coin: coin.market_cap, reverse=True)[:limit]

    def get_tokens_by_graduation_time(self, max_hours: float) -> List[GraduatedToken]:
        """Get tokens that graduated within specified hours."""
        return [coin for coin in self.coins 
                if coin.graduation_time_hours is not None and coin.graduation_time_hours <= max_hours]

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