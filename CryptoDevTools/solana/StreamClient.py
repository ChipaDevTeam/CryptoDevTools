import asyncio
import json
import logging
import websockets
import aiohttp
from typing import Dict, Optional, Callable, Any
from CryptoDevTools.constants import DexPrograms

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SolanaSwapListener:
    def __init__(self, rpc_url: str, ws_url: str):
        self.rpc_url = rpc_url
        self.ws_url = ws_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(5) # Limit concurrent RPC requests
        self.last_request_time = 0.0
        self.request_interval = 0.2 # Minimum time between requests (seconds)
        self.processed_signatures = set() # Cache to avoid processing duplicates

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
                
                # Helius only supports 1 address per subscription.
                # We can send multiple subscribe requests.
                try_params = accounts_to_watch if len(accounts_to_watch) <= 3 else accounts_to_watch[:3]
                
                logger.info(f"Subscribing to logs for: {try_params}")
                
                for i, account in enumerate(try_params):
                    payload = {
                        "jsonrpc": "2.0",
                        "id": i + 1,
                        "method": "logsSubscribe",
                        "params": [
                            {"mentions": [account]},
                            {"commitment": "confirmed"}
                        ]
                    }
                    await websocket.send(json.dumps(payload))
                    
                    # Wait for subscription confirmation
                    response = await websocket.recv()
                    logger.info(f"Subscription response for {account}: {response}")

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
        if signature in self.processed_signatures:
            return
        self.processed_signatures.add(signature)
        
        # Keep cache size manageable
        if len(self.processed_signatures) > 1000:
            # Remove some old signatures (simple approach: clear half)
            self.processed_signatures = set(list(self.processed_signatures)[-500:])
            
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

    async def get_transaction_details(self, signature: str, retries: int = 3) -> Optional[Dict]:
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

            for attempt in range(retries):
                try:
                    async with self.session.post(self.rpc_url, json=payload) as response:
                        if response.status == 429:
                             logger.warning(f"Rate limited (429) for {signature}. Retrying in 2s...")
                             await asyncio.sleep(2)
                             continue

                        if response.status != 200:
                            logger.error(f"RPC Error: {response.status}")
                            return None
                        
                        result = await response.json()
                        
                        if "error" in result:
                            # Handle specific RPC errors if needed
                            logger.error(f"RPC Error Response: {result['error']}")
                            return None
                        return result.get("result")
                except aiohttp.ClientError as e:
                    logger.error(f"Network error fetching transaction {signature} (attempt {attempt+1}/{retries}): {e}")
                    if attempt < retries - 1:
                        await asyncio.sleep(1)
                    else:
                        return None
                except Exception as e:
                    logger.error(f"Error fetching transaction {signature}: {e}")
                    return None
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

        # 1. Identify the Signer (User)
        message = transaction.get("message", {})
        account_keys = message.get("accountKeys", [])
        
        signer = None
        if isinstance(account_keys, list):
            # Handle different formats of accountKeys
            if len(account_keys) > 0:
                first_account = account_keys[0]
                if isinstance(first_account, dict):
                    signer = first_account.get("pubkey")
                else:
                    signer = first_account # String format

        if not signer:
             logger.debug("Could not identify signer")
             return None
        
        # 2. Check Token Balance Changes (Pre vs Post)
        pre_token_balances = meta.get("preTokenBalances", [])
        post_token_balances = meta.get("postTokenBalances", [])

        token_change = 0.0
        
        # Consistent Logic from OnChainHistory.py:
        # Calculate token change for the signer by iterating balances
        found_change = False
        for post in post_token_balances:
            if post.get("mint") == token_mint:
                owner = post.get("owner")
                if owner == signer:
                    # Retrieve pre-balance
                    pre_bal = 0.0
                    for pre in pre_token_balances:
                        if pre.get("accountIndex") == post.get("accountIndex"):
                            pre_bal = float(pre.get("uiTokenAmount", {}).get("uiAmount") or 0)
                            break
                    
                    post_val = float(post.get("uiTokenAmount", {}).get("uiAmount") or 0)
                    token_change = post_val - pre_bal
                    found_change = True
                    break 

        if not found_change or abs(token_change) < 1e-9:
             # Fallback: check if we just missed the signer match (sometimes owner != signer if PDA involves)
             # But for safety in realtime stream, return None rather than bad data
             # logger.debug(f"No token balance change for signer {signer}")
             return None

        # 3. Check SOL Balance Changes (for Buy/Sell determination)
        pre_sol_balances = meta.get("preBalances", [])
        post_sol_balances = meta.get("postBalances", [])
        
        if not pre_sol_balances or not post_sol_balances:
            return None

        # SOL change for signer
        if len(post_sol_balances) < 1 or len(pre_sol_balances) < 1:
             return None
             
        # Check if Wrapped SOL (WSOL) was involved in the swap
        wsol_mint = "So11111111111111111111111111111111111111112"
        wsol_change = 0.0
        
        # Check WSOL balance changes (if token_mint is not WSOL itself)
        if token_mint != wsol_mint:
            for post in post_token_balances:
                if post.get("mint") == wsol_mint:
                    owner = post.get("owner")
                    if owner == signer:
                        pre_bal_wsol = 0.0
                        for pre in pre_token_balances:
                            if pre.get("accountIndex") == post.get("accountIndex"):
                                val = pre.get("uiTokenAmount", {}).get("uiAmount")
                                if val is not None:
                                    pre_bal_wsol = float(val)
                                break
                        val = post.get("uiTokenAmount", {}).get("uiAmount")
                        post_val_wsol = float(val) if val is not None else 0.0
                        wsol_change = post_val_wsol - pre_bal_wsol
                        break

        sol_change_lamports_native = post_sol_balances[0] - pre_sol_balances[0]
        native_change_sol = sol_change_lamports_native / 1e9
        
        # Total SOL Change = Native Change + WSOL Change
        total_sol_change = native_change_sol + wsol_change
        
        # If total change is tiny (just fee?), skip.
        if abs(total_sol_change) < 1e-9:
             return None
             
        sol_change_adjusted = abs(total_sol_change)
        
        # 4. Determine Swap Direction and Amounts
        swap_type = "unknown"
        amount_in = 0.0
        amount_out = 0.0
        price_per_token = 0.0

        if token_change > 0:
            # Token balance increased -> BUY
            if sol_change_lamports > 0: return None # Invalid state
            
            swap_type = "buy"
            amount_out = token_change       # Tokens Received
            amount_in = sol_change_adjusted # SOL Spent
            
            price_per_token = abs(amount_in / amount_out)

        elif token_change < 0:
            # Token balance decreased -> SELL
            if sol_change_lamports < 0: return None # Invalid state
            
            swap_type = "sell"
            amount_in = abs(token_change)   # Tokens Sold
            amount_out = sol_change_adjusted # SOL Received
            
            price_per_token = abs(amount_out / amount_in)
        
        else:
            return None

        # Sanity Filter
        if price_per_token <= 0:
            return None

        block_time = tx_data.get("blockTime")
        timestamp = block_time if block_time else int(time.time())

        return {
            "timestamp": timestamp,
            "type": swap_type,
            "price_per_token": price_per_token,
            "amount_in": amount_in,
            "amount_out": amount_out,
            "signature": transaction.get("signatures", [""])[0]
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
