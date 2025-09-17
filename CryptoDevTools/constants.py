

class DefaultData:
    DEFAULT_SOLANA_RPC = "https://api.mainnet-beta.solana.com"
    DEFAULT_ETHEREUM_RPC = "https://eth.llamarpc.com"
    HELIUS_RPC = "https://greer-651y13-fast-mainnet.helius-rpc.com/"

class GlobalConstants:
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    HEADERS = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    EXCHANGES = ["PumpFun", "Raydium", "Orca", "Jupiter"]  # List of supported exchanges for new token data
    SORT_BY_OPTIONS = ["creationTime", "marketCap", "volume24h"]  # Options for sorting graduated tokens
    GRADUATED_DEFAULT_SORT = "creationTime"