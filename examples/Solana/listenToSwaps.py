import logging
import asyncio
import json
import os
import sys

# Configure logging at the script level to ensure we see INFO/DEBUG logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add project root to sys.path to ensure imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from CryptoDevTools.solana import SolanaSwapListener

async def main():
    # Helper constants
    # You should use a paid RPC for better reliability, especially for logsSubscribe
    RPC_URL = "https://greer-651y13-fast-mainnet.helius-rpc.com"
    WSS_URL = "wss://greer-651y13-fast-mainnet.helius-rpc.com"
    
    # Replace with the Token Mint Address you want to monitor
    # Example: POPCAT
    TOKEN_MINT = "8g1SENegf6vsKagGgvEBxZEsLrGooesdNnE3wsJvByft" 

    print(f"Initializing listener for {TOKEN_MINT}...")
    listener = SolanaSwapListener(RPC_URL, WSS_URL)

    async def on_swap(data):
        print(f"\n--- Swap Detected ---")
        print(json.dumps(data, indent=2))
        print("---------------------")

    print(f"Listening for swaps... Press Ctrl+C to stop.")
    try:
        await listener.start(TOKEN_MINT, on_swap)
    except KeyboardInterrupt:
        print("Stopping listener...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
