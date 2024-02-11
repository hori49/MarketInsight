from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from yahooquery import Ticker

start_date = '2024-01-01'
end_date = '2024-1-15'

ticker = Ticker('AAPL')
data = ticker.history(start=start_date, end=end_date)

print(data)
