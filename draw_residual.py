import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
import numpy as np
import seaborn as sns

def timeswitch(epoch: str):
    year = pd.to_datetime('20' + epoch[:2])
    that_time = year + pd.Timedelta(days=int(epoch[3:6])-1) + pd.Timedelta(seconds=int(epoch[-5:]))
    return that_time

def cal_residual_data(wvrfile: str, gpsfile: str):
    with open(gpsfile, 'r') as gf:
        for i, line in enumerate(gf, start = 1):
            if '+TROP/SOLUTION' in line:
                header_line = i
            if '-TROP/SOLUTION' in line:
                tailer_line = i
                break
    df = pd.read_csv(gpsfile, delim_whitespace = True, 
                    header = header_line, engine = 'c',skip_blank_lines = False, 
                    skiprows = [tailer_line - 1, tailer_line])
    ep = list(df)[1]
    df = df[[ep, list(df)[2]]]
    df[ep] = df[ep].map(timeswitch)

    df2 = pd.read_csv(wvrfile, sep = '\s+', 
                    encoding = "GB2312",
                    usecols = ['时间','总延迟(m)'])
    df2 = df2.reset_index()
    df2['时间']=df2['index'] + ' '+ df2['时间']
    df2 = df2.drop(['index'], axis=1)
    df2['时间'] = df2['时间'].map(lambda x : pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S'))
    df2 = df2.rename(columns = {'时间': ep})

    data = pd.merge(df, df2, on=[ep])
    data["residual"]=data.apply(lambda x:x["总延迟(m)"]*1000-x["TROTOT"],axis=1)

    return data

def get_gps_file(date: str)-> str:
    # date: 20170101

    year = date[:4]
    month = date[4:6]
    day = date[-2:]

    dd = datetime.strptime(date, '%Y%m%d')
    dstart = datetime.strptime(year, '%Y')
    doy = (dd - dstart).days + 1

    if doy < 10:
        doy_str = '00' + str(doy)
    elif doy < 100:
        doy_str = '0' + str(doy)
    else:
        doy_str = str(doy)

    f = '../RawDatas/IGS_ZPD_SHAO/' + 'SHAO' + doy_str + '0.' + year[-2:] + 'zpd'

    return f

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

if __name__ == '__main__':

    # 先得到残差
    """ ds = '20150801'
    de = '20200330'

    for i in tqdm(datelist(ds, de)):
        try:
            f_wvr = get_wvr_file(i)
            f_gps = get_gps_file(i)
            data = cal_residual_data(f_wvr, f_gps)
        except:
            print(i + ' file wrong')
            continue
        data.to_csv('../Estimate/residual/' + i + '.csv') """

    # 画图
    filepath = '../Estimate/residual/'

    files = os.listdir(filepath)
    for i in files:
        if os.path.splitext(i)[1] == ".csv":
            f = filepath + i
            df = pd.read_csv(f,index_col=0)
            ep = list(df)[0]
            df[ep] = df[ep].map(lambda x : datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
            df = df[(df['residual'] > -1000) & (df['residual'] < 1000)]
            plt.scatter(df[ep], df['residual'], color='#1f77b4',s=1)

    plt.xticks(rotation=45)
    plt.title('Time series of residual of WVR and GPS at SHAO station')
    plt.xlabel('Date (UTC)')
    plt.ylabel('Residual (mm)')
    plt.show()
    #plt.savefig(filepath + 'scatter/residual.pdf')

    # 画残差分布直方图——人工分组
    """ filepath = '../Estimate/residual/'

    sections = [-1000, -345, -315, -285, -255, -225, -195, -165, -135, -105,  -75,  -45,
        -15,   15,   45,   75,  105,  135,  165,  195,  225,  255,  285,
        315, 345, 1000]

    group_names = ['< -345','-345 - -315','-315 - -285','-285 - -255','-255 - -225',
               '-225 - -195','-195 - -165','-165 - -135','-135 - -105','-105 - -75',
               '-75 - -45','-45 - -15', '-15 - 15','15 - 45','45 - 75','75 - 105',
               '105 - 135','135 - 165','165 - 195','195 - 225','225 - 255','255 - 285',
               '285 - 315','315 - 345','> 345']

    files = os.listdir(filepath)
    for i in tqdm(files):
        f = filepath + i
        df = pd.read_csv(f,index_col=0)
        ep = list(df)[0]
        df[ep] = df[ep].map(lambda x : pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S'))
        df = df[(df['residual'] > -1000) & (df['residual'] < 1000)]
        res = np.array(df['residual'])
        cuts = pd.cut(res, sections, labels=group_names)
        x = cuts.value_counts().plot(kind='bar')
        x.figure.savefig(filepath + 'hist/' + i + '.png')
        plt.close('all') """

    # 画残差分布直方图——自动分组
    """ filepath = '../Estimate/residual/'

    files = os.listdir(filepath)
    for i in tqdm(files):
        if os.path.splitext(i)[1] == ".csv":
            f = filepath + i
            df = pd.read_csv(f,index_col=0)
            ep = list(df)[0]
            df[ep] = df[ep].map(lambda x : pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S'))
            df = df[(df['residual'] > -1000) & (df['residual'] < 1000)]
            sns.distplot(df['residual'], kde=True)
            plt.savefig(filepath + 'hist_auto/' + i + '.png')
            plt.close('all') """

    # 总统计保存
    """ filepath = '../Estimate/residual/'

    df_total = pd.DataFrame(columns=['EPOCH_______','TROTOT','总延迟(m)','residual'])
    
    files = os.listdir(filepath)
    for i in tqdm(files):
        if os.path.splitext(i)[1] == ".csv":
            f = filepath + i
            df = pd.read_csv(f,index_col=0)
            ep = list(df)[0]
            df[ep] = df[ep].map(lambda x : pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S'))
            df = df[(df['residual'] > -1000) & (df['residual'] < 1000)]
            df = pd.DataFrame(df, columns = ['EPOCH_______','TROTOT','总延迟(m)','residual'])
            df_total = pd.concat([df_total,df])

    df_total.to_csv(filepath + 'all/all.csv') """

    # 总统计值记录
    """ filepath = '../Estimate/residual/all/'
    file = 'all.csv'

    df = pd.read_csv(filepath + file)
    print(df['residual'].mean())
    print(df['residual'].std()) """
    