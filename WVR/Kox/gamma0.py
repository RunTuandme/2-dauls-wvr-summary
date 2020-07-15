# Input :   h0(height above the sea level for the station)(km), 
#           h(height above sea level)(km), 
#           P0(pressure at groud)(K) 
# Output :  gamma0

from Kox.P import P

def gamma0(h0, h, P0):
    Ph = P(h0, h, P0)

    if Ph > 333:
        return 0.59
    elif Ph > 25 and Ph <= 333:
        return 0.59 * (1 + 0.0031 * (333 - Ph))
    else:
        return 1.18