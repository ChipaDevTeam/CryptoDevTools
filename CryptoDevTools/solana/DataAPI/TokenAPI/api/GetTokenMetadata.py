import requests
from CryptoDevTools.constants import DefaultData

class GetTokenMetadata:
    def __init__(self, rpc_url=None):
        self.url = rpc_url if rpc_url else DefaultData.HELIUS_RPC
        self.backup_url = DefaultData.DEFAULT_SOLANA_RPC

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
        
        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            if 'result' in data:
                return data
        except Exception as e:
            print(f"Primary RPC failed for metadata: {e}")

        # Fallback (Note: Standard RPC usually doesn't support getAsset, but some might)
        # If getAsset fails, we could try getAccountInfo and parse, but for now just return error or empty
        print("Metadata fetch failed or not supported by RPC")
        return {}