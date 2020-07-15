# The attenuation spectrum kv of 22GHz water vapor with the Van Vleck-Weisskopf line shape.
# Input :   T(temperature)(K), 
#           v(frequency)(GHz), 
#           p(pressure of air)(hPa or mbar), 
#           rho(density of water vapor)(g/m3) 
# Output :  kv(Absorption coefficient)(km-1)

import numpy as np
import math

def kv(T, v, p, rho):
    '''
    T(temperature)(K), v(frequency)(GHz), p(pressure of dry air)(hPa or mbar), 
    rho(density of water vapor)(g/m3) 
    '''

    delta_v1 = 2.96 * (p / 1013) * (300 / T)**0.626 * (1 + 0.018 * rho * T / p)
    part1 = rho * v**2 * delta_v1 * T**(-3/2)
    part2 = 7.18 * math.exp(-644/T) / T
    part3 = 1 / ((494.40190-v**2)**2 + 4 * v**2 * delta_v1**2)
    part4 = 2.77e-8
    
    k_v = part1 * (part2 * part3 + part4)

    return k_v