import requests

class CryptoProvider:
    """
    Provider Class responsible ONLY for external API communication.
    Adheres to the Single Responsibility Principle (SRP).
    """
    def __init__(self):
        self.url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    def fetch_raw_data(self) -> dict:
        """
        Fetches raw JSON payload from CoinGecko.
        Returns a dictionary or raises an exception if the network fails.
        """
        try:
            response = requests.get(self.url, headers=self.headers)
            # Automatically raises an HTTPError if the response code is 4xx or 5xx
            response.raise_for_status() 
            return response.json()
        except requests.RequestException as e:
            print(f"[ERROR] Network communication failed: {e}")
            raise e
