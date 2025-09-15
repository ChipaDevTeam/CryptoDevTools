import requests
from CryptoDevTools.constants import DefaultData

class GetTokenMetadata:
    def __init__(self):
        self.url = DefaultData.HELIUS_RPC
    def fetch_metadata(self, token_address):
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getAsset",
            "params": {
                "id": token_address
            }
        }
        response = requests.post(self.url, json=payload, headers=headers)
        return response.json()