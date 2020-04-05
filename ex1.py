
from pandas_datareader import data
start_date = '2014-01-01'
end_date = '2018-01-01'
goog_data = data.DataReader('GOOG', 'yahoo', start_date, end_date)

#import some important modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

goog_data_signal = pd.DataFrame(index=goog_data.index)
goog_data_signal['price'] = goog_data['Adj Close']
goog_data_signal['daily_difference'] = goog_data_signal['price'].diff()
goog_data_signal['signal'] = 0.0
goog_data_signal['signal'] = np.where(goog_data_signal['daily_difference'] > 0, 1.0, 0.0)
goog_data_signal['positions'] = goog_data_signal['signal'].diff()


fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Google price in $')
goog_data_signal['price'].plot(ax=ax1, color='b', lw=2.)


ax1.plot(goog_data_signal.loc[goog_data_signal.positions == 1.0].index,
         goog_data_signal.price[goog_data_signal.positions == 1.0],
         '^', markersize=5, color='green')

ax1.plot(goog_data_signal.loc[goog_data_signal.positions == -1.0].index,
         goog_data_signal.price[goog_data_signal.positions == -1.0],
         'v', markersize=5, color='red')



initial_capital = float(1000.0)

positions = pd.DataFrame(index = goog_data_signal.index).fillna(0.0)
portfolio = pd.DataFrame(index = goog_data_signal.index).fillna(0.0)

positions['GOOG'] = goog_data_signal['signal']


# stores the amount of the position ' 1/0 x price' in the portfolio-df
portfolio['positions'] = (positions.multiply(goog_data_signal['price'], axis = 0)) # axis = 0 stands for inedx-wise multiplication - every index is multiplied as opposed to every column

# like before we calculate the positions (.diff()) -> 'position (1/0/-1) x price' - the amount is positive wehn we buy
# (+1 * price) and therefore is substracted from the initial capital (since we buy something)
# for short (-1) vice verca - it gets added 
portfolio['cash'] = initial_capital - (positions.diff().multiply(goog_data_signal['price'], axis = 0)).cumsum()

# calculate total as the sum of positions and cash
portfolio['total'] = portfolio['cash'] + portfolio['positions']


portfolio.plot()

fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel = 'Protfolio Value in $')
portfolio['total'].plot(ax=ax1, lw=2.)
ax1.plot(portfolio.loc[goog_data_signal.positions == 1.0].index,portfolio.total[goog_data_signal.positions == 1.0],
	'^', markersize=4, color='m')
ax1.plot(portfolio.loc[goog_data_signal.positions == -1.0].index,portfolio.total[goog_data_signal.positions == -1.0],
	'v', markersize=4, color='k')
plt.show()


