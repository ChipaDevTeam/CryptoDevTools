from .exchanges.pumpfun import PumpFunAPI

class GetNewTokensByExchange:
    def __init__(self):
        self.pumpfun_api = PumpFunAPI()
    
    def get_new_tokens(self, exchange_name="PumpFun"):
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
        if exchange_name == "PumpFun":
            return self.pumpfun_api.get_runners()
        else:
            raise ValueError(f"Exchange '{exchange_name}' is not supported.")