import asyncio
import aiohttp
import time
import logging
from typing import List, Dict, Optional
from datetime import datetime, timezone
from CryptoDevTools.constants import GlobalConstants

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OnChainHistory:
    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url

    async def get_latest_candles(self, token_mint: str, resolution: int = 60, limit: int = 1000) -> List[Dict]:
        """
        Fetches the latest candles for a given token mint by analyzing recent on-chain transactions.
        
        Args:
            token_mint (str): The mint address of the token.
            resolution (int): Candle resolution in seconds (default 60s).
            limit (int): Number of transactions to analyze (default 1000). Higher limits take longer.
            
        Returns:
            List[Dict]: A list of candles in the format {time, open, high, low, close, volume}.
        """
        async with aiohttp.ClientSession() as session:
            # 1. Find the liquidity pool address (largest holder heuristic)
            pool_address = await self._get_liquidity_pool(session, token_mint)
            if not pool_address:
                logger.warning(f"Could not find liquidity pool for {token_mint}")
                return []
            
            logger.info(f"Using liquidity pool address: {pool_address} for mint {token_mint}")

            # 2. Fetch the latest N signatures for the pool address
            signatures = await self._get_signatures(session, pool_address, limit)
            if not signatures:
                logger.warning(f"No signatures found for pool {pool_address}")
                return []
            
            logger.info(f"Found {len(signatures)} signatures. Fetching details...")

            # 3. Fetch transaction details in batches
            transactions = await self._get_transactions_batch(session, signatures)
            
            # 4. Parse swaps
            swaps = []
            for tx in transactions:
                if tx:
                    swap = self._parse_swap(tx, token_mint)
                    if swap:
                        swaps.append(swap)
            
            logger.info(f"Parsed {len(swaps)} swaps from transactions")

            # 5. Aggregate into candles
            candles = self._build_candles(swaps, resolution)
            return candles

    async def _get_liquidity_pool(self, session: aiohttp.ClientSession, token_mint: str) -> Optional[str]:
        payload = {
            "jsonrpc": "2.0", "id": 1, "method": "getTokenLargestAccounts",
            "params": [token_mint, {"commitment": "confirmed"}]
        }
        try:
            async with session.post(self.rpc_url, json=payload) as response:
                result = await response.json()
                if "error" in result:
                    return None
                value = result.get("result", {}).get("value", [])
                if value:
                    # Return the largest account (usually the pool/bonding curve)
                    return value[0]["address"]
        except Exception as e:
            logger.error(f"Error finding liquidity pool: {e}")
        return None

    async def _get_signatures(self, session: aiohttp.ClientSession, address: str, limit: int) -> List[str]:
        payload = {
            "jsonrpc": "2.0", "id": 1, "method": "getSignaturesForAddress",
            "params": [address, {"limit": limit, "commitment": "confirmed"}]
        }
        try:
            async with session.post(self.rpc_url, json=payload) as response:
                result = await response.json()
                if "error" in result:
                    logger.error(f"Error fetching signatures: {result['error']}")
                    return []
                return [item["signature"] for item in result.get("result", [])]
        except Exception as e:
            logger.error(f"Error fetching signatures: {e}")
            return []

    async def _get_transactions_batch(self, session: aiohttp.ClientSession, signatures: List[str]) -> List[Dict]:
        batch_size = 50 # Helius allows batch requests, but standard RPC might have limits.
        all_txs = []
        
        for i in range(0, len(signatures), batch_size):
            batch_sigs = signatures[i:i + batch_size]
            batch_payload = []
            for idx, sig in enumerate(batch_sigs):
                batch_payload.append({
                    "jsonrpc": "2.0",
                    "id": idx,
                    "method": "getTransaction",
                    "params": [
                        sig,
                        {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0, "commitment": "confirmed"}
                    ]
                })
            
            try:
                async with session.post(self.rpc_url, json=batch_payload) as response:
                    batch_results = await response.json()
                    if isinstance(batch_results, list):
                        for res in batch_results:
                            if "result" in res and res["result"]:
                                all_txs.append(res["result"])
                    else:
                        logger.warning(f"Unexpected batch response format: {batch_results}")

            except Exception as e:
                logger.error(f"Error fetching transaction batch: {e}")
                
        return all_txs

    def _parse_swap(self, tx: Dict, token_mint: str) -> Optional[Dict]:
        """
        Parses a transaction to identify a swap involving the token_mint.
        Simplified heuristic: Check balance changes of token_mint vs SOL (or WSOL).
        """
        try:
            meta = tx.get("meta")
            if not meta or meta.get("err"): # Skip failed transactions
                return None
            
            block_time = tx.get("blockTime")
            if not block_time:
                return None

            # Check Token Balance Changes
            pre_token_balances = meta.get("preTokenBalances", [])
            post_token_balances = meta.get("postTokenBalances", [])
            
            token_change = 0.0
            signer = None
            
            # Find the user who traded the token (usually the payer/signer)
            # The signer is always at index 0 in accountKeys
            account_keys = tx.get("transaction", {}).get("message", {}).get("accountKeys", [])
            if not account_keys:
                return None
                
            signer_key = account_keys[0].get("pubkey") if isinstance(account_keys[0], dict) else account_keys[0]

            # Calculate token change for the signer (or anyone, really - looking for the biggest change)
            # Let's find the change for the mint we care about
            
            total_change = 0
            
            for post in post_token_balances:
                if post.get("mint") == token_mint:
                    owner = post.get("owner")
                    # Retrieve pre-balance
                    pre_bal = 0
                    for pre in pre_token_balances:
                        if pre.get("accountIndex") == post.get("accountIndex"):
                            pre_bal = float(pre.get("uiTokenAmount", {}).get("uiAmount") or 0)
                            break
                    
                    post_bal = float(post.get("uiTokenAmount", {}).get("uiAmount") or 0)
                    change = post_bal - pre_bal
                    
                    # We are looking for the Trader's change. 
                    # If this is a pool, its change is opposite to the trader.
                    # We assume the user's wallet is not a program.
                    # Simple heuristic: If owner == signer, it's the user.
                    if owner == signer:
                        token_change = change
                    elif abs(change) > abs(token_change):
                         # If we haven't found a signer match, take the largest change as the swap amount
                         # But need to be careful about direction.
                         # If pool gains tokens, user sold. Token change for user is negative.
                         # We'll refine this later. For now, rely on signer match or assume user is the opposite of the pool.
                         pass
            
            if abs(token_change) < 1e-9:
                return None

            # Check SOL Balance Changes (for price calculation)
            pre_sol_balances = meta.get("preBalances", [])
            post_sol_balances = meta.get("postBalances", [])
            
            if not pre_sol_balances or not post_sol_balances:
                return None
                
            # SOL change for signer
            sol_change_lamports = post_sol_balances[0] - pre_sol_balances[0]
            sol_change = sol_change_lamports / 1e9

            # Determine Price
            # If Token Change > 0 (Buy): Spent SOL (Sol change < 0)
            # If Token Change < 0 (Sell): Gained SOL (Sol change > 0)
            
            price_per_token = 0.0
            sol_vol = abs(sol_change)
            
            if token_change > 0 and sol_change < 0:
                 price_per_token = abs(sol_change / token_change)
            elif token_change < 0 and sol_change > 0:
                 price_per_token = abs(sol_change / token_change)
            else:
                 # Complex swap or not a direct SOL pair (e.g. USDC)
                 # Ignoring for simplified SOL-based candle chart
                 return None
                 
            return {
                "time": block_time,
                "price": price_per_token,
                "token_volume": abs(token_change),
                "sol_volume": sol_vol,
                "side": "buy" if token_change > 0 else "sell"
            }

        except Exception as e:
            logger.debug(f"Error parsing swap: {e}")
            return None

    def _build_candles(self, swaps: List[Dict], resolution: int) -> List[Dict]:
        if not swaps:
            return []
            
        # Sort swaps by time ascending
        swaps.sort(key=lambda x: x["time"])
        
        candles = {}
        last_close = swaps[0]["price"] # Correctly set initial previous close
        
        # Fill time gaps if necessary, or just rely on sparse list. 
        # TV handles gaps, but ensuring continuity is better.
        
        for swap in swaps:
            # Bucket by time
            bucket_time = (swap["time"] // resolution) * resolution
            
            if bucket_time not in candles:
                candles[bucket_time] = {
                    "time": bucket_time * 1000, # MS for JS
                    "open": last_close, # Open should be previous close theoretically, or first trade price
                    "high": swap["price"],
                    "low": swap["price"],
                    "close": swap["price"],
                    "volume": 0
                }
                # Fix for the VERY first candle if it's the start
                if len(candles) == 1:
                     candles[bucket_time]["open"] = swap["price"]
            
            c = candles[bucket_time]
            c["high"] = max(c["high"], swap["price"])
            c["low"] = min(c["low"], swap["price"])
            c["close"] = swap["price"]
            c["volume"] += swap["sol_volume"]
            
            last_close = c["close"]
        
        # Convert dict to sorted list
        sorted_candles = sorted(candles.values(), key=lambda x: x["time"])
        return sorted_candles
        
        # Convert dict to sorted list
        sorted_candles = sorted(candles.values(), key=lambda x: x["time"])
        return sorted_candles

# Validating usage
# analyzer = OnChainHistory("https://api.mainnet-beta.solana.com")
# candles = asyncio.run(analyzer.get_latest_candles("MintAddress..."))
