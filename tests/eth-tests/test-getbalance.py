from CryptoDevTools.ethereum import EthereumClient

def main():
    eth_client = EthereumClient()
    balance = eth_client.get_balance("0xc94770007dda54cF92009BFF0dE90c06F603a09f")
    print(f"Balance: {balance.ether} ETH")

if __name__ == "__main__":
    main()