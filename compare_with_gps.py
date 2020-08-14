import os
import matplotlib.pyplot as plt
from tqdm import tqdm
from numpy import mean
from datetime import datetime,timedelta
from matplotlib.ticker import AutoMinorLocator
import wreader

WVR_time = []
WVR_ZTD = []        # 干延迟(m)
GPS_time = []
GPS_ZTD = []

def datelist(start: str,end: str) -> list:
    date_list = [] 
    begin_date = datetime.strptime(start, r"%Y%m%d") 
    end_date = datetime.strptime(end,r"%Y%m%d") 
    while begin_date <= end_date: 
        date_str = begin_date.strftime(r"%Y%m%d") 
        date_list.append(date_str) 
        # 日期加法days=1 months=1等等
        begin_date += timedelta(days=1) 
    return date_list

def ReadWVRFile(filename: str = None):
    filein = wreader.wvrfile(filename)
    global WVR_time 
    global WVR_ZTD
    WVR_time = filein.Time()
    WVR_ZTD = filein.ZTD()

def ReadGPSFile(filename: str = None):
    year = int(filename[2:4]) + 2000
    month = int(filename[4:6])
    day = int(filename[-2:])
    doy = ymd2doy(year, month, day)

    if doy < 10:
        doy = '00' + str(doy)
    elif doy < 100:
        doy = '0' + str(doy)
    else:
        doy = str(doy)

    openfile = '../RawDatas/IGS_ZPD_SHAO/SHAO' + doy + '0.' + str(year - 2000) + 'zpd'

    gt = []
    gz = []
    with open(openfile, 'r') as f_gps:
        for line in f_gps:
            if '+TROP/SOLUTION' in line:
                break
        alldata = f_gps.readlines()[1:]
        for line in alldata:
            if '-TROP/SOLUTION' in line:
                break
            Arr = line.strip().split()
            gt.append(float(Arr[1][-5:]))
            gz.append(float(Arr[2]))

    global GPS_time
    global GPS_ZTD
    GPS_time = gt
    GPS_ZTD = gz

def t2s(t: str):
    h,m,s = t.strip().split(":")
    return float(h) * 3600 + float(m) * 60 + float(s)

def ymd2doy(year, month, day):
    return (datetime(year, month, day) - datetime(year, 1, 1)).days + 1

def DrawTogether(date: str):
    plt.cla()
    plt.plot(WVR_time,WVR_ZTD,label='WVR')
    plt.plot(GPS_time,GPS_ZTD,label='GPS')
    plt.title(date +' GPS & WVR')
    plt.ylabel('Total zenith path delay(mm)')
    plt.xlabel('time(s)')
    plt.xlim(0, 86400)
    plt.xticks([0, 21600, 43200, 64800, 86400],
          ['0:00', '6:00', '12:00', '18:00', '24:00'])
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(6))
    plt.tick_params(which='both', direction='in')
    plt.legend()
    plt.savefig('../Estimate/WVR_vs_GPS/'+date+'.png', dpi=500)
    plt.close('all')

def ShowDif(date: str):
    wgt = []
    wvrz = []

    i = 0
    for time in WVR_time:
        if time in GPS_time and time not in wgt:
            wgt.append(WVR_time[i])
            wvrz.append(WVR_ZTD[i])
        i += 1

    dif = [a-b for a,b in zip(GPS_ZTD, wvrz)]
    
    RecordDif(date, dif)

    plt.cla()
    plt.plot(wgt, dif, label='GPS-WVR')
    plt.title(date + 'diference of GPS and WVR')
    plt.ylabel('dif(mm)')
    plt.xlabel('time(s)')
    plt.legend()
    plt.savefig('GPS-WVR_dif/'+date+'.png')
    plt.close('all')

def RecordDif(date: str, dif: list):
    with open('GPS-WVR_dif/dif.txt', 'a') as f_dif:
        mdf = mean(dif)
        f_dif.write(date + '\t' + str(mdf) + '\n')
    f_dif.close()

def Run(ds: str, de: str):

    date_path = "../RawDatas/WVR_raw_data"
    date_dir = os.listdir(date_path)

    for date in tqdm(datelist(ds, de)):
        if date not in date_dir:
            print('Can\'t find ' + i + ' file!')
            continue
        filepath = date_path + '/' + date
        files = os.listdir(filepath)
        for i in files:
            if os.path.splitext(i)[1] == ".txt":
                try:
                    ReadWVRFile(filepath + '/' + i)
                    ReadGPSFile(date)
                    DrawTogether(date)
                    #ShowDif(date)
                except:
                    print('Something wrong with ' + date + ' file!')
                    pass

if __name__ == '__main__':

    ds = '20190101'    # 起
    de = '20191230'    # 止

    Run(ds, de)
