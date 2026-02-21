import asyncio
import json
import logging
import websockets
import aiohttp
from typing import Dict, Optional, Callable, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for DEX Programs
RAYDIUM_V4_PROGRAM_ID = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
PUMP_FUN_PROGRAM_ID = "6EF8rrecthR5DkdfxkqCnDWWFkkKCk2dNRwCpwdRLuqt"

class SolanaSwapListener:
    def __init__(self, rpc_url: str, ws_url: str):
        self.rpc_url = rpc_url
        self.ws_url = ws_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def start(self, token_mint: str, callback: Callable[[Dict[str, Any]], Any]):
        """
        Starts listening for swap events for a specific token mint.
        
        Args:
            token_mint (str): The Token Mint Address to listen for.
            callback (Callable): A function to call with the parsed swap data.
        """
        self.session = aiohttp.ClientSession()
        try:
            logger.info(f"Connecting to WebSocket: {self.ws_url}")
            async with websockets.connect(self.ws_url) as websocket:
                logger.info("Connected to WebSocket")
                
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
                
                # Wait for subscription confirmation
                response = await websocket.recv()
                logger.info(f"Subscription response: {response}")

                async for message in websocket:
                    try:
                        data = json.loads(message)
                        if "params" in data:
                            # Process the notification
                            value = data["params"]["result"]["value"]
                            signature = value.get("signature")
                            
                            if signature:
                                logger.debug(f"Received notification for signature: {signature}")
                                # Fetch full transaction details to parse swap
                                tx_details = await self.get_transaction_details(signature)
                                if tx_details:
                                    swap_data = self.parse_swap(tx_details, token_mint)
                                    if swap_data:
                                        if asyncio.iscoroutinefunction(callback):
                                            await callback(swap_data)
                                        else:
                                            callback(swap_data)
                    except json.JSONDecodeError:
                        logger.error("Failed to decode JSON message")
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                        
        except Exception as e:
            logger.error(f"Connection error: {e}")
        finally:
            if self.session:
                await self.session.close()

    async def get_transaction_details(self, signature: str) -> Optional[Dict]:
        """Fetches full transaction details using RPC."""
        # Check if session is active
        if self.session is None or self.session.closed:
             self.session = aiohttp.ClientSession()

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [
                signature,
                {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0, "commitment": "confirmed"}
            ]
        }
        
        try:
            async with self.session.post(self.rpc_url, json=payload) as response:
                if response.status != 200:
                    logger.error(f"RPC Error: {response.status}")
                    return None
                result = await response.json()
                if "error" in result:
                    logger.error(f"RPC Error Response: {result['error']}")
                    return None
                return result.get("result")
        except Exception as e:
            logger.error(f"Error fetching transaction {signature}: {e}")
            return None

    def parse_swap(self, tx_data: Dict, token_mint: str) -> Optional[Dict]:
        """
        Parses transaction data to extract swap details.
        Returns None if not a swap or irrelevant.
        """
        if not tx_data:
            return None
            
        meta = tx_data.get("meta")
        if not meta:
            return None
            
        if meta.get("err"):
            return None

        transaction = tx_data.get("transaction")
        if not transaction:
            return None

        # 1. Identify the Signer (User) - typically the first account that signed
        message = transaction.get("message", {})
        account_keys = message.get("accountKeys", [])
        
        signer = None
        if isinstance(account_keys, list):
            # Handle different formats of accountKeys
            first_account = account_keys[0]
            if isinstance(first_account, dict):
                if first_account.get("signer"):
                    signer = first_account.get("pubkey")
                else:
                    # Fallback: usually first account is fee payer/signer
                    signer = first_account.get("pubkey")
            else:
                signer = first_account # String format

        if not signer:
            return None
        
        # 2. Check Token Balance Changes (Pre vs Post)
        pre_token_balances = meta.get("preTokenBalances", [])
        post_token_balances = meta.get("postTokenBalances", [])

        # Helper to find balance for an account index and mint
        def get_token_balance(balances, mint, owner):
            for b in balances:
                if b.get("mint") == mint and b.get("owner") == owner:
                    amount_info = b.get("uiTokenAmount", {})
                    return float(amount_info.get("uiAmount") or 0)
            return 0.0

        pre_bal = get_token_balance(pre_token_balances, token_mint, signer)
        post_bal = get_token_balance(post_token_balances, token_mint, signer)
        token_change = post_bal - pre_bal

        if abs(token_change) < 1e-9:
            return None # No significant change in target token balance for signer

        # 3. Check SOL Balance Changes (for Buy/Sell determination)
        pre_sol_balances = meta.get("preBalances", [])
        post_sol_balances = meta.get("postBalances", [])
        
        # Signer is always index 0 in pre/post balances arrays corresponding to accountKeys
        if not pre_sol_balances or not post_sol_balances:
            return None

        sol_change_lamports = post_sol_balances[0] - pre_sol_balances[0]
        sol_change = sol_change_lamports / 1e9

        # 4. Determine Swap Direction and Amounts
        # Heuristic: 
        # Buy: SOL decreases, Token increases
        # Sell: Token decreases, SOL increases
        
        swap_type = "unknown"
        amount_in = 0.0
        amount_out = 0.0
        input_token = ""
        output_token = ""
        price_per_token = 0.0

        if token_change > 0:
            # Token balance increased -> BUY
            swap_type = "buy"
            amount_out = token_change
            output_token = token_mint
            # SOL/WSOL spent (amount_in) is practically the decrease in SOL balance
            # Note: This includes network fees, which might slightly skew the price for small swaps
            amount_in = abs(sol_change) 
            input_token = "SOL" 
        else:
            # Token balance decreased -> SELL
            swap_type = "sell"
            amount_in = abs(token_change)
            input_token = token_mint
            amount_out = sol_change # Includes fees
            output_token = "SOL"

        # Calculate price if possible
        if amount_out > 0:
             if swap_type == "buy":
                 price_per_token = amount_in / amount_out
             else:
                 price_per_token = amount_out / amount_in

        # 5. Identify DEX (Optional - from logs)
        dex = "unknown"
        logs = meta.get("logMessages", [])
        log_str = " ".join(logs) if logs else ""
        
        if RAYDIUM_V4_PROGRAM_ID in log_str:
            dex = "raydium"
        elif PUMP_FUN_PROGRAM_ID in log_str:
            dex = "pumpfun"
        elif "JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4" in log_str: # Jupiter
            dex = "jupiter"

        return {
            "signature": transaction.get("signatures", [""])[0],
            "signer": signer,
            "type": swap_type,
            "amount_in": amount_in,
            "input_token": input_token,
            "amount_out": amount_out,
            "output_token": output_token,
            "price_per_token": price_per_token,
            "dex": dex,
            "timestamp": tx_data.get("blockTime"),
            "slot": tx_data.get("slot")
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
