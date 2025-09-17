# 🚀 CryptoDevTools

A comprehensive Python toolkit for blockchain developers, providing easy-to-use APIs and tools for interacting with multiple blockchain networks and analyzing cryptocurrency data.

## 🌟 Features

### 🔗 Multi-Blockchain Support
- **Solana**: Complete RPC client, trading tools, and token analysis
- **Ethereum**: EVM-compatible interactions
- **BNB Chain**: Binance Smart Chain integration
- **Tronix**: TRON blockchain support

### 📊 Advanced Token Analytics
- **PumpFun Integration**: Real-time token data, graduated tokens, and holder analysis
- **Token Metadata**: Comprehensive token information retrieval
- **Market Analysis**: Price tracking, volume analysis, and market cap calculations
- **Holder Analytics**: Top holders, sniper detection, and distribution analysis

### 🎯 Solana Ecosystem Tools
- **RPC Client**: Full Solana RPC API coverage with 50+ methods
- **Trading Client**: Multi-DEX trading support (Raydium, Serum, Orca, Mango, Jupiter, Aldrin, Drift)
- **Data Client**: Token data aggregation and analysis
- **Stream Client**: Real-time data streaming

## 📦 Installation

```bash
git clone https://github.com/ChipaDevTeam/CryptoDevTools.git
cd CryptoDevTools
pip install -r requirements.txt
```

## 🚀 Quick Start

### Basic Solana Client Usage

```python
from CryptoDevTools.solana import SolanaClient

# Initialize client
rpc_url = "https://api.mainnet-beta.solana.com"
client = SolanaClient(rpc_url)

# Get account information
account = "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh"
account_info = client.getAccountInfo(account)
balance = client.getBalance(account)

print(f"Account Info: {account_info}")
print(f"Balance: {balance['value'] / 1e9} SOL")
```

### Token Data Analysis

```python
from CryptoDevTools.solana import SolanaDataClient

# Initialize data client
data_client = SolanaDataClient()

# Get token metadata
token_address = "F9Lw3ki3hJ7PF9HQXsBzoY8GyE6sPoEZZdXJBsTTD2rk"
metadata = data_client.getTokenMetadata(token_address)
print(f"Token: {metadata.content['metadata']['name']}")

# Get token holders
holders_data = data_client.getHoldersTokens(token_address)
print(f"Total Holders: {holders_data.total_holders}")
```

### PumpFun Token Analysis

```python
from CryptoDevTools.solana import SolanaDataClient

data_client = SolanaDataClient()

# Get new tokens from PumpFun
new_tokens = data_client.getNewTokensByExchange("PumpFun")
print(f"Found {len(new_tokens)} new PumpFun tokens")

for token in new_tokens[:3]:
    print(f"Name: {token.coin.name}")
    print(f"Symbol: {token.coin.symbol}")
    print(f"Market Cap: ${token.coin.usd_market_cap:,.2f}")
    print(f"Currently Live: {token.coin.is_currently_live}")
    print("---")
```

### Graduated Tokens Analytics

```python
# Get graduated tokens with advanced analytics
graduated_response = data_client.getGraduatedTokens()

print(f"Total graduated tokens: {graduated_response.token_count}")
print(f"Total market cap: ${graduated_response.total_market_cap:,.2f}")
print(f"Average market cap: ${graduated_response.average_market_cap:,.2f}")

# Get top performers
top_tokens = graduated_response.get_top_tokens_by_market_cap(5)
for i, token in enumerate(top_tokens, 1):
    print(f"{i}. {token.name} ({token.ticker})")
    print(f"   Market Cap: ${token.market_cap:,.2f}")
    print(f"   Holders: {token.num_holders}")
    print(f"   Time to Graduate: {token.graduation_time_hours:.2f} hours")
    print(f"   Buy/Sell Ratio: {token.buy_sell_ratio:.2f}")
```

### Trading Operations

```python
from CryptoDevTools.solana import SolanaTradeClient

# Initialize trading client
rpc_url = "https://api.mainnet-beta.solana.com"
trade_client = SolanaTradeClient(rpc_url)

# Example order (implementation varies by DEX)
order_details = {
    "token_in": "SOL",
    "token_out": "USDC",
    "amount": 1.0,
    "slippage": 0.5
}

# Place order on Raydium
result = trade_client.PlaceOrderRaydium(order_details)
```

## 🏗️ Architecture

### Core Components

