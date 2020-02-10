from feather import read_dataframe, write_dataframe

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Read cleaned line list df.feather (after data_download.py and data_clean.py)
df = read_dataframe('data/df.feather')

#Charting
for c in ['outcome','male','wuhan(0)_not_wuhan(1)','country','reported_market_exposure','sequence_available']:
    df[c].value_counts().plot('barh', logx=True, title=c)
    plt.show()


# Compute cumulative cases over time (also grouped by outcome)
df_cum = df[['date_confirmation','outcome']]
df_cum = df_cum.set_index(['date_confirmation','outcome']).sort_index(inplace=False)

# Method 1: using cumcount()
df_cum_sum = df_cum.groupby(['date_confirmation','outcome']).cumcount()

cases_by_date = df_cum_sum.groupby('date_confirmation').max()
cumcases_by_date = cases_by_date.cumsum()
cases_by_outcome = df_cum_sum.groupby(['date_confirmation','outcome']).max()
cumcases_by_outcome = cases_by_outcome.cumsum()

# Method 2: using explicit counter and then cumsum
df_cum['counter'] =1
cumcases_by_date = df_cum[['counter']].cumsum().groupby('date_confirmation').max()
cumcases_by_outcome = df_cum[['counter']].groupby('outcome').cumsum().groupby(['date_confirmation','outcome']).max()

# Plot cumulative cases (total and overlaid with outcome totals)
ax = cumcases_by_date.plot(kind='line', rot=45, title="Cases over time")
cumcases_by_outcome.unstack('outcome').plot(ax=ax, kind='line', rot=45)
plt.show()