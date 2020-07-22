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

import sys
sys.path.append('d:/work/two_daul/WVR')

from tqdm import tqdm
from WVR.Lv import Lv
from WVR.e0 import e0
from WVR.tau_ import tau
import matplotlib.pyplot as plt
import os

def t2s(t):
    h,m,s = t.strip().split(":")
    return float(h) * 3600 + float(m) * 60 + float(s)

WVR_time = []
WVR_ZWD = []
WVR_Tb1 = []
WVR_Tb2 = []
WVR_T0 = []
WVR_P0 = []
WVR_e = []      # 相对湿度

file = 'raw_data/20181101/SH_FSJ_D1811010004.txt'
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

#WVR_Lv = [Lv(TB1, TB2, 23.8, 31.2, p_v, T0, P0, 0.0492)[3] for TB1, TB2, p_v, T0, P0 in zip(WVR_Tb1, WVR_Tb2, pv, WVR_T0, WVR_P0)]

WVR_Lv = []

bar = tqdm(rebuild)
for i in bar:
    lv = Lv(i[0], i[1], 23.8, 31.2, i[2], i[3], i[4], 0.0492)
    WVR_Lv.append(lv[3])

plt.plot(WVR_time,WVR_Lv,label='WVR_calculates')
plt.plot(WVR_time,WVR_ZWD,label='WVR_products')
plt.title('products-calculates date:181101')
plt.ylabel('Zenith wet path delay(mm)')
plt.xlabel('time(s)')
plt.legend()
plt.savefig('prod_vs_cal/181101.png') 

with open('prod_vs_cal/181101.txt','w') as f_out:
    f_out.writelines(WVR_Lv)
f_out.close()