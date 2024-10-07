import requests


def fetch_stock_data(symbol: str, mult: int, span: str, start_dt: str, end_dt: str):
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{mult}/{span}/{start_dt}/{end_dt}"
    params = {
        'limit': 50000,
        'apiKey': 'kJePWMLyID8d8KxEU6LFLZP8zw7F8zmU'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()
