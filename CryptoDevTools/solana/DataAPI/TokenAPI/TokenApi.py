from CryptoDevTools.constants import GlobalConstants
from .api.GetTokenMetadata import GetTokenMetadata
from .api.GetNewTokensByExchange import GetNewTokensByExchange
from .api.GetGraduatedTokensPumpFun import GetGraduatedTokensPumpFun
from .api.GetHoldersTokensPumpFun import GetHoldersTokensPumpFun

class TokenAPI:
    def __init__(self):
        self.metadata_api = GetTokenMetadata()
        self.new_tokens_api = GetNewTokensByExchange()
        self.graduated_tokens_api = GetGraduatedTokensPumpFun()
        self.holders_api = GetHoldersTokensPumpFun()

    def get_token_metadata(self, token_address):
        return self.metadata_api.fetch_metadata(token_address)

    def get_new_tokens(self, exchange_name="PumpFun"):
        return self.new_tokens_api.get_new_tokens(exchange_name)

    def get_graduated_tokens(self, sortBy=GlobalConstants.GRADUATED_DEFAULT_SORT):
        return self.graduated_tokens_api.get_graduated_tokens(sortBy=sortBy)
    def get_holders_tokens(self, token_address):
        return self.holders_api.get_holders_tokens(token_address)