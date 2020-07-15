# Temperature at h
# Input :   h0(height above the sea level for the station)(km), 
#           h(height above sea level)(km), 
#           T0(temperature at groud)(K) 
# Output :  T(Temperature)(K)

from Kox.TUS import TUS

def T(h0, h, T0):
    if h >= h0 and h <= h0 + 2:
        result = T0 + (h - h0) / 2 * (TUS(h0 + 2) - T0)
        return result
    elif h > h0 + 2 and h <= 20:
        return TUS(h)
    elif h > 20 and h <= 30:
        return 217
    else:
        raise ValueError('The param \'h\' is less than \'h0\' or more than 30')