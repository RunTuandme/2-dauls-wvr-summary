# calculate wet delay
# Input :   TB1(brightness temperature1)(K), 
#           TB2(brightness temperature2)(K), 
#           v1(frequency1)(GHz), 
#           v2(frequency2)(GHz), 
#           p_v(pressure of wet air)(mm), 
#           T0(temperature at groud)(K), 
#           P0(pressure at groud)(K), 
#           h0(height above the sea level for the station)(km)
# Output :  Lv(wet delay)(mm)

from tau_ import tau
from kv_cruz import *
from Kox.kox import *

def t2s(t):
    h,m,s = t.strip().split(":")
    return float(h) * 3600 + float(m) * 60 + float(s)

def W_m(T0, v1, v2, P0, p_v):
    '''
    T(temperature)(K), v1(frequency1)(GHz), v2(frequency2)(GHz), p(pressure of dry air)(hPa or mbar), 
    p_v(pressure of wet air)(hPa or mbar)
    '''
    kv1 = kv(T0, v1, P0, p_v)
    kv2 = kv(T0, v2, P0, p_v)

    rho = 217 * p_v / T0

    result = T0 / rho * (kv1 / v1**2 - kv2 / v2**2)

    return result

def tau_d(v1, v2, h0, T0, P0):
    sum = 0
    for i in range(5500):
        h = h0 + i * 5 / 1000
        kox1 = kox(v1, h0, h, T0, P0)
        kox2 = kox(v2, h0, h, T0, P0)
        sum += (kox1 / v1**2 - kox2 / v2**2) * 5e-3
    return sum

def Lv(TB1, TB2, v1, v2, p_v, T0, P0, h0):
    """ 
    TB1(brightness temperature1)(K), 
    TB2(brightness temperature2)(K), 
    v1(frequency1)(GHz), 
    v2(frequency2)(GHz), 
    p_v(pressure of wet air)(hPa or mbar), 
    T0(temperature at groud)(K), 
    P0(pressure at groud)(K), 
    h0(height above the sea level for the station)(km) 
    """
    tau1 = tau(TB1, T0)
    tau2 = tau(TB2, T0)

    K = 1.763e-3
    Wm = W_m(T0, v1, v2, P0, p_v)
    taud = tau_d(v1, v2, h0, T0, P0)

    b0 = -K * taud / Wm * 1e6
    b1 = K / (v1**2 * Wm) * 1e6
    b2 =-K / (v2**2 * Wm) * 1e6

    result = b0 + b1*tau1 + b2*tau2

    return [b0, b1, b2, result]

if __name__ == '__main__':
    '''test'''
    from e0 import *
    T0 = 9.2 + 273.15
    pv = e0(T0) * 0.929
    P0 = 1026.3
    h0 = 49.2 / 1000
    re = Lv(27.2514, 29.8020, 23.8, 31.2, pv, T0, P0, h0)
    
    print (re)