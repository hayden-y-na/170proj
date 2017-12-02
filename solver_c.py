import sys
import re
import random
import atexit
import pickle


def main(argv):
    inputFile = open('inputs/' + argv + '.in', 'r')
    numWizards = int(inputFile.readline())
    numConstraints = int(inputFile.readline())

    # Check if we already have a good list of names saved.
    try:
        f = open("bestSoFar/output" + argv[-4:], 'rb')
        names = pickle.load(f)
        f.close()
    except:
        names = list(createSet(inputFile, numWizards))
    inputFile.close()    
    inputFile = open('inputs/' + argv + '.in', 'r')
    numWizards = int(inputFile.readline())
    numConstraints = int(inputFile.readline())
   
    # Create list of contraints 
    constraints = list()
    for line in inputFile:
        triple = re.sub("[^\w]", " ", line).split()
        constraints.append(triple) 

    # If we are starting with a random list of names
    # continue to shuffle them until we get 3/4 of the
    # constraints satisfied
    numSat, numFail = conSat(names, constraints)
    while numSat < (3 * numConstraints) / 4:
        names.reverse()
        random.shuffle(names)
        numSat, numFail = conSat(names, constraints)
    f = open("bestSoFar/output" + argv[-4:], 'w+b') 
    pickle.dump(names, f)
    f.close()
    print("Number satisfied before maxSat called: " + str(numSat))

    # Call our algorithms on names, contraints
    #try:
    maxSat(names, constraints, argv)
    #except:
        #print("error occured during a call to maxSat()")
        #f = open("bestSoFar/output" + argv[-4:], 'w+b') 
        #pickle.dump(names, f)
        #f.close()
    
    # Print information and save list of names to output
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


def maxSat(names, constraints, filename):
    numSat, failed = conSat(names, constraints)
    if (numSat == len(constraints)):
        return
    while numSat < ((19 * len(constraints)) / 20):
        constraint = failed.pop()
        posA = random.randint(0, len(names) - 1)
        posB = random.randint(0, len(names) - 1)
        while (posA == posB):
            posB = random.randint(0, len(names) - 1)

        prob = random.random()
        if (prob < 0.5):
            minimum = min(posA, posB)
            if minimum == 0:
                minimum = 1
            posC = random.randint(0, minimum - 1)
            if posC < 0:
                posC = 0
        else:
            maximum = max(posA, posB)
            minimum = min(posA, posB)
            posC = random.randint(minimum, maximum - 1)

        prob = random.random()
        if (prob < 0.5):
            newNames = move(names, names.index(constraint[0]), posA)
            newNames = move(newNames, names.index(constraint[1]), posB)
            newNames = move(newNames, names.index(constraint[2]), posC)
            newNumSat, newFail = conSat(newNames, constraints)

            chance = random.random()
            if (chance < 1):
                limit = numSat + 5
            elif (chance < 0.99):
                limit = numSat - (len(constraints) / 10)
            elif (chance < 0.999):
                limit = 0
            else:
                limit = numSat - (len(constraints) / 100)

            if newNumSat > limit:
                print("New number of contraints satisfied: " + str(newNumSat))
                numSat = newNumSat
                names = newNames
                f = open("bestSoFar/output" + filename[-4:], 'w+b') 
                pickle.dump(names, f)
                f.close()
                failed = newFail
                if (random.random() < 0.5):
                    names.reverse()
            else:
                failed.append(constraint)
        elif prob < 0.6:
            for i in range(random.randint(0, len(names) - 1)):
                wizard = random.randint(0, len(names) - 1)
                index = random.randint(0, len(names) - 1)
                newNames = move(names, wizard, index)
                newNumSat, newFail = conSat(newNames, constraints)

            chance = random.random()
            if (chance < 1):
                limit = numSat + 5
            elif (chance < 0.99):
                limit = numSat - (len(constraints) / 10)
            elif (chance < 0.999):
                limit = 0
            else:
                limit = numSat - (len(constraints) / 100)

            if newNumSat > limit:
                print("New number of contraints satisfied: " + str(newNumSat))
                numSat = newNumSat
                names = newNames
                f = open("bestSoFar/output" + filename[-4:], 'w+b') 
                pickle.dump(names, f)
                f.close()
                failed = newFail
                if (random.random() < 0.5):
                    names.reverse()
            else:
                failed.append(constraint)
        else:
            names = shift(names, random.randint(0, len(names) - 2))
            failed.append(constraint)



def move(lst, toMove, index):
    newLst = list(lst)
    name = newLst[toMove]
    newLst.remove(name)
    newLst.insert(index, name)
    return newLst

def shift(lst, numShifts):
    while (numShifts > 0):
        lst = move(lst, len(lst) - 1, 0)
        numShifts -= 1
    return lst

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
    """
    for j in range(len(names)):
        for k in range(len(names)):
            for l in range (len(names)):
                newNames = move(names, names.index(constraint[0]), j)
                newNames = move(newNames, names.index(constraint[1]), k)
                newNames = move(newNames, names.index(constraint[2]), l)
                newNumSat, newFail = conSat(newNames, constraints)
                failed = newFail
                if newNumSat > numSat:
                    print("New number of contraints satisfied: " + str(newNumSat))
                    numSat = newNumSat
                    names = newNames
                    names.reverse()
                    return maxSat()
    """
