# Input :   h0(height above the sea level for the station)(km), 
#           h(height above sea level)(km), 
#           T0(temperature at groud)(K), 
#           P0(pressure at groud)(K) 
# Output :  gamma

from Kox.gamma0 import gamma0
from Kox.P import P
from Kox.T import T

def gamma(h0, h, T0, P0):
    p1 = gamma0(h0, h, P0)
    p2 = P(h0, h, P0) / 1013
    p3 = (300 / T(h0, h, T0)) ** 0.85

    return p1 * p2 * p3