from CryptoDevTools.solana import SolanaDataClient

def main():
    data_client = SolanaDataClient()

    holders_tokens = data_client.getHoldersTokens(token_address="F9Lw3ki3hJ7PF9HQXsBzoY8GyE6sPoEZZdXJBsTTD2rk")
    print("Holders Tokens from PumpFun:", holders_tokens)

if __name__ == "__main__":
    main()