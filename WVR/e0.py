# This script used to calculate the saturated water vapor pressure.
# Use method Clausius-Clapeyron equation, which is precise batter 
# than 1% within the temperature range 240-310K

from numpy import exp

def e0(T):
    '''
    This function used to calculate the saturated water vapor pressure.
    Please use it when the temperature range 240-310k.
    T: temperature (K)
    '''
    if T < 240 or T > 310:
        raise ValueError('The temperature param should be between 240-310k')

    Part1 = (T/273) ** (-5.3)
    Part2 = exp(25.2 * (T-273) / T)
    return 6.11 * Part1 * Part2
