import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from CryptoDevTools.solana._DataClient import SolanaDataClient
from CryptoDevTools.constants import GlobalConstants

def test_onchain_metadata():
    # Use a public RPC or the one in constants
    # client = SolanaDataClient(rpc_url="https://api.mainnet-beta.solana.com")
    client = SolanaDataClient() # Uses GlobalConstants.HELIUS_RPC if set, or default
    
    # Test Bonk
    mint = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
    print(f"Fetching metadata for {mint}...")
    
    metadata = client.getTokenMetadata(mint)
    
    if metadata:
        print("Metadata Fetched Successfully (On-Chain)!")
        print(f"ID: {metadata.id}")
        print(f"Name: {metadata.content['metadata']['name']}")
        print(f"Symbol: {metadata.content['metadata']['symbol']}")
        print(f"URI: {metadata.content['json_uri']}")
        print(f"Update Authority: {metadata.authorities['update_authority']}")
        print(f"Is Mutable: {metadata.mutable}")
        print(f"Primary Sale Happened: {metadata.royalty['primary_sale_happened']}")
        print(f"Seller Fee Basis Points: {metadata.royalty['basis_points']}")
        print(f"Creators: {metadata.creators}")
    else:
        print("Failed to fetch metadata.")

if __name__ == "__main__":
    test_onchain_metadata()
