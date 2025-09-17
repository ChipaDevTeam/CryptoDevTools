from CryptoDevTools.solana import SolanaDataClient
import json

def main():
    data_client = SolanaDataClient()

    # Get new tokens from PumpFun exchange
    tokens = data_client.getNewTokensByExchange("PumpFun")

    print(f"Retrieved {len(tokens)} tokens from PumpFun")
    print("\nFirst 3 tokens:")
    
    for i, token in enumerate(tokens[:3]):
        print(f"\n--- Token {i+1} ---")
        print(f"Name: {token.coin.name}")
        print(f"Symbol: {token.coin.symbol}")
        print(f"Mint: {token.coin.mint}")
        print(f"Market Cap: ${token.coin.usd_market_cap:,.2f}")
        print(f"Created: {token.coin.created_datetime}")
        print(f"Description: {token.description}")
        print(f"Currently Live: {token.coin.is_currently_live}")

if __name__ == "__main__":
    main()