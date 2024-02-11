from dotenv import load_dotenv
import os
import requests

def fetch_stock_data(symbol, from_date, to_date):
  load_dotenv()  # .envファイルから環境変数を読み込む
  api_key = os.getenv('API_KEY')

  url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={from_date}&to={to_date}&apikey={api_key}"
  response = requests.get(url)

  if response.status_code == 200:
    return response.json()
  else:
    print(f"Failed to fetch data for {symbol}. HTTP Status Code: {response.status_code}")
    return None
