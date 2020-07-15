# Temperature_US for calculate temperature
# Input : h(height above sea level)(km)
# Output : TUS(Temperature_US)(K)

def TUS(h):
    temp = 288.16 - 6.5 * h
    if temp > 277:
        return temp
    elif temp <= 277 and h < 20:
        return 217
    else:
        return 197 + h