from gpsfname import get_gps_file
from gpspd import gpsfile_to_df
from datelist import datelist
import numpy as np
import pandas as pd

def win_var(windowsize: int, windata: list):
    
    if len(windata) < windowsize:
        raise ValueError('Can\'t move for oversized window.')

    windows = [windata[i:i+windowsize] for i in range(0, len(windata), windowsize)]

    var_list = []
    for i in windows:
        var = np.var(i)
        var_list.append(var)

    return var_list

    
if __name__ == '__main__':

    ds = '20150801'
    de = '20200330'

    for date in datelist(ds, de):
        
        try:
            gpsfile = get_gps_file(date)
            gpd_df = gpsfile_to_df(gpsfile)
        except:
            print(date + ' file wrong')
            continue

        total_delay = gpd_df['TROTOT']
        var_list = win_var(6, total_delay)

        top_varlist =  pd.Series(var_list)
        btm_stats = top_varlist.describe()
        pd.concat([top_varlist, btm_stats]).to_frame().to_csv('../Estimate/variance_stat/gps/' + date + '.csv' )
