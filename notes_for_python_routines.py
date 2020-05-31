
# Python packages to perform linear regression:

# 1. statsmodel

import statsmodels.api as sm
df = sm.add_constant(df)      # add ONES (intercept)
sm.OLS(y, x).fit()

# 2. numpy

np.polyfit(x, y, deg = 1)

# 3. pandas

pd.ols(y, x)

# 4. scipy

from scipy import stats
stats.linregress(x, y)





df = df.dropna() # --> drop NA from df with pct_changes:
fit = sm.OLS(df['stock1'], df[['const','stock2']]).fit()
print(fit.summary())

