import asyncio
import json
import websockets
import aiohttp
from typing import Dict, Optional, Callable

# Constants for DEX Programs
RAYDIUM_V4_PROGRAM_ID = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
PUMP_FUN_PROGRAM_ID = "6EF8rrecthR5DkdfxkqCnDWWFkkKCk2dNRwCpwdRLuqt"

class SolanaSwapListener:
    def __init__(self, rpc_url: str, ws_url: str):
        self.rpc_url = rpc_url
        self.ws_url = ws_url
        self.session = None

    async def start(self, token_mint: str, callback: Callable[[Dict], None]):
        """
        Starts listening for swap events for a specific token mint.
        
        Args:
            token_mint (str): The Token Mint Address to listen for.
            callback (Callable): A function to call with the parsed swap data.
        """
        self.session = aiohttp.ClientSession()
        try:
            async with websockets.connect(self.ws_url) as websocket:
                # Subscribe to logs mentioning the token mint
                payload = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "logsSubscribe",
                    "params": [
                        {"mentions": [token_mint]},
                        {"commitment": "confirmed"}
                    ]
                }
                await websocket.send(json.dumps(payload))
                response = await websocket.recv()
                print(f"Subscription response: {response}")

                async for message in websocket:
                    data = json.loads(message)
                    if "params" in data:
                        # Process the notification
                        logs = data["params"]["result"]["value"].get("logs", [])
                        signature = data["params"]["result"]["value"]["signature"]
                        
                        # Fetch full transaction details to parse swap
                        tx_details = await self.get_transaction_details(signature)
                        if tx_details:
                            swap_data = self.parse_swap(tx_details, token_mint)
                            if swap_data:
                                if asyncio.iscoroutinefunction(callback):
                                    await callback(swap_data)
                                else:
                                    callback(swap_data)
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            if self.session:
                await self.session.close()

    async def get_transaction_details(self, signature: str) -> Optional[Dict]:
        """Fetches full transaction details using RPC."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [
                signature,
                {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}
            ]
        }
        
        try:
            async with self.session.post(self.rpc_url, json=payload) as response:
                result = await response.json()
                return result.get("result")
        except Exception as e:
            print(f"Error fetching transaction {signature}: {e}")
            return None

    def parse_swap(self, tx_data: Dict, token_mint: str) -> Optional[Dict]:
        """
        Parses transaction data to extract swap details.
        Returns None if not a swap or irrelevant.
        """
        if not tx_data:
            return None
            
        meta = tx_data.get("meta")
        if not meta or meta.get("err"):
            return None

        # 1. Identify the Signer (User) - typically the first account
        transaction = tx_data.get("transaction")
        account_keys = transaction.get("message", {}).get("accountKeys", [])
        
        # Handle different transaction versions (legacy vs v0)
        signer = None
        if isinstance(account_keys, list):
            # Legacy: accountKeys is a list of objects or strings
            if isinstance(account_keys[0], dict):
                signer = account_keys[0].get("pubkey")
            else:
                signer = account_keys[0] # parsed format
        
        # 2. Check Token Balance Changes (Pre vs Post)
        pre_token_balances = meta.get("preTokenBalances", [])
        post_token_balances = meta.get("postTokenBalances", [])

        # Find the balance change for the specific token mint
        token_change = 0
        signer_token_index = -1
        
        # Helper to find balance for an account index and mint
        def get_balance(balances, mint, owner):
            for b in balances:
                if b.get("mint") == mint and b.get("owner") == owner:
                    return float(b.get("uiTokenAmount", {}).get("uiAmount") or 0)
            return 0

        pre_bal = get_balance(pre_token_balances, token_mint, signer)
        post_bal = get_balance(post_token_balances, token_mint, signer)
        token_change = post_bal - pre_bal

        if token_change == 0:
            return None # No change in target token balance for signer

        # 3. Check SOL Balance Changes (for Buy/Sell determination)
        # Using preBalances and postBalances from meta (lamports)
        pre_sol_balances = meta.get("preBalances", [])
        post_sol_balances = meta.get("postBalances", [])
        
        # Signer is always index 0
        sol_change_lamports = post_sol_balances[0] - pre_sol_balances[0]
        sol_change = sol_change_lamports / 1e9

        # 4. Determine Swap Direction and Amounts
        # Heuristic: 
        # Buy: SOL decreases, Token increases
        # Sell: Token decreases, SOL increases
        
        swap_type = "unknown"
        amount_in = 0
        amount_out = 0
        input_token = ""
        output_token = ""

        if token_change > 0:
            swap_type = "buy"
            amount_out = token_change
            output_token = token_mint
            # Assuming input was SOL/WSOL (simplified)
            amount_in = abs(sol_change) 
            input_token = "SOL" 
        else:
            swap_type = "sell"
            amount_in = abs(token_change)
            input_token = token_mint
            amount_out = sol_change # Includes fees, so might be approximate
            output_token = "SOL"

        # 5. Identify DEX (Optional - from logs)
        dex = "unknown"
        logs = meta.get("logMessages", [])
        log_str = " ".join(logs)
        if RAYDIUM_V4_PROGRAM_ID in log_str:
            dex = "raydium"
        elif PUMP_FUN_PROGRAM_ID in log_str:
            dex = "pumpfun"

        return {
            "signature": transaction.get("signatures", [""])[0],
            "signer": signer,
            "type": swap_type,
            "amount_in": amount_in,
            "input_token": input_token,
            "amount_out": amount_out,
            "output_token": output_token,
            "dex": dex,
            "timestamp": tx_data.get("blockTime")
        }

# Example Usage
if __name__ == "__main__":
    async def main():
        # Replace with your RPC/WSS endpoints
        RPC_URL = "https://api.mainnet-beta.solana.com" 
        WS_URL = "wss://api.mainnet-beta.solana.com"
        
        # Example: USDC Mint
        TOKEN_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v" 

        listener = SolanaSwapListener(RPC_URL, WS_URL)
        
        async def print_swap(data):
            print(f"Swap Detected: {json.dumps(data, indent=2)}")

        print(f"Listening for swaps on {TOKEN_MINT}...")
        await listener.start(TOKEN_MINT, print_swap)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped.")
