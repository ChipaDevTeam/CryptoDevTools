import logging
import asyncio
import json
import os
import sys
from datetime import datetime

# Configure logging at the script level to ensure we see INFO/DEBUG logs
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add project root to sys.path to ensure imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from CryptoDevTools.solana import SolanaSwapListener

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

async def main():
    # Helper constants
    # You should use a paid RPC for better reliability, especially for logsSubscribe
    RPC_URL = "https://greer-651y13-fast-mainnet.helius-rpc.com"
    WSS_URL = "wss://greer-651y13-fast-mainnet.helius-rpc.com"
    
    # Replace with the Token Mint Address you want to monitor
    # Example: POPCAT
    TOKEN_MINT = input("Enter the Token Mint Address to monitor swaps for: ").strip() or "HxmUkRirJuvoF8dEt74UyXUK7NAs6xtByxHLcSBipump"

    print(f"Initializing listener for {TOKEN_MINT}...")
    listener = SolanaSwapListener(RPC_URL, WSS_URL)

    async def on_swap(data):
        ts = data.get("timestamp", 0)
        dt = datetime.fromtimestamp(ts) if ts else datetime.now()
        time_str = dt.strftime("%H:%M:%S")
        
        swap_type = data.get("type", "unknown")
        signer = data.get("signer", "Unknown")
        short_signer = f"{signer[:3]}...{signer[-3:]}" if len(signer) > 6 else signer
        
        if swap_type == "buy":
            sol_amount = data.get("amount_in", 0.0)
            color = GREEN
            action_str = "(🟢 Buy )"
            icon = "[ ✨ ]"
            amount_str = f"+{sol_amount:.3f} sol"
        else:
            sol_amount = data.get("amount_out", 0.0)
            color = RED
            action_str = "(🔴 Sell)"
            icon = "[  - ]"
            amount_str = f"-{sol_amount:.3f} sol"
            
        # Format: 15:00:00 | [ ✨ ] (🟢 Buy ) | 46b...iY7 | Amount: +0.102 sol
        formatted_msg = f"{color}{time_str} | {icon} {action_str} | {short_signer} | Amount: {amount_str}{RESET}"
        print(formatted_msg)

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
