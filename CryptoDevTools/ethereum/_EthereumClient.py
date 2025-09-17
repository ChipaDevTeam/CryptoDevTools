import requests

from CryptoDevTools.constants import DefaultData
from CryptoDevTools.models.ethereum.EthBlockchainData import GetBalanceResponse

class EthereumClient:
    def __init__(self):
        self.rpc_url = DefaultData.DEFAULT_ETHEREUM_RPC

    def get_balance(self, address: str) -> int:
        payload = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "eth_getBalance",
            "params": [address, "latest"]
        }
        response = requests.post(self.rpc_url, json=payload)
        response.raise_for_status()
        data = int(response.json()["result"], 16)
        GetBalanceResponse.ether = data / 10**18
        GetBalanceResponse.wei = data
        return GetBalanceResponse