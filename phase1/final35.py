import sys
import random
import pickle


wizards = pickle.load(open('wizards/wizards35.p', 'rb'))

w = open('inputs/input35.in', 'w')
w.write(str(35) + '\n')
for name in wizards:
    w.write(name + " ")
w.write("\n")    

s = set()
tbl = list()
for i in range(35):
    tbl.insert(i, list())
    for j in range(35):
        tbl[i].insert(j, 0)



for x in range(1800):
    a1 = random.randint(0,34)
    a2 = random.randint(0,34)
    a3 = random.randint(0,34)
    if a1 < a2:
        if a3 not in range(a1, a2 + 1) and abs(a1 - a2) > 7 and tbl[a1][a2] < 7:
            s.add(wizards[a1] + " " + wizards[a2] + " " + wizards[a3] + "\n")
            tbl[a1][a2] += 1
            tbl[a2][a1] += 1
    elif a2 < a1:
        if a3 not in range(a2, a1 + 1) and abs(a1 - a2) > 7 and tbl[a2][a1] < 7:
            s.add(wizards[a1] + " " + wizards[a2] + " " + wizards[a3] + "\n")
            tbl[a1][a2] += 1
            tbl[a2][a1] += 1
    else:
        continue

w.write(str(len(s)) + "\n")
for x in s:
    w.write(x)
w.close()
