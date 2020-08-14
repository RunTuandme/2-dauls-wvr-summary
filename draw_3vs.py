import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mp
from matplotlib.ticker import AutoMinorLocator
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

    openfile = '../RawDatas/IGS_ZPD_SHAO/SHAO' + doy + '0.' + str(year - 2000) + 'zpd'

    with open(openfile, 'r') as f_gps:
        for line in f_gps:
            if '+TROP/SOLUTION' in line:
                break
        alldata = f_gps.readlines()[1:]
        for line in alldata:
            if '-TROP/SOLUTION' in line:
                break
            Arr = line.strip().split()
            GPS_time.append(float(Arr[1][-5:]))
            GPS_ZTD.append(float(Arr[2]))

def ReadRTFile(filename: str = None):
    openfile = '../Estimate/spa_result/' + filename + '.txt'

    with open(openfile, 'r') as f_rt:
        All = f_rt.readlines()
        Data = All[1:]

        for line in Data:
            Arr = line.strip().split()
            RT_ZTD.append(float(Arr[1])*10)

def t2s(t: str):
    h,m,s = t.strip().split(":")
    return float(h) * 3600 + float(m) * 60 + float(s)

def ymd2doy(year, month, day):
    return (datetime(year, month, day) - datetime(year, 1, 1)).days + 1

# for all
def DrawTogether(date: str):
    plt.cla()

    p1, = plt.plot(WVR_time,WVR_ZTD,'#fdae61',label='WVR')
    p2, = plt.plot(GPS_time,GPS_ZTD,'#2b83ba',label='GPS')
    p3 = plt.scatter(RT_time,RT_ZTD,color='#abdda4',label='RT',marker='^')

    plt.title('GPS & WVR & RT comparison on '\
         + date[:4] + '-' + date[4:6] + '-' + date[6:], fontdict={'weight': 'semibold'})

    plt.ylabel('Total zenith path delay (mm)', fontdict={'weight': 'medium'})
    plt.xlabel('time', fontdict={'weight': 'medium'})

    plt.legend()
    
    plt.savefig('../Estimate/WVR_vs_GPS_vs_RT/'+date+'.png')

    plt.close('all')

# for 20180122
""" def DrawTogether(date: str):
    plt.cla()

    p1, = plt.plot(WVR_time,WVR_ZTD,'#fdae61',label='WVR')
    p2, = plt.plot(GPS_time,GPS_ZTD,'#2b83ba',label='GPS')
    p3 = plt.scatter(RT_time,RT_ZTD,color='#abdda4',label='RT',marker='^')

    plt.title('GPS & WVR & RT comparison on '\
         + date[:4] + '-' + date[4:6] + '-' + date[6:], fontdict={'weight': 'semibold'})

    plt.ylabel('Total zenith path delay (mm)', fontdict={'weight': 'medium'})
    plt.xlabel('time', fontdict={'weight': 'medium'})

    plt.xlim(0, 86400)
    plt.ylim(2100,3000)

    plt.xticks([0, 21600, 43200, 64800, 86400],
          ['0:00', '6:00', '12:00', '18:00', '24:00'])
    plt.yticks([2200, 2400, 2600, 2800],
          [2200, 2400, 2600, 2800])
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(6))
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator(5))
    plt.tick_params(which='both', direction='in')

    bottom = 2175
    height = 50
    rect1 = mp.Rectangle((0, bottom), 7200, height, edgecolor='black', facecolor='#08519c', alpha=0.5, label='Light Rain')
    rect2 = mp.Rectangle((7200,bottom), 21600, height, edgecolor='black', facecolor='#6baed6', alpha=0.5, label='Cloudy')
    rect3 = mp.Rectangle((28800, bottom), 9000, height, edgecolor='black', facecolor='#eff3ff', alpha=0.5, label='Fog')
    rect4 = mp.Rectangle((37800, bottom), 3600, height, edgecolor='black', facecolor='#6baed6', alpha=0.5)
    rect5 = mp.Rectangle((41400, bottom), 3600, height, edgecolor='black', facecolor='#3182bd', alpha=0.5, label='Mostly Cloudy')
    rect6 = mp.Rectangle((45000, bottom), 1800, height, edgecolor='black', facecolor='#bdd7e7', alpha=0.5, label='Partly Cloudy')
    rect7 = mp.Rectangle((46800, bottom), 9000, height, edgecolor='black', facecolor='#3182bd', alpha=0.5)
    rect8 = mp.Rectangle((55800, bottom), 7200, height, edgecolor='black', facecolor='#bdd7e7', alpha=0.5)
    rect9 = mp.Rectangle((63000, bottom), 3600, height, edgecolor='black', facecolor='#3182bd', alpha=0.5)
    rect10 = mp.Rectangle((66600, bottom), 1800, height, edgecolor='black', facecolor='w', alpha=0.5, label='Fair')
    rect11 = mp.Rectangle((68400, bottom), 5400, height, edgecolor='black', facecolor='#bdd7e7', alpha=0.5)
    rect12 = mp.Rectangle((73800, bottom), 12600, height, edgecolor='black', facecolor='#3182bd', alpha=0.5)

    r1 = plt.gca().add_patch(rect1)
    r2 = plt.gca().add_patch(rect2)
    r3 = plt.gca().add_patch(rect3)
    plt.gca().add_patch(rect4)
    r5 = plt.gca().add_patch(rect5)
    r6 = plt.gca().add_patch(rect6)
    plt.gca().add_patch(rect7)
    plt.gca().add_patch(rect8)
    plt.gca().add_patch(rect9)
    r10 = plt.gca().add_patch(rect10)
    plt.gca().add_patch(rect11)
    plt.gca().add_patch(rect12)

    l1 = plt.legend(handles=[p1,p2,p3], labels=['WVR','GPS','RT'], loc='upper right', bbox_to_anchor=(0.69,1))
    plt.legend(handles=[r1,r5,r2,r6,r3,r10], labels=['Light Rain','Mostly Cloudy', 'Cloudy', 'Partly Cloudy', 'Fog', 'Fair'], loc='upper right')
    plt.gca().add_artist(l1)

    plt.gca().spines['top'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.gca().spines['left'].set_linewidth(1.5)
    plt.gca().spines['right'].set_linewidth(1.5)

    plt.savefig('../Estimate/WVR_vs_GPS_vs_RT/'+date+'.png', dpi = 1500)

    plt.close('all') """

