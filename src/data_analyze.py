import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import numpy as np


def convert_to_dataframe(data):
  pd.set_option('display.max_columns', None)
  df = pd.DataFrame(data['historical'])
  df_filtered = df[['date', 'high', 'low', 'open', 'close', 'adjClose', 'volume']]
  df_filtered['date'] = pd.to_datetime(df_filtered['date'])
  df_filtered.set_index('date', inplace=True)
  df_filtered = df_filtered.sort_index()
  return df_filtered

# ＋2σ(標準偏差)と－2σのラインを計算する
def calculate_bollinger_bands(df, window=20, no_of_std=2):
  rolling_mean = df['close'].rolling(window=window).mean()
  rolling_std = df['close'].rolling(window=window).std()

  df['Bollinger High'] = rolling_mean + (rolling_std * no_of_std)
  df['Bollinger Low'] = rolling_mean - (rolling_std * no_of_std)

def calculate_macd_histogram(df):
  # MACDヒストグラムの計算 (MACD - MACDシグナル)
  df['MACD_histogram'] = df['MACD'] - df['MACD_signal']

def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
  # 短期EMAと長期EMAの計算
  df['EMA_short'] = df['close'].ewm(span=short_period, adjust=False).mean()
  df['EMA_long'] = df['close'].ewm(span=long_period, adjust=False).mean()
  # MACDの計算
  df['MACD'] = df['EMA_short'] - df['EMA_long']
  # MACDのシグナル線の計算
  df['MACD_signal'] = df['MACD'].ewm(span=signal_period, adjust=False).mean()

def calculate_rsi(df, periods):
    delta = df['close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()

    RS = gain / loss
    RSI = 100 - (100 / (1 + RS))

    return RSI

def plot_stock_price(df_filtered, company_name):
  # RSIの計算
  df_filtered['RSI14'] = calculate_rsi(df_filtered, 14)
  df_filtered['RSI25'] = calculate_rsi(df_filtered, 25)
  df_filtered['RSI75'] = calculate_rsi(df_filtered, 75)

  # MACDの計算関数を呼び出し
  calculate_macd(df_filtered)

  # MACDヒストグラムの計算
  calculate_macd_histogram(df_filtered)

  # MACDヒストグラムの追加プロット設定
  macd_histogram_plot = mpf.make_addplot(df_filtered['MACD_histogram'], panel=3, type='bar', color='gray', alpha=0.3, width=0.8)

  # ボリンジャーバンドの計算
  calculate_bollinger_bands(df_filtered)

  # 移動平均線の設定
  sma05 = mpf.make_addplot(df_filtered['close'].rolling(window=5).mean(), color='r', label='SMA[5d]')
  sma25 = mpf.make_addplot(df_filtered['close'].rolling(window=25).mean(), color='g', label='SMA[25d]')
  sma50 = mpf.make_addplot(df_filtered['close'].rolling(window=50).mean(), color='b', label='SMA[50d]')

  # 各期間のRSIの追加プロット設定
  rsi14_plot = mpf.make_addplot(df_filtered['RSI14'], panel=2, color='purple', ylabel='RSI (14)')
  rsi25_plot = mpf.make_addplot(df_filtered['RSI25'], panel=2, color='orange', ylabel='RSI (25)')
  rsi75_plot = mpf.make_addplot(df_filtered['RSI75'], panel=2, color='green', ylabel='RSI (75)')

  # MACDとシグナル線の追加プロット
  macd_plot = mpf.make_addplot(df_filtered['MACD'], panel=3, color='blue', ylabel='MACD')
  macd_signal_plot = mpf.make_addplot(df_filtered['MACD_signal'], panel=3, color='red')

  bollinger_high = mpf.make_addplot(df_filtered['Bollinger High'], color='cyan')
  bollinger_low = mpf.make_addplot(df_filtered['Bollinger Low'], color='cyan')

  # 既存のaddplotにヒストグラムの追加プロットを追加
  addplots = [sma05, sma25, sma50, bollinger_high, bollinger_low, rsi14_plot, rsi25_plot, rsi75_plot, macd_plot, macd_signal_plot, macd_histogram_plot]

  mpf.plot(
              df_filtered,
              type='candle',
              style='charles',
              addplot=addplots,
              title=company_name,
              ylabel='Price',
              volume=True,
              ylabel_lower='Volume',
              panel_ratios=(2, 1, 1, 1), # 株価チャート、出来高チャート、RSIチャートの高さ比
              figsize=(20, 10), # チャートのサイズ
              figratio=(16, 9), # チャートのサイズ比
              mav=(5,25,50) # 移動平均線の期間
  )

  plt.show()
