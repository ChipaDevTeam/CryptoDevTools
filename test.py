from CryptoDevTools.solana import SolanaDataClient

def main():
    data_client = SolanaDataClient()

    # Example token address (replace with a valid Solana token address)
    token_address = "F9Lw3ki3hJ7PF9HQXsBzoY8GyE6sPoEZZdXJBsTTD2rk"
    metadata = data_client.getTokenMetadata(token_address)
    print("Token Metadata:", metadata)

if __name__ == "__main__":
    main()