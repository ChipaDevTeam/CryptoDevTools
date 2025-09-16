from .api.GetTokenMetadata import GetTokenMetadata
from .api.GetNewTokensByExchange import GetNewTokensByExchange

class TokenAPI:
    def __init__(self):
        self.metadata_api = GetTokenMetadata()
        self.new_tokens_api = GetNewTokensByExchange()

    def get_token_metadata(self, token_address):
        return self.metadata_api.fetch_metadata(token_address)

    def get_new_tokens(self, exchange_name="PumpFun"):
        return self.new_tokens_api.get_new_tokens(exchange_name)