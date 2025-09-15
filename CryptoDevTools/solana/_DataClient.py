from .DataAPI.TokenAPI.TokenApi import TokenAPI

class SolanaDataClient:
    def __init__(self):
        self.token_api = TokenAPI()
    def getTokenMetadata(self, token_address):
        return self.token_api.get_token_metadata(token_address)