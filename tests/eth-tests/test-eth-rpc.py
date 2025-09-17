import requests

def main():
    rpc_url = "https://eth.llamarpc.com"

    payload = {
        "id":1,
        "jsonrpc":"2.0",
        "method":"eth_getBalance",
        "params":[
            "0xc94770007dda54cF92009BFF0dE90c06F603a09f",
            "latest"
        ]
    }

    response = requests.post(rpc_url, json=payload)
    data = int(response.json()["result"], 16)
    print(f"Balance: {data} wei")

if __name__ == "__main__":
    main()