from CryptoDevTools.solana import SolanaDataClient

def main():
    data_client = SolanaDataClient()

    new_tokens = data_client.getNewTokensByExchange()
    print("New Tokens from Exchange:", new_tokens)

if __name__ == "__main__":
    main()