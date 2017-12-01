import argparse
import itertools
import sys
import re
import random
import heapq
import datetime

"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(num_wizards, num_constraints, wizards, constraints):
    """
    Write your algorithm here.
    Input:
        num_wizards: Number of wizards
        num_constraints: Number of constraints
        wizards: An array of wizard names, in no particular order
        constraints: A 2D-array of constraints, 
                     where constraints[0] may take the form ['A', 'B', 'C']i

    Output:
        An array of wizard names in the ordering your algorithm returns
    """
    
    """constraint_array = []
    constraint_set = set()
    free_var = constraints[0][0]
    curr = 0
    for i in range(0,len(constraints)):
        if free_var in constraints[i]:
            constraint_array += [constraints[i]]
            constraint_set.add(constraints[i][0])
            constraint_set.add(constraints[i][1])
            constraint_set.add(constraints[i][2])
            curr = i
        if (len(constraint_set) > 10):
            break

    poss_perm = list(itertools.permutations(list(constraint_set)))

    print(constraint_array)
    print(constraint_set)
    print(curr)


    for p in poss_perm:
        pl = list(p)
        for c in constraint_array:
            if (pl.index(c[0]) > pl.index(c[2]) and pl.index(c[1]) < pl.index(c[2])):
                poss_perm.pop(poss_perm.index(p))
                break
            elif (pl.index(c[0]) < pl.index(c[2]) and pl.index(c[1]) > pl.index(c[2])):
                poss_perm.pop(poss_perm.index(p))
                break

    print(len(poss_perm))
    return []"""
    startTime = datetime.datetime.now()
    bestParent = startWizards(wizards, constraints)
    bestFitness = get_fitness(bestParent, constraints)
    display(bestParent, startTime)

    wizardPriorityQueue = []
    seenWizards = set()
    seenWizards.add(tuple(bestParent))

    heapq.heappush(wizardPriorityQueue, (len(constraints) - bestFitness, bestParent))
    mutate(bestParent, wizardPriorityQueue, seenWizards)


    while bestFitness < num_constraints:
        child = pickChild(wizardPriorityQueue, seenWizards)
        childFitness = get_fitness(child, constraints)
        print(childFitness)
        print(bestFitness)

        if bestFitness >= childFitness:
            continue
        display(bestParent, startTime)
        bestFitness = childFitness
        bestParent = child 


    return bestParent


def pickChild(wizardPriorityQueue, seenWizards):
    rand = random.random()
    if (rand < 0.9):
        fitness, newWizard = heapq.heappop(wizardPriorityQueue)
        mutate(newWizard, wizardPriorityQueue, seenWizards)
        return newWizard
    else: 
        index = random.randrange(0, len(wizardPriorityQueue))
        newWizard = wizardPriorityQueue.pop(index)
        mutate(newWizard[1], wizardPriorityQueue, seenWizards)
        heapq.heapify(wizardPriorityQueue)
        return newWizard[1]



def startWizards(wizards, constraints):
    numSat  = get_fitness(wizards, constraints)
    while numSat < (4 * num_constraints) / 6:
    #while numSat < numConstraints:
        random.shuffle(wizards)
        numSat = get_fitness(wizards, constraints)
    print("Number Passed: " + str(numSat))
    return wizards


def get_fitness(wizards, constraints):
    numFailed = 0
    numPassed = 0
    for constraint in constraints:
        wiz_a = wizards.index(constraint[0])
        wiz_b = wizards.index(constraint[1])
        wiz_c = wizards.index(constraint[2])
        if (wiz_a < wiz_c < wiz_b) or (wiz_b < wiz_c < wiz_a):
            numFailed += 1
        else:
            numPassed += 1
    return numPassed

def mutate(wizards, wizardPriorityQueue, seenWizards):
    index1 = random.randrange(0, len(wizards))
    index2 = random.randrange(0, len(wizards))
    index3 = random.randrange(0, len(wizards))

    wizards1 = list(wizards)
    wizards2 = list(wizards)
    wizards3 = list(wizards)

    temp = wizards1[index1]
    wizards1[index1] = wizards1[index2]
    wizards1[index2] = temp
    if tuple(wizards1) not in seenWizards:
        seenWizards.add(tuple(wizards1))
        heapq.heappush(wizardPriorityQueue, (len(constraints) - get_fitness(wizards1, constraints), wizards1))

    temp = wizards2[index1]
    wizards2[index1] = wizards2[index3]
    wizards2[index3] = temp
    if tuple(wizards2) not in seenWizards:
        seenWizards.add(tuple(wizards2))
        heapq.heappush(wizardPriorityQueue, (len(constraints) - get_fitness(wizards2, constraints), wizards2))

    temp = wizards3[index2]
    wizards3[index2] = wizards3[index3]
    wizards3[index3] = temp
    if tuple(wizards3) not in seenWizards:
        seenWizards.add(tuple(wizards3))
        heapq.heappush(wizardPriorityQueue, (len(constraints) - get_fitness(wizards3, constraints), wizards3))



def shiftArray(wizards, index):
    wizards = [wizards[index]] + wizards[0:index] + wizards[index + 1:]
    return wizards

def display(gwizards, startTime):
    timeDiff = datetime.datetime.now() - startTime
    fitness = get_fitness(wizards, constraints)
    print("{0}\t{1}\t{2}".format(wizards, fitness, str(timeDiff)))





"""
======================================================================
   No need to change any code below this line
======================================================================
"""

def read_input(filename):
    with open(filename) as f:
        num_wizards = int(f.readline())
        num_constraints = int(f.readline())
        constraints = []
        wizards = set()
        for _ in range(num_constraints):
            c = f.readline().split()
            constraints.append(c)
            for w in c:
                wizards.add(w)
                
    wizards = list(wizards)
    return num_wizards, num_constraints, wizards, constraints

def write_output(filename, solution):
    with open(filename, "w") as f:
        for wizard in solution:
            f.write("{0} ".format(wizard))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Constraint Solver.")
    parser.add_argument("input_file", type=str, help = "___.in")
    parser.add_argument("output_file", type=str, help = "___.out")
    args = parser.parse_args()

    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
    solution = solve(num_wizards, num_constraints, wizards, constraints)
    write_output(args.output_file, solution)
