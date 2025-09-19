from .DataAPI.TokenAPI.TokenApi import TokenAPI

from CryptoDevTools.constants import GlobalConstants
from CryptoDevTools.models.solana.token_data import HoldersData, TokenMetadata, PumpFunToken, GraduatedTokensResponse, TradesResponse

class SolanaDataClient:
    def __init__(self):
        self.token_api = TokenAPI()
    def getTokenMetadata(self, token_address):
        data = self.token_api.get_token_metadata(token_address)
        return TokenMetadata(
            last_indexed_slot=data.get("lastIndexedSlot"),
            interface=data.get("interface"),
            id=data.get("id"),
            content=data.get("content"),
            authorities=data.get("authorities"),
            compression=data.get("compression"),
            collection=data.get("collection"),
            royalty=data.get("royalty"),
            creators=data.get("creators"),
            ownership=data.get("ownership"),
            supply=data.get("supply"),
            mutable=data.get("mutable"),
            burnt=data.get("burnt"),
            token_info=data.get("tokenInfo"),
        )
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