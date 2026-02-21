import asyncio
import json
import logging
import websockets
import aiohttp
from typing import Dict, Optional, Callable, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DexPrograms:
    RAYDIUM_V4_PROGRAM_ID = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
    PUMP_FUN_PROGRAM_ID = "6EF8rrecthR5DkdfxkqCnDWWFkkKCk2dNRwCpwdRLuqt"
    RAYDIUM_AMM_V4 = "675kPXaZJ9UQCj3D9V6G3z1P7XpYj7945A8K5M42S28L"
    RAYDIUM_CLMM = "CAMMCzo5YLgUDd1G51k5VfC1r4N2z977u4T4q5v51717"
    RAYDIUM_CONCENTRATED_LIQUIDITY = "whirVjicr14JgS2fS2C3C91W6671A6y4qS3k45U6f2f"
    ORCA_WHIRLPOOLS = "whirVjicr14JgS2fS2C3C91W6671A6y4qS3k45U6f2f"
    ORCA_TOKEN_SWAP_V2 = "9W959DqjETzGZJ5C2Q3C91W6671A6y4qS3k45U6f2f"
    METEORA_DLMM = "LBUZKhsJWnrJvPz36k3zT9Fq5s17596p9v7a8S9r3a7"
    JUPITER_AGGREGATOR_V6 = "JUP6LKBh1qy2t34V462D6y4qS3k45U6f2f"
    SERUM_LEGACY = "9xQeWvG816bUx94zG3z1P7XpYj7945A8K5M42S28L"

