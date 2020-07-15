# Input :   v(frequency)(GHz)
# Output :  C(value)(1)

def C(v):
    b0 = 1.110303146
    b1 = -0.01906468
    b2 = 3.280422e-3
    b3 = -9.2051e-5
    b4 = 7.13e-7

    result = b0 + b1 * v + b2 * v**2 + b3 * v**3 + b4 * v**4

    return 0.011 * result