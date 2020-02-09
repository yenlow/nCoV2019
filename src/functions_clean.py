import numpy as np
import re

def clean_age(x):
    # strip white spaces
    x = re.sub(r"\s", "", x)
    # change 20s to 25
    x = re.sub(r"\ds$", "5", x)

    # convert age ranges dd-dd to the mid value
    if re.match(r"\d+-\d+", x):
        x = np.floor(np.asarray(x.split('-'), dtype=int).mean())
    else:
        # drop anything that's not a number or period
        x = re.sub(r"[^\d.]", "", x)
    try:
        return int(x)
    except:
        return None


def clean_float(x):
    if isinstance(x,str):
        # strip non-digits and .
        x = re.sub(r"[^\d|.|-]", "", x)
    try:
        return float(x)
    except:
        return None


def clean_bin(x, missing=None):
    if isinstance(x,str):
        # strip non-digits and .
        x = re.sub(r"\s", "", x)
        if x not in ['0','1']:
            return missing
    try:
        return int(x)
    except:
        return None


def recode(s,mapdict,inplace=False):
    return s.replace(mapdict, inplace=inplace)


def recode_bin(s,mapdict,inplace=False, missing=None):
    s1 = s.replace(mapdict, inplace=inplace)
    s1[~(s1.isin([0,1]))] = missing
    return s1