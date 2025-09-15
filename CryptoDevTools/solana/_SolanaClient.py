import requests

from .helpers.LamportsToSol import LamportsToSol

class SolanaClient:
    def __init__(self, rpc_url):
        self.rpc_url = rpc_url

    def get_account_info(self, account):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getAccountInfo",
            "params": [account, {"encoding": "base64"}]
        }
        response = requests.post(self.rpc_url, json=payload)
        return response.json()
    def get_balance(self, account):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [account]
        }
        response = requests.post(self.rpc_url, json=payload)

        # process and return the balance information
        if response.status_code == 200:
            data = response.json()
            balance = data.get("result", {}).get("value", 0)
            return {"balance": LamportsToSol.convert(balance)}
        else:
            return {"error": "Failed to retrieve balance information"}