# Pressure at h
# Input :   h0(height above the sea level for the station)(km), 
#           h(height above sea level)(km), 
#           P0(pressure at groud)(K) 
# Output :  P(pressure)(hPa or mbar)

from math import exp

def P(h0, h, P0):
    '''
    h0(height above the sea level for the station)(km), 
    h(height above sea level)(km), 
    P0(pressure at groud)(K) 
    '''
    top = 8.387 * (h0 - h)
    btm = (8.387 - 0.0887 * h0) * (8.387 - 0.0887 * h)
    result = P0 * exp(top / btm)

    return result