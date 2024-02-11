from datetime import date
from data_fetcher_FMP import fetch_stock_data
import data_analyze

def main():
  stock_symbols = {
    '8035.T': 'Tokyo Electron Limited', #東京エレクトロン
    # '6857.T': 'Advantest Corporation', #アドバンテスト
    # '7735.T': 'SCREEN Holdings Co., Ltd.', #スクリーンホールディングス
    # '7729.T': 'Tokyo Seimitsu Co., Ltd.', #東京精密
    # '6146.T': 'DISCO Inc.', #ディスコ
    # '7203.T': 'Toyota Motor Corporation', #トヨタ自動車
    # '9433.T': 'KDDI Corporation', # KDDI
    # '6594.T': 'Nidec Corporation', # 日本電産
    # '7936.T': 'Asics Corporation', # アシックス
    # '9984.T': 'SoftBank Group Corp.', # ソフトバンクグループ
    # '8233.T': 'Takashimaya Company, Limited', # 高島屋
    # '9201.T': 'Japan Airlines Co., Ltd.', # 日本航空
  }

  from_date = '2023-04-01'
  to_date = date.today().strftime('%Y-%m-%d')

  for symbol, name in stock_symbols.items():
    print(f"Fetching data for {name} ({symbol})...")
    data = fetch_stock_data(symbol, from_date, to_date)
    if data is not None:
      df = data_analyze.convert_to_dataframe(data)
      print(df)
      data_analyze.plot_stock_price(df, name)
    else:
      print(f"No data available for {name} ({symbol}).")

if __name__ == "__main__":
  main()
