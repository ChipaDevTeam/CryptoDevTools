from CryptoDevTools.solana import SolanaDataClient
from CryptoDevTools.models.solana.token_data import TradesResponse

def main():
    solana_client = SolanaDataClient()
    response_data = solana_client.getTrades("HxmUkRirJuvoF8dEt74UyXUK7NAs6xtByxHLcSBipump", limit=100)
    data = TradesResponse.from_dict(response_data.__dict__)
    
    print(f"Trades: {data.trades.trade_type}")

if __name__ == "__main__":
    main()