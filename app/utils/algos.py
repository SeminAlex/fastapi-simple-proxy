def nearest_divisor(dividend, value):
    for i in range(value, int(dividend/2)+1):
        if dividend % i == 0:
            return i
    return dividend

