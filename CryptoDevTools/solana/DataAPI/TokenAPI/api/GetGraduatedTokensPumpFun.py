from .exchanges.pumpfun import PumpFunAPI
from CryptoDevTools.constants import GlobalConstants

class GetGraduatedTokensPumpFun:
    def __init__(self):
        self.pumpfun_api = PumpFunAPI()

    def get_graduated_tokens(self, sortBy=GlobalConstants.GRADUATED_DEFAULT_SORT):
        """
        Fetches graduated token data from the PumpFun API.

        Args:
            sortBy (str): The field to sort the results by. Default is "creationTime".

        Returns:
            dict: JSON response containing graduated token data
        """
        return self.pumpfun_api.get_graduated(sortBy=sortBy)