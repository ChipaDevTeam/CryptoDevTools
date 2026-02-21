import asyncio
import json
import os
import sys

# Add project root to sys.path to ensure imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from CryptoDevTools.solana import SolanaSwapListener

async def main():
    # Helper constants
    # You should use a paid RPC for better reliability, especially for logsSubscribe
    RPC_URL = "https://hardworking-magical-replica.arbitrum-mainnet.quiknode.pro"
    WSS_URL = "wss://hardworking-magical-replica.arbitrum-mainnet.quiknode.pro"
    
    # Replace with the Token Mint Address you want to monitor
    # Example: POPCAT
    TOKEN_MINT = "6sUrXQq46D9VeMpb2tJAEVyw5QEGCCZ2gRftq49TdMJy" 

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
