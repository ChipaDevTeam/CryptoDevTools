"""
Example usage of the improved token models.
"""

import json
from CryptoDevTools.models.solana.token_data import (
    PumpFunToken, 
    SolanaToken,
    TokenPrice,
    ExchangeInfo
)
from decimal import Decimal
from datetime import datetime

def example_pumpfun_integration():
    """Example of how to use the models with PumpFun data."""
    
    # Sample PumpFun API response (like what you got in your test)
    sample_response = {
        "coin": {
            "mint": "4CBToKTRKfBsv8RMfzMr6VfKQ8PLRYeG6RFGZmq4pump",
            "name": "101 Year Old Pumpfun Livestreamr",
            "symbol": "grandma",
            "description": "Oldest Lady in the entire world to stream on Pump.fun Making history",
            "image_uri": "https://ipfs.io/ipfs/bafybeiffvalpqlekg6kutkh4rrci4zkvr7jt4negeklq5no633tbbqmjam",
            "metadata_uri": "https://ipfs.io/ipfs/bafkreidtq3b7vbdiyciymsty3ere3rsnmyr3dyy4tgq6gjgvyq3hodm5xq",
            "twitter": None,
            "telegram": None,
            "website": "https://thenewamericansmag.com/2024/11/08/columbus-resident-thelma-mae-scott-marks-101-years-old/",
            "market_cap": 2854.596384978938,
            "usd_market_cap": 672057.6269155914,
            "created_timestamp": 1758033239691,
            "total_supply": 1000000000000000,
            "complete": True
        },
        "description": "101-Year-Old Grandma Outplays Trenches Live on Stream",
        "modifiedBy": "FmoMPpn9LjpY8MiigHhFZgm79RE1ynj2tsipz3a96icb"
    }
    
    # Create PumpFun token model
    pumpfun_token = PumpFunToken.from_dict(sample_response)
    print("PumpFun Token Created:")
    print(f"Name: {pumpfun_token.coin.name}")
    print(f"Symbol: {pumpfun_token.coin.symbol}")
    print(f"Market Cap: ${pumpfun_token.coin.usd_market_cap:,.2f}")
    print(f"Created: {pumpfun_token.coin.created_datetime}")
    
    # Create comprehensive Solana token from PumpFun data
    solana_token = SolanaToken.from_pumpfun_data(pumpfun_token)
    
    # Add additional exchange info
    raydium_info = ExchangeInfo(
        exchange_name="Raydium",
        pair="GRANDMA/SOL",
        price=Decimal("0.000672"),
        volume_24h=Decimal("50000")
    )
    solana_token.add_exchange_info(raydium_info)
    
    print(f"\nComprehensive Token Model:")
    print(f"Is PumpFun token: {solana_token.is_pumpfun_token}")
    print(f"Market Cap: ${solana_token.market_cap_usd}")
    print(f"Exchanges: {len(solana_token.exchanges)}")
    
    return solana_token

if __name__ == "__main__":
    token = example_pumpfun_integration()
    
    # Convert to dict for JSON serialization
    token_dict = token.to_dict()
    print(f"\nSerialized token keys: {list(token_dict.keys())}")
