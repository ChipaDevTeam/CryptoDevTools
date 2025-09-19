from CryptoDevTools.solana import SolanaDataClient
from CryptoDevTools.models.solana.token_data import TradesResponse

def main():
    solana_client = SolanaDataClient()
    response_data = solana_client.getTrades("HxmUkRirJuvoF8dEt74UyXUK7NAs6xtByxHLcSBipump", limit=5)
    
    print(f"Trades: {response_data.trades}")

if __name__ == "__main__":
    main()