'''
画出GPS、WVR、RT总延迟结果在一天中不同天气条件下的成图，可自定义天气范围
'''

import os
import matplotlib.pyplot as plt
from tqdm import tqdm
from numpy import mean
from datetime import datetime,timedelta
from matplotlib.ticker import AutoMinorLocator
import matplotlib.patches as mp
import wreader
import pandas as pd
import importlib
import numpy as np

WVR_time = []
WVR_ZTD = []        # 总延迟(m)
GPS_time = []
GPS_ZTD = []
RT_time = (0, 10800, 21600, 32400, 43200, 54000, 64800, 75600)
RT_ZTD = []
Weather_Condition = []
WVR_T = []
WVR_RHO = []
WVR_P = []

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
    global WVR_P
    global WVR_RHO
    global WVR_T
    WVR_time = filein.Time()
    WVR_ZTD = filein.ZTD()
    WVR_T = filein.T0()
    WVR_RHO = filein.e()
    WVR_P = filein.P0()

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

def ReadRTFile(filename: str = None):
    """ Format:'20180204' """
    openfile = '../Estimate/spa_result/' + filename + '.txt'

    rz = []
    with open(openfile, 'r') as f_rt:
        All = f_rt.readlines()
        Data = All[1:]

        for line in Data:
            Arr = line.strip().split()
            rz.append(float(Arr[1])*10)

    global RT_ZTD
    RT_ZTD = rz

def ReadWeatherFile(filename: str = None):
    """ Format:'2018-2-4' """
    openfile = '../RawDatas/weather_data/' + filename + '.csv'
    df = pd.read_csv(openfile)

    wd = []
    for i in df['Condition']:
        wd.append(i)
    
    global Weather_Condition
    Weather_Condition = wd

def t2s(t: str):
    h,m,s = t.strip().split(":")
    return float(h) * 3600 + float(m) * 60 + float(s)

def ymd2doy(year, month, day):
    return (datetime(year, month, day) - datetime(year, 1, 1)).days + 1

def DivWC(wclist: list) -> list:
    """ Divide Weather Condition, return large of blocks, corresponding name """
    con = []
    name = ''
    leng = 0
    for i in wclist:
        if name != i:
            if leng > 0:
                con.append((leng, name))
            name = i
            leng = 1
        else:
            leng += 1
    con.append((leng, name))
    return con

def weather_color(condition: str) -> str:
    if 'T-Storm' in condition:
        return '#08519c'
    if 'Rain' in condition or 'Snow' in condition \
        or 'Wintry Mix' in condition or 'Thunder' in condition:
        return '#3182bd'
    if 'Cloudy' in condition:
        return '#6baed6'
    if 'Fog'  in condition or 'Mist' in condition:
        return '#bdd7e7'
    if 'Haze' in condition:
        return '#eff3ff'
    if 'Fair' in condition:
        return '#fed976' 
    else:
        return '#FFFFFF'

def BlueColors(num: int) -> list:
    if num == 1:
        return ['blue']
    if num == 2:
        return ['blue', '#f7fbff']
    if num >= 3 and num <= 9:
        module_name = 'Blues_' + str(num)
        lib = importlib.import_module('palettable.colorbrewer.sequential')
        class_in_lib = getattr(lib, module_name)
        return class_in_lib.hex_colors
    else:
        raise ValueError('Number of colors is out of range')

def DrawTogether(date: str):
    plt.cla()

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    p1, = ax1.plot(WVR_time,WVR_ZTD,'#fdae61',label='WVR')
    p2, = ax1.plot(GPS_time,GPS_ZTD,'#2b83ba',label='GPS')
    p3  = ax1.scatter(RT_time,RT_ZTD,color='#abdda4',label='RT',marker='^')

    ax1.set_title('GPS & WVR & RT comparison on '\
         + date[:4] + '-' + date[4:6] + '-' + date[6:], fontdict={'weight': 'semibold'})
    
    ax1.set_ylabel('Total zenith path delay(mm)')
    ax1.set_xlabel('time(s)')
    ax1.set_xlim(0, 86400)
    ymin = min(min(WVR_ZTD),min(GPS_ZTD),min(RT_ZTD))
    ymax = max(max(WVR_ZTD),max(GPS_ZTD),max(RT_ZTD))
    ax1.set_ylim(ymin-240, ymax+100)
    ax1.set_xticks([0, 21600, 43200, 64800, 86400])
    ax1.set_xticklabels(['0:00', '6:00', '12:00', '18:00', '24:00'])
    ax1.xaxis.set_minor_locator(AutoMinorLocator(6))
    ax1.tick_params(which='both', direction='in')

    bottom = ymin - 215
    height = 50

    rect = DivWC(Weather_Condition)
    # colorlist = BlueColors(len(set(rect)))
    # bound = dict(zip(set(Weather_Condition),colorlist))
    start = 0
    r_type = []
    r_type_name = []
    typen = []
    for i in rect:
        rect_object = mp.Rectangle((start, bottom), i[0]*1800, height, edgecolor='black',
            facecolor=weather_color(i[1]), alpha=0.5, label=i[1])
        start += i[0] * 1800
        if i[1] not in typen:
            r_type.append(ax1.add_patch(rect_object))
            r_type_name.append(i[1])
            typen.append(i[1])
        else:
            ax1.add_patch(rect_object)

    box1 = ax1.get_position()
    ax1.set_position([box1.x0, box1.y0, box1.width* 0.8, box1.height])

    l1 = ax1.legend(handles=[p1,p2,p3], labels=['WVR','GPS','RT'], loc='best')
    ax1.legend(handles=r_type, labels=r_type_name, loc='upper left', bbox_to_anchor=(1, 1))
    ax1.add_artist(l1)
    # plt.legend(loc='best', ncol= 2)

    ax1.spines['top'].set_linewidth(1.5)
    ax1.spines['bottom'].set_linewidth(1.5)
    ax1.spines['left'].set_linewidth(1.5)
    ax1.spines['right'].set_linewidth(1.5)

    plt.savefig('../Estimate/3vs_weather/'+date+'.png', dpi=500)
    plt.close('all')

def SwitchDate(date: str) -> str:
    year = date[:4]
    month = str(int(date[4:6]))
    day = str(int(date[6:]))
    return year + '-' + month + '-' + day

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
                    ReadRTFile(date)
                    ReadWeatherFile(SwitchDate(date))
                    DrawTogether(date)
                except:
                    print('Something wrong with ' + date + ' file!')
                    pass

if __name__ == '__main__':

    ds = '20180101'    # 起
    de = '20180101'    # 止

    Run(ds, de)
