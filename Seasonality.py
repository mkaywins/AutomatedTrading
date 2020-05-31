import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data

start_date = '2001-01-01'
end_date = '2018-01-01'
SRC_DATA_FILENAME = 'goog_data_large.pkl'

try:
    goog_data = pd.read_pickle(SRC_DATA_FILENAME)
    print('File data found')
except FileNotFoundError:
    print('file not found - downloading')
    goog_data = data.DataReader('GOOG', 'yahoo', start_date, end_date)
    goog_data.to_pickle(SRC_DATA_FILENAME)

goog_monthly_return = goog_data['Adj Close'].pct_change().groupby([goog_data['Adj Close'].index.year,
                                                                   goog_data['Adj Close'].index.month]).mean()
goog_monthly_return_list = []

for i in range(len(goog_monthly_return)):
    goog_monthly_return_list.append({
        'month': goog_monthly_return.index[i][1],
        'monthly_return': goog_monthly_return[i]
    })

goog_monthly_return_list = pd.DataFrame(goog_monthly_return_list, columns = ('month', 'monthly_return'))

goog_monthly_return_list.boxplot(column='monthly_return', by = 'month')

#ax = plt.gca()
#labels = [item.get_text() for item in ax.get_xticklabels()]
#labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
#ax.set_xticklabels(labels)
#plt.tick_params(axis='both', which= 'major', labelsize = 7)
#plt.title('GOOG Monthly return 2001-2018')
#plt.suptitle('')
#plt.show()

# convert into time series:


plt.figure()
ts = pd.DataFrame(goog_data['Adj Close']) 
ts.index = pd.to_datetime(ts.index)
ts['return'] = ts['Adj Close'].pct_change()
autocorrelation = ts['return'].autocorr()

print('Autocorrelation is: ', autocorrelation)