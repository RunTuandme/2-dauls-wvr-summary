


import os

def get_wvr_file(date: str)-> str:

    # date: 20170101

    year = date[:4]
    month = date[4:6]
    day = date[-2:]

    filepath = '../RawDatas/WVR_raw_data/' + date

    files = os.listdir(filepath)
    for i in files:
        if os.path.splitext(i)[1] == ".txt":
            f = filepath + '/' + i

    return f