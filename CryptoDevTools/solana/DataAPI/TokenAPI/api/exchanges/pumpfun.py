import json
import requests

from CryptoDevTools.constants import GlobalConstants

class PumpFunAPI:
    def __init__(self):
        self.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6,ru;q=0.5',
            'priority': 'u=1, i',
            'referer': 'https://pump.fun/board',
            'sec-ch-ua': '"Opera GX";v="121", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 OPR/121.0.0.0',
        }
        self.cookies = {
            'cf_clearance': '5dmF64R6Qef6edZGfdAE_GXwSY3dd9C72kPoCL0m8CI-1758044770-1.2.1.1-WYOFtb6AMW.YLM5.luVY6LxOIYR0ylEJTDks4BdeXX9p6XynuRLTRQeiTxhzlwJ2A6WS.vkj9nmkQfg_N.AVtMyoeJA_156pSxoxxzFjCFJLk9niTY37ollrOx1o2jp2FwpN7Thh9SqrBHCbF1roWCuQC1qEaql4.f2xq0PoSMJ6XwH2vy_omO0goK_IyGgz_CeT8WgtTHlVDtuorZADEI8p37Y3u6zznIwRHnnNg20',
            '_ga': 'GA1.1.1573348401.1758044772',
            'intercom-id-w7scljv7': '55144242-72a2-406e-b6a9-69e02f966a6f',
            'intercom-session-w7scljv7': '',
            'intercom-device-id-w7scljv7': '6372a7fc-02ed-485a-b211-086b928421a8',
            '__cf_bm': 'H3pxzs7U39Y9yOryRaQH.BanszFzWBsXWDaDiBc7w6Q-1758044773-1.0.1.1-OIbD4qZXfrzvOgEmGAIxKFHi12Jgo2TwPHq4hBiJAWPfdTDrgd40xk4wSnDrTTdhNQKALm1a62CqkqQdjnL_wEiwjElOK_L4WRQFn.5eirE',
            '_cfuvid': 'K7QfhQdTyBsyPMhmTZlkRrYwMmVNHL4t_wKdBDKoHmw-1758044773145-0.0.1.1-604800000',
            '_ga_T65NVS2TQ6': 'GS2.1.s1758044771^$o1^$g0^$t1758044784^$j60^$l0^$h0',
            '_dd_s': 'aid=8fdcdeb8-74dd-4282-8d42-8d4e3c83ffa5^&logs=1^&id=d7bc9d98-7318-4d65-8814-3f05316779b8^&created=1758044771021^&expire=1758045686273^',
        }
        self.url = 'https://pump.fun/api/runners'
    
    def get_runners(self):
        """
        Fetches runner data from the PumpFun API.
        
        Returns:
            dict: JSON response containing runner data
            
        Raises:
            requests.exceptions.RequestException: For network-related errors
            requests.exceptions.HTTPError: For HTTP error responses
            ValueError: For invalid JSON responses
            Exception: For any other unexpected errors
        """
        try:
            response = requests.get(
                self.url, 
                headers=self.headers, 
                cookies=self.cookies,
                timeout=30  # Add timeout to prevent hanging
            )
            response.raise_for_status()  # Raise an error for bad responses
            
            # Validate that the response contains valid JSON
            try:
                json_data = response.json()
                return json_data
            except ValueError as e:
                raise ValueError(f"Invalid JSON response from API: {e}")
                
        except requests.exceptions.Timeout:
            raise requests.exceptions.RequestException("Request timed out after 30 seconds")
        except requests.exceptions.ConnectionError:
            raise requests.exceptions.RequestException("Failed to connect to PumpFun API")
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError(f"HTTP error occurred: {e.response.status_code} - {e.response.reason}")
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Request failed: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error occurred while fetching runners: {e}")
    def get_graduated(self, sortBy=GlobalConstants.GRADUATED_DEFAULT_SORT):
        """
        Fetches graduated token data from the PumpFun API.
        
        Returns:
            dict: JSON response containing graduated token data
        """

        if sortBy not in GlobalConstants.SORT_BY_OPTIONS:
            raise ValueError(f"Invalid sortBy value. Must be one of {GlobalConstants.SORT_BY_OPTIONS}")

        url = f'https://advanced-api-v2.pump.fun/coins/graduated?sortBy={sortBy}'

        try:
            # Make the GET request
            response = requests.get(url, headers=self.headers)

            # The 'If-None-Match' header may result in a 304 Not Modified status
            # if the content on the server hasn't changed.
            if response.status_code == 200:
                return response.json()
            if response.status_code == 304:
                return (f"Status Code: {response.status_code} (Not Modified)")
            else:
                # Raise an HTTPError for other bad status codes (4xx or 5xx)
                return response.raise_for_status()

        except requests.exceptions.RequestException as e:
            return (f"An error occurred: {e}")
        except json.JSONDecodeError:
            return (f"Failed to decode JSON from response.")
    
    def get_holders(self, token_address):
        """
        Fetches top holders and SOL balance for a specific token from the PumpFun API.

        Args:
            token_address (str): The Solana token address.
        Returns:
            dict: JSON response containing holders data
        """
        url = f'https://advanced-api-v2.pump.fun/coins/top-holders-and-sol-balance/{token_address}'

        try:
            # Make the GET request
            response = requests.get(url, headers=self.headers)

            # Check for a '304 Not Modified' status, which can result from the 'if-none-match' header
            if response.status_code == 200:
                return response.json()
            if response.status_code == 304:
                return (f"Status Code: {response.status_code} (Not Modified)")
            else:
                # For any other status, raise an error if it's a client or server error (4xx or 5xx)
                return response.raise_for_status()

        except requests.exceptions.RequestException as e:
            return (f"A network error occurred: {e}")
        except json.JSONDecodeError:
            return (f"Failed to decode JSON from the response.")
    def get_trades(self, token_address, limit=100, cursor=0, minSolAmount=0):
        """
        Fetches recent trades for a specific token from the PumpFun API.

        Args:
            token_address (str): The Solana token address.
        Returns:
            dict: JSON response containing trades data
        """

        # The target URL from the cURL command
        url = f"https://swap-api.pump.fun/v2/coins/{token_address}/trades"

        # The query parameters
        params = {
            'limit': limit,
            'cursor': cursor,
            'minSolAmount': minSolAmount
        }

        try:
            # Make the GET request with the headers and parameters
            response = requests.get(url, headers=self.headers, params=params)

            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as err:
            return (f"❌ HTTP Error: {err}")
        except requests.exceptions.RequestException as e:
            return (f"❌ An error occurred: {e}")
