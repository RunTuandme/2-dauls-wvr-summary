# tau
# Input :   TB(brightness temperature)(K), 
#           T0(temperature at groud)(K) 
# Output :  T(Temperature)(K)

def T_m(T0):
    return 0.72 * T0 + 70.2

from math import log

def tau(TB, T0):
    Tc = 2.9
    Tm = T_m(T0)
    inm = (Tm-Tc) / (Tm-TB)
    result = log(abs(inm))

    return result