```
CryptoDevTools/
├── solana/                 # Solana ecosystem tools
│   ├── _SolanaClient.py   # RPC client (50+ methods)
│   ├── _DataClient.py     # Token data aggregation
│   ├── _TradeClient.py    # Multi-DEX trading
│   ├── _StreamClient.py   # Real-time data streaming
│   └── DataAPI/           # Data sources and APIs
├── ethereum/              # Ethereum tools
├── bnb/                   # BNB Chain tools
├── tronix/                # TRON tools
├── models/                # Data models and structures
└── constants.py           # Configuration and constants
```

### Solana RPC Methods (50+ Supported)

**Account & Balance Operations:**
- `getAccountInfo()`, `getBalance()`, `getMultipleAccounts()`
- `getProgramAccounts()`, `getLargestAccounts()`

**Block & Transaction Operations:**
- `getBlock()`, `getBlockHeight()`, `getBlockCommitment()`
- `getTransaction()`, `getConfirmedTransaction()`
- `getSignatureStatuses()`, `getTransactionCount()`

**Network & Cluster Operations:**
- `getClusterNodes()`, `getEpochInfo()`, `getHealth()`
- `getVersion()`, `getGenesisHash()`, `getIdentity()`

**Advanced Operations:**
- `simulateTransaction()`, `sendTransaction()`
- `getRecentPerformanceSamples()`, `getInflationRate()`
- `getSlot()`, `getSlotLeaders()`, `getSupply()`

## 📊 Advanced Analytics Features

### Token Metrics
- **Market Analysis**: Real-time prices, volume, market cap tracking
- **Holder Distribution**: Top holders, concentration analysis
- **Trading Patterns**: Buy/sell ratios, transaction volumes
- **Risk Assessment**: Sniper detection, dev holdings analysis

### PumpFun Specific Analytics
- **Graduation Tracking**: Time to graduation, success rates
- **Live Stream Monitoring**: Real-time token launches
- **Community Metrics**: Social media presence, engagement
- **Performance Indicators**: ATH tracking, price movements

### Data Models

**Rich Token Models:**
```python
# PumpFun tokens with full metadata
PumpFunToken(
    coin=PumpFunCoin(mint, name, symbol, market_cap, ...),
    description="Token description",
    modified_by="Creator address"
)

# Graduated tokens with analytics
GraduatedToken(
    coin_mint="...", name="...", ticker="...",
    market_cap=100000, volume=5000,
    graduation_time_hours=2.5,
    buy_sell_ratio=1.25,
    holders=[...], sniper_count=10
)
```

## 🛠️ Supported Trading Platforms

### Solana DEXs
- **Raydium**: AMM and order book trading
- **Serum**: Central limit order book
- **Orca**: Automated market maker
- **Mango Markets**: Margin trading and lending
- **Jupiter**: DEX aggregator
- **Aldrin**: AMM with concentrated liquidity
- **Drift Protocol**: Perpetual futures

## 📖 Documentation & Examples

### Examples Directory
```bash
examples/
├── Solana/
│   ├── getNewTokensByExchange.py    # Fetch new PumpFun tokens
│   └── getGraduatedTokens.py        # Analyze graduated tokens
└── token_model_usage.py             # Advanced model usage
```

### Running Examples
```bash
# Get new PumpFun tokens
python examples/Solana/getNewTokensByExchange.py

# Analyze graduated tokens
python examples/Solana/getGraduatedTokens.py

# Test token models
python examples/token_model_usage.py
```

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Custom RPC endpoints
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
HELIUS_API_KEY=your_helius_api_key_here

# Optional: API rate limiting
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

### Constants Configuration
```python
from CryptoDevTools.constants import GlobalConstants

# Available sort options for graduated tokens
GlobalConstants.SORT_BY_OPTIONS = [
    "marketCap", "volume", "creationTime", 
    "graduationDate", "numHolders"
]

# Supported exchanges
GlobalConstants.EXCHANGES = ["PumpFun"]
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Setup
```bash
# Clone the repository
git clone https://github.com/ChipaDevTeam/CryptoDevTools.git
cd CryptoDevTools

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚨 Disclaimer

This tool is for educational and development purposes. Always verify transactions and use appropriate security measures when dealing with cryptocurrency. The developers are not responsible for any financial losses.

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/ChipaDevTeam/CryptoDevTools/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ChipaDevTeam/CryptoDevTools/discussions)
- **Documentation**: [Wiki](https://github.com/ChipaDevTeam/CryptoDevTools/wiki)

## 🙏 Acknowledgments

- Solana Foundation for the comprehensive RPC API
- PumpFun team for the token launch platform
- The broader crypto development community

---

**⭐ Star this repository if you find it useful!**
