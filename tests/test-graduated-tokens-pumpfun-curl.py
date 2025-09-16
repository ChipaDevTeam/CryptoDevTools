import requests
import json

# The headers from your cURL command
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru;q=0.5',
    'if-none-match': 'W/"118d5-ED9gKVZ9glJ/xxswClXuEXNgMgI"',
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

# The target URL with query parameters
url = 'https://advanced-api-v2.pump.fun/coins/graduated?sortBy=creationTime'

try:
    # Make the GET request
    response = requests.get(url, headers=headers)

    # The 'If-None-Match' header may result in a 304 Not Modified status
    # if the content on the server hasn't changed.
    if response.status_code == 304:
        print(f"Status Code: {response.status_code} (Not Modified)")
        print("Content is unchanged.")
    else:
        # Raise an HTTPError for other bad status codes (4xx or 5xx)
        response.raise_for_status()

        # Print the status code and the JSON response
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        
        # Pretty-print the JSON content
        print(json.dumps(response.json(), indent=2))

        with open('tests/sample-output-pumpfun-graduated.json', 'w') as f:
            json.dump(response.json(), f, indent=2)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except json.JSONDecodeError:
    print("Failed to decode JSON from response.")
    print(f"Response Text: {response.text}")