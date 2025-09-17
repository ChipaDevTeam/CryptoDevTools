from .DataAPI.TokenAPI.TokenApi import TokenAPI

from CryptoDevTools.constants import GlobalConstants
from CryptoDevTools.models.solana.token_data import HoldersData, TokenMetadata

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
        return self.token_api.get_new_tokens(exchange_name=exchange_name)
    def getGraduatedTokens(self, sortBy=GlobalConstants.GRADUATED_DEFAULT_SORT):
        if sortBy not in GlobalConstants.SORT_BY_OPTIONS:
            raise ValueError(f"Invalid sortBy value. Must be one of {GlobalConstants.SORT_BY_OPTIONS}")
        return self.token_api.get_graduated_tokens(sortBy=sortBy)
    def getHoldersTokens(self, token_address):
        data = self.token_api.get_holders_tokens(token_address)

        return HoldersData(
            total_holders=data.get("totalHolders"),
            top_holders=data.get("topHolders", [])
        )