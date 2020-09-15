import pandas as pd
from wreader import wvrfile
import matplotlib.pyplot as plt
import datetime
import os

def find_first_txt(pathdir: str) -> str:
    for i in os.listdir(pathdir):
        if i[-4:] == '.txt':
            return i
    return None

def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y%m%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y%m%d")
    return dates

def SwitchDate(date: str) -> str:
    year = date[:4]
    month = str(int(date[4:6]))
    day = str(int(date[6:]))
    return year + '-' + month + '-' + day

def SwitchTemper(F: float) -> float:
    """ (F -> K) """
    t = (F - 32) * 5 / 9
    K = t + 273.15
    return K

def t2s(t: str) -> float:
    if 'AM' in t:
        t = t[:-3]
        h,m = t.strip().split(":")
        if float(h) == 12:
            h = '0'
        return float(h) * 3600 + float(m) * 60
    if 'PM' in t:
        t = t[:-3]
        h,m = t.strip().split(":")
        if '12' in t:
            h = '0'
        return (float(h)+12) * 3600 + float(m) * 60
    
ds = '20180101'
de = '20180101'

for i in dateRange(ds, de):
    wvrdir = '../RawDatas/WVR_raw_data/' + i + '/'
    aimfile = find_first_txt(wvrdir)
    wf = wvrfile(wvrdir + aimfile)
    T = wf.T0()
    RHO = wf.e() * 100
    wvr_time = wf.Time()

    df = pd.read_csv('../RawDatas/weather_data/' + SwitchDate(i) + '.csv')
    dtime = [t2s(a) for a in df['Time'].tolist()]
    dT = [SwitchTemper(float(a[:-1])) for a in df['Temperature'].tolist()]
    dRHO = [float(a[:-1]) for a in df['Humidity'].tolist()]

    plt.cla()
    plt.plot(wvr_time, T, label='WVR')
    plt.scatter(dtime, dT, label='wt', color='#ff7f0e')
    plt.legend()
    plt.savefig('../Estimate/weatherpara_cmp/'+i+'.png', dpi=500)