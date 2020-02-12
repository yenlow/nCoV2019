#Create a gspread class and extract the data from the sheets
#requires:
# 1. Google API credentials json_key file path
# 2. scope e.g. ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# 3. gspread_url e.g. 'https://docs.google.com/spreadsheets/d/1itaohdPiAeniCXNlntNztZ_oRvjh0HsGuJXUJWET008/edit?usp=sharing'

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from github import Github
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

class gspread_obj(object):
    """
    Create a google spreadsheet instance to download sheet(s) and merge them
    Requires spreadsheet url and Google API json key file

    Examples:
        >>>> gc = gspread_obj()

        >>>> gc.login('home/user/google_api_key.json')

        >>>> gc.get_sheets('https://docs.google.com/spreadsheets/d/1itaohdPiAeniCXNlntNztZ_oRvjh0HsGuJXUJWET008/edit?usp=sharing')

        >>>> df = gc.merge_sheets()

    """
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        self.client = None # gspread.Client object
        self.sheets = None

    def login(self, credentials_google: str):
        #set Google spreadsheet credentials
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_google, self.scope)
        self.client = gspread.authorize(credentials)

    def get_sheets(self, gspread_url: str):
        #Get Google sheet instance
        wks = self.client.open_by_url(gspread_url)
        self.sheets = wks.worksheets()

    def merge_sheets(self):
        if self.sheets is None:
            print('No sheets are found!')
            df = None

        elif len(self.sheets)==1:
            data = self.sheets[0].get_all_values()
            header = data.pop(0)
            df = pd.DataFrame(data, columns=header)

        elif len(self.sheets)>1:
            #read all the sheets
            df_list = []
            for s in self.sheets:
                data = s.get_all_values()
                header = data.pop(0)
                df = pd.DataFrame(data, columns=header)
                df_list.append(df)
            df = pd.concat(df_list, axis=0, join='outer', sort=False)

        else:
            print("self.sheets must be a list of sheet(s)!")
            df = None

        if df is not None:
            print("Columns: ", df.columns)
            print("{} Rows x {} Columns".format(df.shape[0],df.shape[1]))
        return df


def get_rawfile_from_github(raw_url: str, outdir: str = None) -> None:
    """
    Download raw script from github. URL should point to the raw script off github

    Args:
        raw_url (str): url of raw script off github (should be publicly accessible)
        outdir (str): directory for saving the script; defaults to current path otherwise
    Example:
        >>> get_rawfile_from_github('https://raw.githubusercontent.com/beoutbreakprepared/nCoV2019/master/entry-checker.R','other_authors')

    """
    from wget import download, filename_from_url
    filename = filename_from_url(raw_url)
    if outdir:
        outpath = outdir + '/' + filename
    else:
        outpath = filename
    download(raw_url,outpath)


class gh_obj(object):
    """
    Creates a github instance to download file from repo via the Github V3 API
    This requires Github V3 API access token
    See https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line

    Examples:
        >>>gh = gh_obj("jameshay218/case_to_infection")

        >>>gh.login(<accesstoken>)

        >>>gh.get_file(file="code/analysis_functions.R", outdir="other_authors")
    """
    def __init__(self):
        self.instance = None

    def login(self, credentials_github: str):
        self.instance = Github(credentials_github)

    def get_file(self, repo: str, file: str, outdir: str = None) -> None:
        if not repo:
            raise ValueError('Please provide repo as str')

        repoinstance = self.instance.get_repo(repo)
        contents = repoinstance.get_contents(file)

        if outdir:
            outpath = outdir + "/" + contents.name
        else:
            outpath = contents.name

        f = open(outpath, "wb")
        f.write(contents.decoded_content)
        f.close()
