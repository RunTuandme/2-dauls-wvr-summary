import os
from datetime import datetime
import matplotlib.pyplot as plt
from tqdm import tqdm
from numpy import mean

def ReadWVRFile(filename: str = None):
    read = False
    with open(filename, 'r') as f_wvr:
        for line in f_wvr:
            if line in ['\n','\r\n']:
                pass
            else:
                Arr = line.strip().split()
                if len(Arr[0]) > 4:
                    if ':' in Arr[3]:
                        del Arr[:2]
                    if Arr[0][:3] == '201':
                        WVR_time.append(t2s(Arr[1]))
                        WVR_ZTD.append(float(Arr[4]) * 1e3)
                        read = True
    f_wvr.close()
    if not read:
        return

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

    openfile = 'IGS_ZPD_SHAO/SHAO' + doy + '0.' + str(year - 2000) + 'zpd'

    with open(openfile, 'r') as f_gps:
        n = 0
        for line in f_gps:
            if '+TROP/SOLUTION' in line:
                break
            n += 1
        for line in f_gps.readlines()[n+2:]:
            if '-TROP/SOLUTION' in line:
                break
            Arr = line.strip().split()
            GPS_time.append(float(Arr[1][-5:]))
            GPS_ZTD.append(float(Arr[2]))
    f_gps.close()


def t2s(t: str):
    h,m,s = t.strip().split(":")
    return float(h) * 3600 + float(m) * 60 + float(s)

def ymd2doy(year, month, day):
    return (datetime(year, month, day) - datetime(year, 1, 1)).days + 1

def DrawTogether(date: str):
    plt.cla()
    plt.plot(WVR_time,WVR_ZTD,'r',label='WVR')
    plt.plot(GPS_time,GPS_ZTD,'b',label='GPS')
    plt.title(date +' GPS & WVR')
    plt.ylabel('Total zenith path delay(mm)')
    plt.xlabel('time(s)')
    plt.legend()
    plt.savefig('WVR_vs_GPS/'+date+'.png')
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

if __name__ == '__main__':

    filelist = []

    path = "raw_data"

    data_year = '2018'
    data_month = '11'
    data_day_start = '01'
    data_day_end = '30'

    date_records = os.listdir(path)

    # -----打开 WVR 文件 ----- #
    ds = int(data_day_start)
    de = int(data_day_end)
    dd = ds

    while dd <= de:
        if dd < 10:
            date = data_year + data_month + '0' + str(dd)
        else:
            date = data_year + data_month + str(dd)

        if date in date_records:
            print ('Now is dealing with: ' + date + '...')

            filepath = path + '/' + date
            files = os.listdir(filepath)

            for i in files:
                if os.path.splitext(i)[1] == ".txt":
                    WVR_time = []
                    WVR_ZTD = []        # 干延迟(m)
                    GPS_time = []
                    GPS_ZTD = []
                    try:
                        ReadWVRFile(filepath + '/' + i)
                        ReadGPSFile(date)
                        DrawTogether(date)
                        ShowDif(date)
                    except:
                        print('Can\'t find ' + date + ' file!')
                        pass
        dd += 1