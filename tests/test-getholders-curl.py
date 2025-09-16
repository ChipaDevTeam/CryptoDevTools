import requests
import json

# Headers from your cURL command
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru=q=0.5',
    'content-type': 'application/json',
    'if-none-match': 'W/"44fa-N6htMs4URtCVfn6Km8Lbz24bc+g"',
    'origin': 'https://pump.fun',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Opera GX";v="121", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0',
}

# The target URL, including the specific coin address
url = 'https://advanced-api-v2.pump.fun/coins/top-holders-and-sol-balance/HxmUkRirJuvoF8dEt74UyXUK7NAs6xtByxHLcSBipump'

try:
    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check for a '304 Not Modified' status, which can result from the 'if-none-match' header
    if response.status_code == 304:
        print(f"Status Code: {response.status_code} (Not Modified)")
        print("Content has not changed since the last request.")
    else:
        # For any other status, raise an error if it's a client or server error (4xx or 5xx)
        response.raise_for_status()

        # Print the status code and the JSON response
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        
        # Pretty-print the JSON content for readability
        print(json.dumps(response.json(), indent=2))

        with open('tests/sample-output-pumpfun-holders.json', 'w') as f:
            json.dump(response.json(), f, indent=2)

except requests.exceptions.RequestException as e:
    print(f"A network error occurred: {e}")
except json.JSONDecodeError:
    print("Failed to decode JSON from the response.")
    print(f"Response Text: {response.text}")