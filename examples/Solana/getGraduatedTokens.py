from CryptoDevTools.solana import SolanaDataClient
import json

def main():
    data_client = SolanaDataClient()

    # Get graduated tokens from PumpFun
    graduated_response = data_client.getGraduatedTokens()
    
    print(f"Total graduated tokens: {graduated_response.token_count}")
    print(f"Total market cap: ${graduated_response.total_market_cap:,.2f}")
    print(f"Average market cap: ${graduated_response.average_market_cap:,.2f}")
    
    # Show top 3 tokens
    top_tokens = graduated_response.get_top_tokens_by_market_cap(3)
    print("\nTop 3 tokens by market cap:")
    
    for i, token in enumerate(top_tokens, 1):
        print(f"\n{i}. {token.name} ({token.ticker})")
        print(f"   Market Cap: ${token.market_cap:,.2f}")
        print(f"   Holders: {token.num_holders}")
        print(f"   Created: {token.creation_datetime}")
        print(f"   Time to Graduate: {token.graduation_time_hours:.2f} hours" if token.graduation_time_hours else "N/A")

    

if __name__ == "__main__":
    main()