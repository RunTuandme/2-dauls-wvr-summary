import pandas as pd
from wvrfname import get_wvr_file
from datelist import datelist
from wvrpd import wvrfile_to_df
from tqdm import tqdm
#from profilehooks import profile

#@profile
def rain_fliter(date: str):
    # date格式: 20150801
    # return : ep.[(Timestamp('2015-08-01 17:00:00'), Timestamp('2015-08-01 17:30:00')),
    #              (Timestamp('2015-08-01 17:30:00'), Timestamp('2015-08-01 18:00:00'))]

    def SwitchDate(date: str) -> str:
        year = date[:4]
        month = str(int(date[4:6]))
        day = str(int(date[6:]))
        return year + '-' + month + '-' + day

    def time_to_second(t: str) -> float:
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

    # 读取文件得到Dataframe
    filepath = '../RawDatas/weather_data/' + SwitchDate(date) + '.csv'
    weather_df = pd.read_csv(filepath)

    # 查找下雨时辰并记录
    fliter_container = []
    for i, condition in enumerate(weather_df['Condition']):
        if 'Rain' in condition or 'Snow' in condition \
            or 'Wintry Mix' in condition or 'Thunder' in condition:
            fliter_container.append(i)

    # 记录下雨时段
    fliter_time = []
    time_interval = pd.Timedelta('30 min')
    for i in fliter_container:
        time_second = time_to_second(weather_df['Time'][i])
        rain_start_time = pd.to_datetime(date) + pd.Timedelta(seconds = time_second)
        fliter_time.append((rain_start_time, rain_start_time + time_interval))

    return  fliter_time

#@profile
def del_from_time(wvr_df, fliter_time: list):
    if len(fliter_time) < 1:
        return wvr_df

    copy_wvrdf = wvr_df.copy()
    flag = False
    drop_box = []
    for i, wtime in enumerate(copy_wvrdf['时间']):
        if wtime >= fliter_time[0][0]:
            if wtime > fliter_time[0][1]:
                if len(fliter_time) == 1:
                    flag = True
                else:
                    fliter_time.pop(0)
            else:
                drop_box.append(i)
        if flag:
            break
    copy_wvrdf = copy_wvrdf.drop(drop_box)
    return copy_wvrdf


if __name__ == '__main__':

    ds = '20170725'
    de = '20200330'

    for i in tqdm(datelist(ds, de)):
        try:
            wvr_file = get_wvr_file(i)
            wvr_df = wvrfile_to_df(wvr_file)
        except:
            print(i + ' file wrong')
            continue
        rain_time = rain_fliter(i)
        new_wvr_df = del_from_time(wvr_df, rain_time)
        new_wvr_df.to_csv('../RainFilterData/' + i + '.csv')
        