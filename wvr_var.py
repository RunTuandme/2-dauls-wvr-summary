from wvrfname import get_wvr_file
from wvrpd import wvrfile_to_df
from datelist import datelist
import numpy as np
import pandas as pd
from tqdm import tqdm

def win_var(windowsize: int, windata: list):
    
    if len(windata) < windowsize:
        raise ValueError('Can\'t move for oversized window.')

    windows = [windata[i:i+windowsize] for i in range(0, len(windata), windowsize)]

    var_list = []
    for i in windows:
        var = np.std(i, ddof=1)
        var_list.append(var)

    return var_list

    
if __name__ == '__main__':

    ds = '20150801'
    de = '20200330'

    for date in tqdm(datelist(ds, de)):
        
        try:
            wvrfile = get_wvr_file(date)
            wvr_df = wvrfile_to_df(wvrfile)
        except:
            print(date + ' file wrong')
            continue

        total_delay = wvr_df['总延迟(m)']
        try:
            var_list = win_var(3600, total_delay)
        except:
            print(date + ' file lack of data')
            continue

        top_varlist =  pd.Series(var_list)
        btm_stats = top_varlist.describe()
        pd.concat([top_varlist, btm_stats]).to_frame().to_csv('../Estimate/variance_stat/wvr/' + date + '.csv' )
