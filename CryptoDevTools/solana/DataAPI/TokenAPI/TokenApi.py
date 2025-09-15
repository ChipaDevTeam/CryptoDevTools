from .api.GetTokenMetadata import GetTokenMetadata

class TokenAPI:
    def __init__(self):
        self.metadata_api = GetTokenMetadata()
    def get_token_metadata(self, token_address):
        return self.metadata_api.fetch_metadata(token_address)