"""
Test script to demonstrate graduated tokens model usage.
"""

import json
from CryptoDevTools.models.solana.token_data import GraduatedTokensResponse, GraduatedToken

def test_graduated_tokens_model():
    """Test the graduated tokens model with sample data."""
    
    # Load sample data
    with open('tests/sample-output-pumpfun-graduated.json', 'r') as f:
        sample_data = json.load(f)
    
    # Create graduated tokens response object
    graduated_response = GraduatedTokensResponse.from_dict(sample_data)
    
    print(f"Total graduated tokens: {graduated_response.token_count}")
    print(f"Total market cap: ${graduated_response.total_market_cap:,.2f}")
    print(f"Average market cap: ${graduated_response.average_market_cap:,.2f}")
    print(f"Tokens with social: {len(graduated_response.tokens_with_social)}")
    
    # Get top 3 tokens by market cap
    top_tokens = graduated_response.get_top_tokens_by_market_cap(3)
    
    print("\n=== Top 3 Tokens by Market Cap ===")
    for i, token in enumerate(top_tokens, 1):
        print(f"\n--- Token {i} ---")
        print(f"Name: {token.name}")
        print(f"Ticker: {token.ticker}")
        print(f"Market Cap: ${token.market_cap:,.2f}")
        print(f"All-Time High: ${token.all_time_high_market_cap:,.2f}")
        print(f"Holders: {token.num_holders}")
        print(f"Volume: ${token.volume:,.2f}")
        print(f"Created: {token.creation_datetime}")
        print(f"Graduated: {token.graduation_datetime}")
        print(f"Time to Graduate: {token.graduation_time_hours:.2f} hours" if token.graduation_time_hours else "N/A")
        print(f"Buy/Sell Ratio: {token.buy_sell_ratio:.2f}")
        print(f"Has Social: {token.has_social}")
        print(f"Sniper Count: {token.sniper_count}")
        print(f"Dev Holdings: {token.dev_holdings_percentage:.4f}%")
        print(f"Top Holders %: {token.top_holders_percentage:.2f}%")
        
        # Show top 3 holders
        print(f"Top 3 Holders:")
        for j, holder in enumerate(token.top_10_holders[:3], 1):
            print(f"  {j}. {holder.holder_id[:8]}... - {holder.owned_percentage:.2f}% - Sniper: {holder.is_sniper}")
    
    # Get fast graduating tokens (within 1 hour)
    fast_tokens = graduated_response.get_tokens_by_graduation_time(1.0)
    print(f"\n=== Fast Graduating Tokens (< 1 hour) ===")
    print(f"Found {len(fast_tokens)} tokens that graduated in less than 1 hour")
    
    # Get high volume tokens
    high_volume = graduated_response.get_high_volume_tokens(1000.0)
    print(f"\n=== High Volume Tokens (> $1000) ===")
    print(f"Found {len(high_volume)} tokens with volume > $1000")
    
    return graduated_response

if __name__ == "__main__":
    response = test_graduated_tokens_model()
