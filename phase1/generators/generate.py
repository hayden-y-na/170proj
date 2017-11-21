import sys
import random

def translate(x):
    if x == 1:
        return "A"
    elif x == 2:
        return "B"
    elif x == 3:
        return "C"
    elif x == 4:
        return "D"
    elif x == 5:
        return "E"
    elif x == 6:
        return "F"
    elif x == 7:
        return "G"
    elif x == 8:
        return "H"
    elif x == 9:
        return "I"
    elif x == 10:
        return "J"
    elif x == 11:
        return "K"
    elif x == 12:
        return "L"
    elif x == 13:
        return "M"
    elif x == 14:
        return "N"
    elif x == 15:
        return "O"
    elif x == 16:
        return "P"
    elif x == 17:
        return "Q"
    elif x == 18:
        return "R"
    elif x == 19:
        return "S"
    elif x == 20:
        return "T"
    elif x == 21:
        return "U"
    elif x == 22:
        return "V"
    elif x == 23:
        return "W"
    elif x == 24:
        return "X"
    elif x == 25:
        return "Y"
    elif x == 26:
        return "Z"
    else:
        return "invalid"
    

f = open("constraints.txt", 'w')

for x in range(1000):
    a1 = random.randint(1,26)
    a2 = random.randint(1,26)
    a3 = random.randint(1,26)
    if a1 < a2:
        if a3 not in range(a1, a2 + 1):
            f.write(translate(a1) + " " + translate(a2) + " " + translate(a3) + "\n")
    elif a2 < a1:
        if a3 not in range(a2, a1 + 1):
            f.write(translate(a1) + " " + translate(a2) + " " + translate(a3) + "\n")
    else:
        continue


































