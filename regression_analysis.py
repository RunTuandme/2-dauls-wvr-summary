from WVR.tau_ import tau
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import time

def t2s(t):
    h,m,s = t.strip().split(":")
    return float(h) * 3600 + float(m) * 60 + float(s)

filelist = []
now_time = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

with open('regression/regression' + now_time + '.txt','w') as outfile:
    outfile.writelines('data\t\tb0\t\tb1\t\tb2\t\trms\t\tr2\n')
outfile.close()

path = "raw_data"

for home, dirs, files in os.walk(path):
    for filename in files:
        if 'txt' in filename:
            filelist.append(os.path.join(home, filename))

bar = tqdm(filelist)

for file in bar:
    bar.set_description(f"Now get {file}")

    WVR_time = []
    WVR_ZWD = []
    WVR_Tb1 = []
    WVR_Tb2 = []
    WVR_T0 = []

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
                        read = True
        if not read:
            continue

    WVR_tau1 = [tau(a, b) for a,b in zip(WVR_Tb1, WVR_T0)]
    WVR_tau2 = [tau(a, b) for a,b in zip(WVR_Tb2, WVR_T0)]

    length = len(WVR_tau1)
    l3 = int(length/3)

    x_data = list(zip(WVR_tau1, WVR_tau2)) 
    #y_data = [a * 1e-6 for a in WVR_ZWD]
    y_data = WVR_ZWD

    x1 = x_data[:l3]
    x2 = x_data[l3:l3*2]
    x3 = x_data[l3*2:]
    y1 = y_data[:l3]
    y2 = y_data[l3:l3*2]
    y3 = y_data[l3*2:]

    x_train = np.array(x1 + x3)
    y_train = np.array(y1 + y3)
    x_test = np.array(x2)
    y_test = np.array(y2)

    model = LinearRegression()

    model.fit(x_train, y_train)

    b0 = model.intercept_
    b1, b2 = model.coef_
    rms = mean_squared_error(y_test, model.predict(x_test))
    r2 = model.score(x_test, y_test)

    f_wvr.close()

    with open('regression/regression' + now_time + '.txt','a') as outfile:
        outfile.write(date + '\t\t' )
        print('%.3f' % b0, file=outfile, end='')
        outfile.write('\t\t')
        print('%.3f' % b1, file=outfile, end='')
        outfile.write('\t\t')
        print('%.3f' % b2, file=outfile, end='')
        outfile.write('\t\t')
        print('%.3f' % rms, file=outfile, end='')
        outfile.write('\t\t')
        print('%.3f' % r2, file=outfile)
    outfile.close()

    time.sleep(0.1)

    """ print("coefficients: ", model.coef_)
    print("intercept: ", model.intercept_)
    print('Mean squared error: %.3f' % mean_squared_error(y_test, model.predict(x_test)))
    print('score: %.3f' % model.score(x_test, y_test)) """ 

    WVR_cal = [b0+b1*a+b2*b for a,b in zip(WVR_tau1,WVR_tau2)]

    plt.plot(WVR_time,WVR_cal,label='WVR_calculates')
    plt.plot(WVR_time,WVR_ZWD,label='WVR_products')
    #plt.plot(GPS_time,GPS_ZTD,label='GPS')
    plt.title('products-calculates date:'+date)
    plt.ylabel('Zenith wet path delay(mm)')
    plt.xlabel('time(s)')
    plt.legend()
    plt.savefig('regression/' + date + '.png')
    plt.close('all')  
