#Read in individual cases of nCov2019 from https://docs.google.com/spreadsheets/d/1itaohdPiAeniCXNlntNztZ_oRvjh0HsGuJXUJWET008/edit?usp=sharing
# (url set by config.gspread_url)

from utils import gspread_obj
from config import credentials_google, gspread_url   #get google API credentials
from feather import read_dataframe, write_dataframe

# Read in individual cases of nCov2019 from gspread_url
gc = gspread_obj()
gc.login(credentials_google)
gc.get_sheets(gspread_url)
df = gc.merge_sheets()
df.sort_values(['date_confirmation', 'country', 'city', 'ID'], axis=0, ascending=True, inplace=True)

# Save unprocessed df to a feather format to be compatible with R
write_dataframe(df, 'data/df_raw.feather')
#combined_dat = read_dataframe('data/combined_dat.feather')

