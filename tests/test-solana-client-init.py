from CryptoDevTools.solana import SolanaClient

def main():
    rpc_url = "https://api.mainnet-beta.solana.com"
    client = SolanaClient(rpc_url)

    # Example account (replace with a valid Solana account address)
    account = "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh"
    account_info = client.getAccountInfo(account)
    balance_info = client.getBalance(account)
    print("Account Info:", account_info)
    print("Balance Info:", balance_info)

if __name__ == "__main__":
    main()