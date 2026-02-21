

class DefaultData:
    DEFAULT_SOLANA_RPC = "https://api.mainnet-beta.solana.com"
    DEFAULT_ETHEREUM_RPC = "https://eth.llamarpc.com"
    HELIUS_RPC = "https://greer-651y13-fast-mainnet.helius-rpc.com/"

class GlobalConstants:
    HELIUS_RPC = DefaultData.HELIUS_RPC
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    HEADERS = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    EXCHANGES = ["PumpFun", "Raydium", "Orca", "Jupiter"]  # List of supported exchanges for new token data
    SORT_BY_OPTIONS = ["creationTime", "marketCap", "volume24h"]  # Options for sorting graduated tokens
    GRADUATED_DEFAULT_SORT = "creationTime"

class DexPrograms:
    RAYDIUM_V4_PROGRAM_ID = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
    PUMP_FUN_PROGRAM_ID = "6EF8rrecthR5DkdfxkqCnDWWFkkKCk2dNRwCpwdRLuqt"
    RAYDIUM_AMM_V4 = "675kPXaZJ9UQCj3D9V6G3z1P7XpYj7945A8K5M42S28L"
    RAYDIUM_CLMM = "CAMMCzo5YLgUDd1G51k5VfC1r4N2z977u4T4q5v51717"
    RAYDIUM_CONCENTRATED_LIQUIDITY = "whirVjicr14JgS2fS2C3C91W6671A6y4qS3k45U6f2f"
    ORCA_WHIRLPOOLS = "whirVjicr14JgS2fS2C3C91W6671A6y4qS3k45U6f2f"
    ORCA_TOKEN_SWAP_V2 = "9W959DqjETzGZJ5C2Q3C91W6671A6y4qS3k45U6f2f"
    METEORA_DLMM = "LBUZKhsJWnrJvPz36k3zT9Fq5s17596p9v7a8S9r3a7"
    JUPITER_AGGREGATOR_V6 = "JUP6LKBh1qy2t34V462D6y4qS3k45U6f2f"
    SERUM_LEGACY = "9xQeWvG816bUx94zG3z1P7XpYj7945A8K5M42S28L"
    