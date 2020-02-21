# Config params
import os

#for Google API
gspread_url = 'https://docs.google.com/spreadsheets/d/1itaohdPiAeniCXNlntNztZ_oRvjh0HsGuJXUJWET008/edit?usp=sharing'
credentials_google = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

#for Github v3 API
credentials_github = os.environ.get("GITHUB_ACCESS_TOKEN")
