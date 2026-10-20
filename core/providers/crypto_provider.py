import requests

class CryptoProvider:
    """
    Provider Class responsible ONLY for external API communication.
    Adheres to the Single Responsibility Principle (SRP).
    """
    def __init__(self):
        self.url = "https://coingecko.com"

    def fetch_raw_data(self) -> dict:
        """
        Fetches raw JSON payload from CoinGecko.
        Returns a dictionary or raises an exception if the network fails.
        """
        try:
            response = requests.get(self.url, timeout=10)
            # Automatically raises an HTTPError if the response code is 4xx or 5xx
            response.raise_for_status() 
            return response.json()
        except requests.RequestException as e:
            print(f"[ERROR] Network communication failed: {e}")
            raise e
