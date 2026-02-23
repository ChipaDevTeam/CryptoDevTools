from .DataAPI.TokenAPI.TokenApi import TokenAPI
from .OnChainHistory import OnChainHistory
import asyncio
import base64
import requests
from solders.pubkey import Pubkey
from CryptoDevTools.constants import GlobalConstants
from CryptoDevTools.models.solana.token_data import HoldersData, TokenMetadata, PumpFunToken, GraduatedTokensResponse, TradesResponse
from .helpers.metadata_decoder import MetadataDecoder
from ._SolanaClient import SolanaClient

class SolanaDataClient:
    def __init__(self, rpc_url=None):
        self.token_api = TokenAPI()
        self.rpc_url = rpc_url or GlobalConstants.HELIUS_RPC
        self.solana_client = SolanaClient(self.rpc_url)

    def getTokenMetadata(self, token_address):
        """
        Fetches token metadata directly from the blockchain (Metaplex Metadata Account).
        No third-party indexer APIs are used.
        """
        try:
            mint_pubkey = Pubkey.from_string(token_address)
            
            # 1. Derive Metadata PDA
            pda = MetadataDecoder.get_metadata_pda(mint_pubkey)

            # 2. Get Account Info via RPC
            account_info_response = self.solana_client.getAccountInfo(str(pda))
            
            if not account_info_response or "error" in account_info_response:
                print(f"Error fetching metadata account: {account_info_response.get('error', 'Unknown Error')}")
                return None
            
            result = account_info_response.get("result", {}).get("value")
            
            if not result:
                print(f"No metadata account found for {token_address} at {pda}")
                return None
                
            data_base64 = result.get("data", ["", "base64"])[0]
            if not data_base64:
                return None
                
            data_bytes = base64.b64decode(data_base64)
            
            # 3. Decode Metadata
            try:
                metadata = MetadataDecoder.decode_metadata(data_bytes)
            except Exception as e:
                print(f"Error decoding metadata: {e}")
                return None
            
            # 4. (Optional) Fetch JSON from URI if available
            content = {
                "json_uri": metadata["data"]["uri"],
                "metadata": {
                    "name": metadata["data"]["name"],
                    "symbol": metadata["data"]["symbol"],
                    "uri": metadata["data"]["uri"]
                }
            }
            
            # Map valid creators to format
            creators = []
            if metadata["data"].get("creators"):
                for c in metadata["data"]["creators"]:
                    creators.append({
                        "address": c["address"],
                        "share": c["share"],
                        "verified": c["verified"]
                    })

            # Check Mint Supply separate call? Or just return partial if not critical.
            # The original API call likely returned full asset data. Here we have Metadata.
            
            return TokenMetadata(
                last_indexed_slot=0, # Not applicable
                interface="MplTokenMetadata", 
                id=token_address,
                content=content,
                authorities={
                    "update_authority": metadata["update_authority"]
                },
                compression={"compressed": False}, 
                collection=metadata.get("collection"), 
                royalty={
                    "percent": (metadata["data"]["seller_fee_basis_points"] or 0) / 100.0,
                    "basis_points": metadata["data"]["seller_fee_basis_points"],
                    "primary_sale_happened": metadata["primary_sale_happened"],
                    "locked": False 
                },
                creators=creators,
                ownership={
                    "frozen": False, 
                    "delegated": False,
                    "ownership_model": "token"
                },
                supply={}, 
                mutable=metadata["is_mutable"],
                burnt=False,
                token_info={}
            )

        except Exception as e:
            print(f"Error in on-chain metadata fetch: {e}")
            return None

    def getNewTokensByExchange(self, exchange_name="PumpFun"):
        if exchange_name not in GlobalConstants.EXCHANGES:
            raise ValueError(f"Exchange '{exchange_name}' is not supported.")
        data = self.token_api.get_new_tokens(exchange_name=exchange_name)
        
        # Handle list of tokens from API
        if isinstance(data, list):
            return [PumpFunToken.from_dict(token_data) for token_data in data]
        else:
            # Handle single token response
            return PumpFunToken.from_dict(data)
    def getGraduatedTokens(self, sortBy=GlobalConstants.GRADUATED_DEFAULT_SORT):
        if sortBy not in GlobalConstants.SORT_BY_OPTIONS:
            raise ValueError(f"Invalid sortBy value. Must be one of {GlobalConstants.SORT_BY_OPTIONS}")
        data = self.token_api.get_graduated_tokens(sortBy=sortBy)
        return GraduatedTokensResponse.from_dict(data)
    def getHoldersTokens(self, token_address):
        data = self.token_api.get_holders_tokens(token_address)

        return HoldersData(
            total_holders=data.get("totalHolders"),
            top_holders=data.get("topHolders", [])
        )
    def getTrades(self, token_address, limit=100, cursor=0, minSolAmount=0):
        data = self.token_api.get_trades(token_address, limit, cursor, minSolAmount)
        trades_response = TradesResponse.from_dict(data)
        return trades_response

    def get_latest_candles_onchain(self, token_mint, resolution=60, limit=100):
        """
        Fetches the latest candles directly from on-chain data.
        """
        analyzer = OnChainHistory(GlobalConstants.HELIUS_RPC)
        try:
            # Check for existing loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                 # Should not block a running loop, better to run in executor or just return awaitable if this was async
                 # But this function is synchronous signature.
                 # Creating task and waiting for result in threadsafe manner? No simple way without async def.
                 # Assuming this is called from sync context.
                 if not loop.is_running():
                     return loop.run_until_complete(analyzer.get_latest_candles(token_mint, resolution, limit))
                 
                 # If loop IS running (e.g. uvicorn), we can't block it.
                 # But Flask + threading usually means no loop.
                 future = asyncio.run_coroutine_threadsafe(analyzer.get_latest_candles(token_mint, resolution, limit), loop)
                 return future.result()
            else:
                 return loop.run_until_complete(analyzer.get_latest_candles(token_mint, resolution, limit))
        except RuntimeError:
            # No loop in current thread
            return asyncio.run(analyzer.get_latest_candles(token_mint, resolution, limit))
