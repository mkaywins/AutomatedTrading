import pandas as pd
from pandas_datareader import data


# Fetch daily data for 4 years, for 7 major currency pairs
TRADING_INSTRUMENT = 'CADUSD=X'
SYMBOLS = ['AUDUSD=X', 'GBPUSD=X', 'CADUSD=X', 'CHFUSD=X', 'EURUSD=X', 'JPYUSD=X', 'NZDUSD=X']
START_DATE = '2014-01-01'
END_DATE = '2018-01-01'

# DataSeries for each currency
symbols_data = {}
for symbol in SYMBOLS:
  SRC_DATA_FILENAME = symbol + '_data.pkl'

  try:
    data1 = pd.read_pickle(SRC_DATA_FILENAME)
  except FileNotFoundError:
    data1 = data.DataReader(symbol, 'yahoo', START_DATE, END_DATE)
    data1.to_pickle(SRC_DATA_FILENAME)

  symbols_data[symbol] = data1

# Visualize prices for currency to inspect relationship between them
import matplotlib.pyplot as plt
import numpy as np
from itertools import cycle

cycol = cycle('bgrcmky')

price_data = pd.DataFrame()
for symbol in SYMBOLS:
  multiplier = 1.0
  if symbol == 'JPYUSD=X':
    multiplier = 100.0

  label = symbol + ' ClosePrice'
  price_data = price_data.assign(label=pd.Series(symbols_data[symbol]['Close'] * multiplier, index=symbols_data[symbol].index))
  ax = price_data['label'].plot(color=next(cycol), lw=2., label=label)
plt.xlabel('Date', fontsize=18)
plt.ylabel('Scaled Price', fontsize=18)
plt.legend(prop={'size': 18})
plt.show()

