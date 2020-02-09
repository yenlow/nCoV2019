#Read in individual cases of nCov2019 from https://docs.google.com/spreadsheets/d/1itaohdPiAeniCXNlntNztZ_oRvjh0HsGuJXUJWET008/edit?usp=sharing
# (url set by config.gspread_url)

from feather import read_dataframe, write_dataframe
from functions_clean import *

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Read df.feather from gspread_url (see get_data.py)
df = read_dataframe('output/data/df.feather')
#combined_dat = read_dataframe('output/data/combined_dat.feather')

# get column data types
df.dtypes

col_date = list(filter(lambda x:'date' in x, df.columns))
col_admin = list(filter(lambda x:'admin' in x, df.columns))
col_float = ['age','latitude','longitude']
col_bin = ['wuhan(0)_not_wuhan(1)','chronic_disease_binary']   #sex',
col_cat = ['city','province','country','geo_resolution','location','lives_in_Wuhan',
           'outcome','reported_market_exposure','sequence_available','country_new']
col_str = col_admin + ['ID','chronic_disease','symptoms',
            'travel_history_location','source',
            'notes_for_discussion','additional_information']

# Clean numeric values
# Clean age
df.age.value_counts(dropna=False)
df.age = df.age.apply(clean_age)
df.age.value_counts(dropna=False)
df.age.hist(bins=100)
plt.show()

# Clean latitudes, longitudes
for c in ['latitude','longitude']:
    df[c] = df[c].apply(clean_float)
    print(df[c].value_counts(dropna=False))
    df[c].hist(bins=100)
    plt.show()

# Get freq counts for col_cat
for c in col_bin:
    print("Before cleaning:")
    print(df[c].value_counts())
    df[c] = df[c].apply(clean_bin, missing=0)
    print("After cleaning:")
    print(df[c].value_counts(dropna=False))
#    df[c].hist(bins=100)
#    plt.show()

df['male'] = recode_bin(df.sex, {"female": 0, "male": 1}, inplace=False, missing=None)
df.sex.value_counts(dropna=False)
df.male.value_counts(dropna=False)


### More cleaning