# for 20180121
""" def DrawTogether(date: str):
    plt.cla()

    p1, = plt.plot(WVR_time,WVR_ZTD,'#fdae61',label='WVR')
    p2, = plt.plot(GPS_time,GPS_ZTD,'#2b83ba',label='GPS')
    p3 = plt.scatter(RT_time,RT_ZTD,color='#abdda4',label='RT',marker='^')

    plt.title('GPS & WVR & RT comparison on '\
         + date[:4] + '-' + date[4:6] + '-' + date[6:], fontdict={'weight': 'semibold'})

    plt.ylabel('Total zenith path delay (mm)', fontdict={'weight': 'medium'})
    plt.xlabel('time', fontdict={'weight': 'medium'})

    plt.xlim(0, 86400)
    plt.ylim(2100,3100)

    plt.xticks([0, 21600, 43200, 64800, 86400],
          ['0:00', '6:00', '12:00', '18:00', '24:00'])
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(6))
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator(5))
    plt.tick_params(which='both', direction='in')

    bottom = 2175
    height = 50
    rect1 = mp.Rectangle((0, bottom), 27000, height, edgecolor='black', facecolor='w', alpha=0.5, label='fair')
    rect2 = mp.Rectangle((27000, bottom), 5400, height, edgecolor='black', facecolor='#eff3ff', alpha=0.5, label='Partly Cloudy')
    rect3 = mp.Rectangle((32400, bottom), 9000, height, edgecolor='black', facecolor='#6baed6', alpha=0.5, label='Mostly Cloudy')
    rect4 = mp.Rectangle((41400, bottom), 14400, height, edgecolor='black', facecolor='#bdd7e7', alpha=0.5, label='Cloudy')
    rect5 = mp.Rectangle((55800, bottom), 30600, height, edgecolor='black', facecolor='#2171b5', alpha=0.5, label='Light Rain')

    r1 = plt.gca().add_patch(rect1)
    r2 = plt.gca().add_patch(rect2)
    r3 = plt.gca().add_patch(rect3)
    r4 = plt.gca().add_patch(rect4)
    r5 = plt.gca().add_patch(rect5)

    l1 = plt.legend(handles=[p1,p2,p3], labels=['WVR','GPS','RT'], loc='upper left', bbox_to_anchor=(0.31,1))
    plt.legend(handles=[r5,r3,r4,r2,r1], labels=['Light Rain','Mostly Cloudy', 'Cloudy', 'Partly Cloudy', 'Fair'], loc='upper left')
    plt.gca().add_artist(l1)

    plt.savefig('../Estimate/WVR_vs_GPS_vs_RT/'+date+'.png', dpi = 1500)

    plt.close('all') """

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

    path = "../RawDatas/WVR_raw_data"

    data_year = '2018'
    data_month = '01'
    data_day_start = '23'
    data_day_end = '26'

    date_records = os.listdir(path)

    # -----按日期打开 WVR 文件 ----- #
    ds = int(data_day_start)
    de = int(data_day_end)
    dd = ds

    while dd <= de:
        if dd < 10:
            date = data_year + data_month + '0' + str(dd)
        else:
            date = data_year + data_month + str(dd)

        if date in date_records:
            print ('---> Now is dealing with: ' + date + '...')

            filepath = path + '/' + date
            files = os.listdir(filepath)

            for i in files:
                if os.path.splitext(i)[1] == ".txt":
                    WVR_time = []
                    WVR_ZTD = []        # 干延迟(m)
                    GPS_time = []
                    GPS_ZTD = []
                    RT_time = (0, 10800, 21600, 32400, 43200, 54000, 64800, 75600)
                    RT_ZTD = []
                    #try:
                    ReadWVRFile(filepath + '/' + i)
                    ReadGPSFile(date)
                    ReadRTFile(date)
                    DrawTogether(date)
                        # ShowDif(date)
                    #except:
                        #print('Can\'t find ' + date + ' file!')
                        #pass
        dd += 1