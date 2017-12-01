import sys
import re
import random

def main(argv):
    inputFile = open('inputs/' + argv + '.in', 'r')
    numWizards = int(inputFile.readline())
    numConstraints = int(inputFile.readline())
    names = list(createSet(inputFile, numWizards))

    inputFile = open('inputs/' + argv + '.in', 'r')
    numWizards = int(inputFile.readline())
    numConstraints = int(inputFile.readline())
    
    constraints = list()
    for line in inputFile:
        triple = re.sub("[^\w]", " ", line).split()
        constraints.append(triple) 

    while numSat < (4 * numConstraints) / 5:
        random.shuffle(names)
        numSat, numFail = conSat(names, constraints)
    print("Number satisfied before maxSat called: " + numSat)

    names = maxSat(names, constraints)

    print("num constraints: " + str(len(constraints)))
    outputFile = open('outputs/output' + argv[-4:] + '.out', 'w') 
    output = ""
    for name in names:
        output += name + " "
    outputFile.write(output)
    inputFile.close()

    numPassed, numFailed = conSat(names, constraints)
    print("Number Passed: " + str(numPassed))
    print("Number Failed: " + str(len(numFailed)))


def maxSat(names, constraints):
    numSat, failed = conSat(names, constraints)
    if (numSat == len(constraints)):
        return names
    while numSat < len(constraints):
        constraint = failed.pop()
        for j in range(len(names)):
            for k in range(len(names)):
                for l in range (len(names)):
                    newNames = move(names, names.index(constraint[0]), j)
                    newNames = move(newNames, names.index(constraint[1]), k)
                    newNames = move(newNames, names.index(constraint[2]), l)
                    newNumSat, newFail = conSat(newNames, constraints)
                    if newNumSat > numSat:
                        print("New number of contraints satisfied: " + str(newNumSat))
                        numSat = newNumSat
                        names = newNames
                        return maxSat(names, constraints)



def move(lst, toMove, index):
    newLst = list(lst)
    name = newLst[toMove]
    newLst.remove(name)
    newLst.insert(index, name)
    return newLst



def switch(lst, index0, index1):
    if (index0 < 0 or index1 < 0):
        return list(lst)
    if (index0 >= len(lst) or index1 >= len(lst)):
        return list(lst)
    lst = list(lst)
    x = lst[index0]
    lst[index0] = lst[index1]
    lst[index1] = x
    return lst


def allSat(names, constraints):
    numPassed = 0
    for constraint in constraints:
        wiz_a = names.index(constraint[0])
        wiz_b = names.index(constraint[1])
        wiz_c = names.index(constraint[2])
        if (wiz_a < wiz_c < wiz_b) or (wiz_b < wiz_c < wiz_a):
            numFailed.append(constraint)
        else:
            numPassed += 1
    return numPassed == len(constraints)


def createSet(f, numWiz):
    s = set()
    for line in f:
        names = re.sub("[^\w]", " ", line).split()
        for name in names:
            s.add(name)
        if len(s) == numWiz:
            return s
    return s

def alphabetize(lst):
    for triple in lst:
        if triple[0] > triple[1]:
            x = triple[0]
            triple[0] = triple[1]
            triple[1] = x

def makeTable(constraints, numWizards):
    alphabetize(constraints)

    # Make a table to see how many times two variables are used as constraints
    tbl = list()
    for i in range(numWizards):
        tbl.insert(i, list())
        for j in range(numWizards):
            tbl[i].insert(j, 0)
    for constraint in constraints:
       tbl[names.index(constraint[0])][names.index(constraint[1])] += 1
    for row in tbl:
        print(row)
    return tbl

def writeNames(argv, names):
    inputFile = open('inputs/' + argv + '.in', 'r')
    contents = inputFile.readlines()
    inputFile.close()

    wizardString = ""
    for name in names:
        wizardString += name + " "
    wizardString += "\n"

    contents.insert(1, wizardString) 

    f = open('inputs/' + argv + '.in', 'w')
    contents = "".join(contents)
    f.write(contents)
    f.close()

def conSat(names, constraints):
    numFailed = list()
    numPassed = 0
    for constraint in constraints:
        wiz_a = names.index(constraint[0])
        wiz_b = names.index(constraint[1])
        wiz_c = names.index(constraint[2])
        if (wiz_a < wiz_c < wiz_b) or (wiz_b < wiz_c < wiz_a):
            numFailed.append(constraint)
        else:
            numPassed += 1
    return numPassed, numFailed



if __name__ == "__main__":
    main(sys.argv[1])
