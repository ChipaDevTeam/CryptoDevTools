from CryptoDevTools.solana import SolanaDataClient

def main():
    data_client = SolanaDataClient()

    graduated_tokens = data_client.token_api.get_graduated_tokens(sortBy="creationTime")
    print("Graduated Tokens from PumpFun:", graduated_tokens)

if __name__ == "__main__":
    main()