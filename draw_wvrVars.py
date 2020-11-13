from tqdm import tqdm
from datetime import datetime
from datelist import datelist
import matplotlib.pyplot as plt

def get_mvdata(filename: str):
    with open(filename, 'r') as dealing_file:
        for line in dealing_file:
            if 'mean' in line:
                mean_var = line.strip().split(',')[1]
                break
        return float(mean_var)

if __name__ == '__main__':

    ds = '20150801'    # 起
    de = '20200330'    # 止

    wvr_vars_stats = []
    gps_vars_stats = []

    dates = []

    for date in tqdm(datelist(ds, de)):
        try:
            wvrdata_var = get_mvdata('../Estimate/variance_stat/wvr/' + date + '.csv')
            gpsdata_var = get_mvdata('../Estimate/variance_stat/gps/' + date + '.csv')
            if wvrdata_var > 1000:
                continue
            else:
                wvr_vars_stats.append(wvrdata_var)
                gps_vars_stats.append(gpsdata_var)
        except:
            print(date + ' file wrong')
            continue
        else:
            dates.append(datetime.strptime(date, '%Y%m%d'))

    plt.plot(dates, wvr_vars_stats)
    plt.plot(dates, gps_vars_stats)
    plt.ylim(0, 50)
    plt.xticks(rotation=30)
    plt.show()
    