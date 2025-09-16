from .exchanges.pumpfun import PumpFunAPI

class GetHoldersTokensPumpFun:
    def __init__(self):
        self.pumpfun_api = PumpFunAPI()

    def get_holders_tokens(self, token_address):
        """
        Fetches new token data from the Specific exchange API.
        
        Returns:
            dict: JSON response containing new token data
            
        Raises:
            requests.exceptions.RequestException: For network-related errors
            requests.exceptions.HTTPError: For HTTP error responses
            ValueError: For invalid JSON responses
            Exception: For any other unexpected errors
            
        """
        return self.pumpfun_api.get_holders(token_address)