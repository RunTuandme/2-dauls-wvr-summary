from WVR.tau import tau
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def t2s(t):
    h,m,s = t.strip().split(":")
    return float(h) * 3600 + float(m) * 60 + float(s)

WVR_time = []
WVR_ZWD = []
WVR_Tb1 = []
WVR_Tb2 = []
WVR_T0 = []

with open('../WVR_raw_data/20181101/SH_FSJ_D1811010004.txt','r') as f_wvr:
    for line in f_wvr:
        if line in ['\n','\r\n']:
            pass
        else:
            Arr = line.strip().split()
            if len(Arr[0]) > 4:
                if Arr[0][:4] == '2018':
                    WVR_time.append(t2s(Arr[1]))
                    WVR_ZWD.append(float(Arr[3]))
                    WVR_Tb1.append(float(Arr[6]))
                    WVR_Tb2.append(float(Arr[7]))
                    WVR_T0.append(float(Arr[8]))

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

""" print("coefficients: ", model.coef_)
print("intercept: ", model.intercept_)
print('Mean squared error: %.3f' % mean_squared_error(y_test, model.predict(x_test)))
print('score: %.3f' % model.score(x_test, y_test))   """

WVR_cal = [b0+b1*a+b2*b for a,b in zip(WVR_tau1,WVR_tau2)]

plt.plot(WVR_time,WVR_cal,'b',label='WVR_calculates')
plt.plot(WVR_time,WVR_ZWD,'r',label='WVR_products')
#plt.plot(GPS_time,GPS_ZTD,label='GPS')
plt.title('WVR')
plt.ylabel('Total zenith path delay(mm)')
plt.xlabel('time(s)')
plt.legend()
plt.show() 