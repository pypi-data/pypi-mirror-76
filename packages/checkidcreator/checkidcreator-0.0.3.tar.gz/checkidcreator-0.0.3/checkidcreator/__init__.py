import random


def createID(length=3, modulo=10):
    n = ""
    cd = 0
    digits = []
    id = ""
    for i in range(0, length-1):
        n = (random.randint(0, 9))
        digits.append(n)

    for i in range(length - 1, 0, -1):
        cd = cd + (digits[i - 1] * i)

    cd = cd % modulo
    for i in range(0, length - 1):
        id = id + str(digits[i])

    id = id + str(cd)
    if len(id) == length:
        return (id)
    else:
        return createID(length, modulo)
