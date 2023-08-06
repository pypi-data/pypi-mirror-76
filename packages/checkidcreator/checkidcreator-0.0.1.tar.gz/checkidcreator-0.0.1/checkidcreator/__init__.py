import random


def createID(length=3):
    n = ""
    cd = 0
    digits = []
    id = ""
    for i in range(0, length-1):
        n = (random.randint(0, 9))
        digits.append(n)

    for i in range(length - 1, 0, -1):
        cd = cd + (digits[i - 1] * i)
        print("d:", digits[i-1])
        print("d*i:", digits[i - 1] * i)
        print("cd:", cd)

    cd = cd % 10
    for i in range(0, length - 1):
        id = id + str(digits[i])

    id = id + str(cd)
    return(id)


createID(4)
