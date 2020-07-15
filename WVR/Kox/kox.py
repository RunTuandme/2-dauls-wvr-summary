# Oxygen absorption coefficient.
# Input :   v(frequency)(GHz)
#           h0(height above the sea level for the station)(km), 
#           h(height above sea level)(km), 
#           T0(temperature at groud)(K), 
#           P0(pressure at groud)(K) 
# Output :  kox(Oxygen absorption coefficient)

import sys  
sys.path.append('D:\\work\\python\WVR')

from Kox.C import C
from Kox.gamma import gamma
from Kox.gamma0 import gamma0
from Kox.T import T
from Kox.P import P

def kox(v, h0, h, T0, P0):
    '''
    v(frequency)(GHz), 
    h0(height above the sea level for the station)(km), 
    h(height above sea level)(km), 
    T0(temperature)(K), 
    P0(pressure at groud)(K) 
    '''
    p1 = C(v) * gamma0(h0, h, P0) * v**2
    p2 = (P(h0, h, P0) / 1013)**2
    p3 = (300 / T(h0, h, T0))**2.85
    p4 = (v - 60)**2 + gamma(h0, h, T0, P0)**2
    p5 = v**2 + gamma(h0, h, T0, P0)**2

    return p1 * p2 * p3 * (1/p4 + 1/p5)

if __name__ == '__main__':
    '''test'''
    v = 23
    h0 = 0
    h = 0
    T0 = 293
    P0 = 1013
    print (kox(v, h0, h, T0, P0))
