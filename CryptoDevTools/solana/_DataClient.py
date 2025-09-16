from .DataAPI.TokenAPI.TokenApi import TokenAPI

from CryptoDevTools.constants import GlobalConstants

class SolanaDataClient:
    def __init__(self):
        self.token_api = TokenAPI()
    def getTokenMetadata(self, token_address):
        return self.token_api.get_token_metadata(token_address)
    def getNewTokensByExchange(self, exchange_name="PumpFun"):
        if exchange_name not in GlobalConstants.EXCHANGES:
            raise ValueError(f"Exchange '{exchange_name}' is not supported.")
        return self.token_api.get_new_tokens(exchange_name=exchange_name)