class SolanaSwapListener:
    def __init__(self, rpc_url: str, ws_url: str):
        self.rpc_url = rpc_url
        self.ws_url = ws_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(5) # Limit concurrent RPC requests
        self.last_request_time = 0.0
        self.request_interval = 0.2 # Minimum time between requests (seconds)

    async def _get_liquidity_accounts(self, token_mint: str) -> list[str]:
        """
        Heuristic: The largest token holders are usually Liquidity Pools (Raydium, Orca, etc.)
        or Bonding Curves (PumpFun).
        Listening to these accounts is more reliable than listening to the Mint itself
        because swap transactions always Write to the pool's Vault account.
        """
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenLargestAccounts",
            "params": [
                token_mint,
                {"commitment": "confirmed"}
            ]
        }
        try:
            async with self.session.post(self.rpc_url, json=payload) as response:
                result = await response.json()
                if "error" in result:
                    logger.warning(f"Could not fetch largest accounts: {result['error']}")
                    return []
                
                value = result.get("result", {}).get("value", [])
                # Return the top 5 largest accounts
                accounts = [item["address"] for item in value[:5]]
                logger.info(f"Identified potential pool accounts to monitor: {accounts}")
                return accounts
        except Exception as e:
            logger.error(f"Error fetching largest accounts: {e}")
            return []

    async def start(self, token_mint: str, callback: Callable[[Dict[str, Any]], Any]):
        """
        Starts listening for swap events for a specific token mint.
        
        Args:
            token_mint (str): The Token Mint Address to listen for.
            callback (Callable): A function to call with the parsed swap data.
        """
        # Determine accounts to watch
        # We need a session for _get_liquidity_accounts
        if self.session is None or self.session.closed:
             self.session = aiohttp.ClientSession()

        try:
            pool_accounts = await self._get_liquidity_accounts(token_mint)
        except Exception as e:
            logger.error(f"Failed to find pool accounts: {e}")
            pool_accounts = []
            
        # Watch Mint + generic pool accounts to maximize chance involved in tx
        accounts_to_watch = [token_mint]
        # Subscribe to top 2 accounts (usually main LP + maybe bonding curve)
        # Limit total mentions as RPCs often cap at 1-5
        if pool_accounts:
             accounts_to_watch.extend(pool_accounts[:2])

        try:
            logger.info(f"Connecting to WebSocket: {self.ws_url}")
            # Add ping_interval to keep connection alive, or None if server handles it. 
            # Some RPCs aggressive with ping. Using defaults usually OK but let's be explicit or catch errors.
            async with websockets.connect(self.ws_url, ping_interval=20, ping_timeout=20) as websocket:
                logger.info("Connected to WebSocket")
                
                # Subscribe to logs mentioning the token mint OR its pool accounts
                # Note: logsSubscribe 'mentions' only supports ONE filter array which is OR logic?
                # Actually, mentions is an array. A transaction matching ANY of these pubkeys is returned?
                # Yes, "mentions" array functions as OR.
                
                # However, there is a limit on array size (usually 1 or small).
                # If RPC fails with too many mentions, fall back to just the Mint + Top 1.
                
                # Try all first
                try_params = accounts_to_watch if len(accounts_to_watch) <= 3 else accounts_to_watch[:3]
                
                logger.info(f"Subscribing to logs for: {try_params}")
                
                payload = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "logsSubscribe",
                    "params": [
                        {"mentions": try_params},
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
                        
                        # Debug: Log type of message received (remove in production if too noisy)
                        if "method" in data:
                             logger.debug(f"Received method: {data.get('method')}")
                        elif "result" in data:
                             logger.debug(f"Received result: {data.get('result')}")
                        else:
                             logger.info(f"Received unknown message structure: {str(data)[:100]}...")

                        if "params" not in data:
                             continue

                        if "params" in data:
                            # Process the notification
                            value = data["params"]["result"]["value"]
                            signature = value.get("signature")
                            
                            # Fire and forget (or rather, run in background) so we don't block the websocket loop
                            if signature:
                                logger.info(f"Detected Transaction: {signature}")
                                asyncio.create_task(self._process_signature(signature, token_mint, callback))

                    except json.JSONDecodeError:
                        logger.error("Failed to decode JSON message")
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                        
        except Exception as e:
            logger.error(f"Connection error: {e}")
        finally:
            if self.session:
                await self.session.close()

    async def _process_signature(self, signature: str, token_mint: str, callback: Callable):
        """Process a single signature with rate limiting."""
        logger.debug(f"Processing signature: {signature}")
        # Fetch full transaction details to parse swap
        tx_details = await self.get_transaction_details(signature)
        if tx_details:
            swap_data = self.parse_swap(tx_details, token_mint)
            if swap_data:
                logger.info(f"Swap confirmed: {signature}")
                if asyncio.iscoroutinefunction(callback):
                    await callback(swap_data)
                else:
                    callback(swap_data)
            else:
                logger.debug(f"Transaction {signature} was not a valid swap for {token_mint}")
        else:
             logger.warning(f"Failed to fetch details for {signature}")

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
        
        async with self.semaphore:
             # Rate limiting sleep
            import time
            now = time.time()
            time_since_last = now - self.last_request_time
            if time_since_last < self.request_interval:
                await asyncio.sleep(self.request_interval - time_since_last)
            self.last_request_time = time.time()

            try:
                async with self.session.post(self.rpc_url, json=payload) as response:
                    if response.status == 429:
                         logger.warning(f"Rate limited (429) for {signature}. Retrying in 2s...")
                         await asyncio.sleep(2)
                         # Recursive retry (simple)
                         return await self.get_transaction_details(signature)

                    if response.status != 200:
                        logger.error(f"RPC Error: {response.status}")
                        return None
                    
                    result = await response.json()
                    
                    if "error" in result:
                        # Handle specific RPC errors if needed
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
            # Fallback: account 0 is usually fee payer
            if account_keys:
                 signer = account_keys[0] if isinstance(account_keys[0], str) else account_keys[0].get("pubkey")

        if not signer:
             logger.debug("Could not identify signer")
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

        # Debugging info
        if abs(token_change) < 1e-9:
             # Try determining if *any* account had a significant change for this mint, 
             # maybe we identified the wrong signer (some swaps happen via PDA/router)
             total_moved = 0
             for b in post_token_balances:
                 if b.get("mint") == token_mint:
                     owner = b.get("owner")
                     p_bal = get_token_balance(pre_token_balances, token_mint, owner)
                     diff = float(b.get("uiTokenAmount", {}).get("uiAmount") or 0) - p_bal
                     if abs(diff) > 1e-9 and owner != signer:
                         # Found a movement, but not for "signer". 
                         # This happens in some aggregator swaps where user is not account 0 or transfer is internal
                         pass
             
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
        
        if DexPrograms.RAYDIUM_V4_PROGRAM_ID in log_str or DexPrograms.RAYDIUM_AMM_V4 in log_str:
            dex = "raydium"
        elif DexPrograms.RAYDIUM_CLMM in log_str or DexPrograms.RAYDIUM_CONCENTRATED_LIQUIDITY in log_str:
            dex = "raydium_clmm"
        elif DexPrograms.PUMP_FUN_PROGRAM_ID in log_str:
            dex = "pumpfun"
        elif DexPrograms.ORCA_WHIRLPOOLS in log_str or DexPrograms.ORCA_TOKEN_SWAP_V2 in log_str:
            dex = "orca"
        elif DexPrograms.METEORA_DLMM in log_str:
            dex = "meteora"
        elif DexPrograms.JUPITER_AGGREGATOR_V6 in log_str:
            dex = "jupiter"
        elif DexPrograms.SERUM_LEGACY in log_str:
            dex = "serum"

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
