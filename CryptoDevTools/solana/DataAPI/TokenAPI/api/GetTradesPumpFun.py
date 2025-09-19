from .exchanges.pumpfun import PumpFunAPI

class GetTradesPumpFun:
    def __init__(self):
        self.pumpfun_api = PumpFunAPI()
    
    def get_trades(self, token_address, limit=100, cursor=0, minSolAmount=0):
        """
        Fetches recent trades for a specific token from the PumpFun API.

        Args:
            token_address (str): The Solana token address.
        Returns:
            dict: JSON response containing trades data
        """
        return self.pumpfun_api.get_trades(token_address, limit, cursor, minSolAmount)