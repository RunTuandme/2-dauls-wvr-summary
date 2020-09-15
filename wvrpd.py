# 建立读取的wvr pandas dataframe对象

import pandas as pd
import wreader
from datetime import datetime, timedelta

def wvrfile_to_df(filepath: str):
    cut = filepath.split('/')
    date_str = cut[3]

    date_pdtime = datetime.strptime(date_str, '%Y%m%d')
    wvrf = wreader.wvrfile(filepath)

    wvr_dict = {
        '时间':         [date_pdtime + timedelta(seconds = m) for m in wvrf.Time()],
        '湿延迟(mm)':   wvrf.ZWD(),
        '总延迟(m)':    wvrf.ZTD()
    }
    wvr_dataframe = pd.DataFrame(wvr_dict)
    
    return wvr_dataframe