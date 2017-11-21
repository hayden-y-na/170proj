import sys
import random

def translate(x):
    if x // 10 == 0:
        return "A" + str(x % 10)
    elif x // 10 == 1:
        return "B" + str(x % 10)
    elif x // 10 == 2:
        return "C" + str(x % 10)
    elif x // 10 == 3:
        return "D" + str(x % 10)
    elif x // 10 == 4:
        return "E" + str(x % 10)
    elif x // 10 == 1:
        return "F" + str(x % 10)
    elif x // 10 == 1:
        return "G" + str(x % 10)
    elif x // 10 == 1:
        return "H" + str(x % 10)
    else:
        return "invalid"
    

f = open("constraints.txt", 'w')
s = set()
tbl = list()
for i in range(50):
    tbl.insert(i, list())
    for j in range(50):
        tbl[i].insert(j, 0)



for x in range(3000):
    a1 = random.randint(0,49)
    a2 = random.randint(0,49)
    a3 = random.randint(0,49)
    if a1 < a2:
        if a3 not in range(a1, a2 + 1) and abs(a1 - a2) > 10 and tbl[a1][a2] < 10:
            s.add(translate(a1) + " " + translate(a2) + " " + translate(a3) + "\n")
            tbl[a1][a2] += 1
            tbl[a2][a1] += 1
    elif a2 < a1:
        if a3 not in range(a2, a1 + 1) and abs(a1 - a2) > 10 and tbl[a2][a1]:
            s.add(translate(a1) + " " + translate(a2) + " " + translate(a3) + "\n")
            tbl[a1][a2] += 1
            tbl[a2][a1] += 1
    else:
        continue

for x in s:
    f.write(x)

































