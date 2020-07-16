# The attenuation spectrum kv of 22GHz water vapor with the Van Vleck-Weisskopf line shape.
# Input :   T(temperature)(K), 
#           v(frequency)(GHz), 
#           p(pressure of dry air)(hPa or mbar), 
#           p_v(pressure of wet air)(hPa or mbar)
# Output :  kv(Absorption coefficient)(km-1)

import numpy as np
import math

def kv(T, v, p, p_v):
    '''
    T(temperature)(K), v(frequency)(GHz), p(pressure of dry air)(hPa or mbar), 
    p_v(pressure of wet air)(hPa or mbar) 
    '''
    v0 = 22.23510 # GHz
    delta_v = 2.784e-3 * ( p*((300/T)**0.6) + 4.8*p_v*((300/T)**1.1) )
    m1 = 1 / ( ((v-v0)**2)+(delta_v ** 2) )
    m2 = 1 / ( ((v+v0)**2)+(delta_v ** 2) )
    x1 = m1 + m2

    TL = 0.0109 * p_v * (300/T)**3.5 * math.exp(2.143 * (1 - 300/T))
    TS = delta_v / v0 * x1
    TC = 1.2 * (1.13e-8 * p_v * p * (300/T)**3 + 3.57e-7 * p_v**2 * (300/T)**10.5)

    k_v = 0.0419 * v**2 * (TL * TS + TC)

    return k_v