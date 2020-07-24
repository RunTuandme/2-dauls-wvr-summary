""" 
import sys
sys.path.append('d:/work/two_daul/WVR')

#from tqdm import tqdm
from WVR.Lv import Lv
from WVR.e0 import e0
from WVR.tau_ import tau
import matplotlib.pyplot as plt
import os

def t2s(t):
    h,m,s = t.strip().split(":")
    return float(h) * 3600 + float(m) * 60 + float(s)

filelist = []

path = "raw_data"

for home, dirs, files in os.walk(path):
    for filename in files:
        if 'txt' in filename:
            filelist.append(os.path.join(home, filename))

#bar = tqdm(filelist)


for file in filelist:
    # bar.set_description(f"Now get {file}")

    WVR_time = []
    WVR_ZWD = []
    WVR_Tb1 = []
    WVR_Tb2 = []
    WVR_T0 = []
    WVR_P0 = []
    WVR_e = []      # 相对湿度

    date_year = file[-14:-12]
    date_month = file[-12:-10]
    date_day = file[-10:-8]
    date = date_year + date_month + date_day

    with open(file,'r') as f_wvr:
        read = False
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
                        WVR_ZWD.append(float(Arr[3]))
                        WVR_Tb1.append(float(Arr[6]))
                        WVR_Tb2.append(float(Arr[7]))
                        WVR_T0.append(float(Arr[8])+273.15)
                        WVR_e.append(float(Arr[9])/100)
                        WVR_P0.append(float(Arr[10]))
                        read = True
        if not read:
            continue
    f_wvr.close()

    WVR_tau1 = [tau(a, b) for a,b in zip(WVR_Tb1, WVR_T0)]
    WVR_tau2 = [tau(a, b) for a,b in zip(WVR_Tb2, WVR_T0)]

    pv = [e0(T0)*e for T0, e in zip(WVR_T0, WVR_e)]

    WVR_Lv = [Lv(TB1, TB2, 23.8, 31.2, p_v, T0, P0, 0.0492) for TB1, TB2, p_v, T0, P0 in zip(WVR_Tb1, WVR_Tb2, pv, WVR_T0, WVR_P0)]

    plt.plot(WVR_time,WVR_Lv,label='WVR_calculates')
    plt.plot(WVR_time,WVR_ZWD,label='WVR_products')
    plt.title('products-calculates date:'+date)
    plt.ylabel('Zenith wet path delay(mm)')
    plt.xlabel('time(s)')
    plt.legend()
    plt.savefig('prod_vs_cal/' + date + '.png')
    plt.close('all')  """

# --------------- 单个文件读取 --------------- #

import sys
sys.path.append('d:/work/two_daul/WVR')

from tqdm import tqdm
# from WVR.Lv import Lv
from WVR.e0 import e0
from WVR.tau_ import tau
import matplotlib.pyplot as plt
import os
from multiprocessing import Pool
from ctypes import *

dll = CDLL('zwd.dll')
dll.Lv.argtypes = [c_double] * 8    # 指定传入参数类型
dll.Lv.restype = c_double           # 指定输出结果类型

def t2s(t: str):
    h,m,s = t.strip().split(":")
    return float(h) * 3600 + float(m) * 60 + float(s)

def Mutiwork(Team: tuple) -> float:
    a1 = c_double(Team[0])
    a2 = c_double(Team[1])
    a3 = c_double(23.8)
    a4 = c_double(31.2)
    a5 = c_double(Team[2])
    a6 = c_double(Team[3])
    a7 = c_double(Team[4])
    a8 = c_double(0.0492)
    lv = dll.Lv(a1, a2, a3, a4, a5, a6, a7, a8)
    return lv

if __name__ == '__main__':

    WVR_time = []
    WVR_ZWD = []
    WVR_Tb1 = []
    WVR_Tb2 = []
    WVR_T0 = []
    WVR_P0 = []
    WVR_e = []      # 相对湿度

    file = '../WVR_raw_data/20180217/SH_FSJ_D1802170004.txt'
    with open(file,'r') as f_wvr:
        read = False
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
                        WVR_ZWD.append(float(Arr[3]))
                        WVR_Tb1.append(float(Arr[7]))
                        WVR_Tb2.append(float(Arr[8]))
                        WVR_T0.append(float(Arr[9])+273.15)
                        WVR_e.append(float(Arr[10])/100)
                        WVR_P0.append(float(Arr[11]))
                        read = True
        if not read:
            pass
    f_wvr.close()

    WVR_tau1 = [tau(a, b) for a,b in zip(WVR_Tb1, WVR_T0)]
    WVR_tau2 = [tau(a, b) for a,b in zip(WVR_Tb2, WVR_T0)]

    pv = [e0(T0)*e for T0, e in zip(WVR_T0, WVR_e)]

    rebuild = list(zip(WVR_Tb1, WVR_Tb2, pv, WVR_T0, WVR_P0))

    p = Pool(6)
    pbar = tqdm(total=len(rebuild))
    def Update(*a):
        pbar.update()

    ms = []
    for i in rebuild:
        result = p.apply_async(Mutiwork, args=(i,), callback=Update)
        ms.append(result)

    p.close()
    p.join()

    WVR_Lv = []
    for i in ms:
        WVR_Lv.append(i.get())   # 注意：获取返回值get()方法一定要在进程池回收之后进行，否则进程阻塞。无法并行。

    plt.plot(WVR_time,WVR_Lv,label='WVR_calculates')
    plt.plot(WVR_time,WVR_ZWD,label='WVR_products')
    plt.title('products-calculates date:181101')
    plt.ylabel('Zenith wet path delay(mm)')
    plt.xlabel('time(s)')
    plt.legend()
    plt.savefig('prod_vs_cal/180217_cruz.png') 

    with open('prod_vs_cal/180217_cruz.txt','w') as f_out:
        for i in WVR_Lv:
            f_out.write(str(i) + '\n')
    f_out.close()