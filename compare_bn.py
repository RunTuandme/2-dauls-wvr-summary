# -*- coding: UTF-8 -*-

# --------------- 单个文件读取 --------------- #

import sys
sys.path.append('d:/work/TwoDaul/two_daul/WVR') 

from tqdm import tqdm
# from WVR.Lv import Lv             # python版的湿延迟计算库
from WVR.e0 import e0
from WVR.tau_ import tau
import matplotlib.pyplot as plt
import os
from multiprocessing import Pool
from ctypes import *

dll = CDLL('zwd.dll')             # windows版
# dll = CDLL('libzwd.so')             # linux版
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

    file = '../RawDatas/WVR_raw_data/20180121/SH_FSJ_D1801210004.txt'
    with open(file,'r',encoding='gbk') as f_wvr:
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
    plt.title('products-calculates date:180121')
    plt.ylabel('Zenith wet path delay(mm)')
    plt.xlabel('time(s)')
    plt.xlim(0, 86400)
    plt.xticks([21600, 43200, 64800],
          ['6:00', '12:00', '18:00'])
    plt.tick_params(which='both', direction='in')
    plt.legend()
    plt.savefig('prod_vs_cal/180121_cruz492.png', dpi=1500) 

    with open('prod_vs_cal/180121_cruz492.txt','w') as f_out:
        for i in WVR_Lv:
            f_out.write(str(i) + '\n')
    f_out.close()