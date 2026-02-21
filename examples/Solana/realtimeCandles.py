import logging
import asyncio
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
from CryptoDevTools.solana.helpers.CandleAggregator import CandleAggregator

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

async def main():
    # Helper constants
    RPC_URL = "https://greer-651y13-fast-mainnet.helius-rpc.com"
    WSS_URL = "wss://greer-651y13-fast-mainnet.helius-rpc.com"
    
    # Replace with the Token Mint Address you want to monitor
    TOKEN_MINT = "4du67Lp42navoc7zvh42689yz1CRjzWycjp1qsRDpump" 

    print(f"{CYAN}Initializing Real-Time On-Chain Candle Aggregator for {TOKEN_MINT}...{RESET}")
    listener = SolanaSwapListener(RPC_URL, WSS_URL)

    def on_candle_close(candle):
        """
        Callback triggered when a candle timeframe closes.
        """
        dt = datetime.fromtimestamp(candle['start_time'])
        time_str = dt.strftime("%H:%M:%S")
        
        o = candle['open']
        h = candle['high']
        l = candle['low']
        c = candle['close']
        vol = candle['sol_volume']
        trades = candle['trades']
        
        color = GREEN if c >= o else RED
        icon = "📈" if c >= o else "📉"
        
        print(f"{color}{time_str} | {icon} CANDLE | O: {o:.8f} | H: {h:.8f} | L: {l:.8f} | C: {c:.8f} | Vol: {vol:.2f} SOL | Trades: {trades}{RESET}")

    # Create an aggregator for 10-second candles (adjust timeframe_seconds as needed)
    aggregator = CandleAggregator(timeframe_seconds=10, on_candle_close=on_candle_close)

    async def on_swap(data):
        """
        Callback triggered on every individual swap.
        """
        # 1. Print the individual swap (faintly)
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

        # 2. Pass the swap to the aggregator to build candles
        aggregator.process_swap(data)

    print(f"Listening for swaps and building candles... Press Ctrl+C to stop.")
    try:
        await listener.start(TOKEN_MINT, on_swap)
    except KeyboardInterrupt:
        print("Stopping listener...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
