import argparse
import itertools
import sys
import math
import random
from simanneal import Annealer


"""
======================================================================
  Complete the following function.
======================================================================
"""
class orderAnnealer(Annealer):
    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state, constraints):
        self.state = state
        self.constraints = constraints
        self.immutableconstraints = constraints
        super(orderAnnealer, self).__init__(state)  # important!

    def move(self):
        index = random.randrange(0, len(self.state))
        bestWizards = []
        bestEnergy = 500
        for i in range(0, len(self.state)):
            if i == index:
                continue
            rand = random.random()
            tempWizards = list(self.state)
            wizard = tempWizards.pop(index)
            tempWizards.insert(i, wizard)
            tempEnergy = self.get_fitness(tempWizards)
            if tempEnergy < bestEnergy and rand > 0.01:
                bestEnergy = tempEnergy
                bestWizards = tempWizards
        print(bestEnergy)
        f = open("currentOutput", "w")
        string = ""
        for wizard in bestWizards:
            string += wizard + " "
        f.write(string)
        f.close()
        if (bestEnergy == 0):
            print("WOAH")
            sys.exit()
        self.state = bestWizards

     
    def energy(self):
        numFailed = 0
        numPassed = 0
        for constraint in self.constraints:
            wiz_a = self.state.index(constraint[0])
            wiz_b = self.state.index(constraint[1])
            wiz_c = self.state.index(constraint[2])
            if (wiz_a < wiz_c < wiz_b) or (wiz_b < wiz_c < wiz_a):
                numFailed += 1
            else:
                numPassed += 1
        return numFailed

    def get_fitness(self, wizards):
        numFailed = 0
        numPassed = 0
        for constraint in self.immutableconstraints:
            wiz_a = wizards.index(constraint[0])
            wiz_b = wizards.index(constraint[1])
            wiz_c = wizards.index(constraint[2])
            if (wiz_a < wiz_c < wiz_b) or (wiz_b < wiz_c < wiz_a):
                numFailed += 1
            else:
                numPassed += 1
        return numFailed




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
    init_state = startWizards(wizards, constraints)

    op = orderAnnealer(init_state, constraints)
    auto_schedule = op.auto(minutes=5)
    op.set_schedule(auto_schedule) 

    # since our state is just a list, slice is the fastest way to copy
    op.copy_strategy = "slice"
    state, e = op.anneal()

    print("\nNumber Passed: " + str(num_constraints - e))


    return wizards



def pickChild(wizardPriorityQueue, seenWizards):
    rand = random.random()
    if (rand < 0.9):
        fitness, newWizard = heapq.heappop(wizardPriorityQueue)
        pickMutate(newWizard, wizardPriorityQueue, seenWizards)
        return newWizard
    else: 
        index = random.randrange(0, len(wizardPriorityQueue))
        newWizard = wizardPriorityQueue.pop(index)
        pickMutate(newWizard[1], wizardPriorityQueue, seenWizards)
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

def pickMutate(wizards, wizardPriorityQueue, seenWizards):
    rand = random.random()
    rand2 = random.random()
    if rand2 < 0.5:
        wizards = wizards[::-1]
    if (rand < 0.5):
        mutate(wizards, wizardPriorityQueue, seenWizards)
    else: 
        alt_mutate(wizards, wizardPriorityQueue, seenWizards)


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

def alt_mutate(wizards, wizardPriorityQueue, seenWizards):
    for i in range(1, len(wizards)):
        shiftWizard = shiftArray(wizards, i)
        newNumPassed = get_fitness(shiftWizard, constraints)
        if tuple(shiftWizard) not in seenWizards:
                seenWizards.add(tuple(shiftWizard))
                heapq.heappush(wizardPriorityQueue, (num_constraints - newNumPassed, shiftWizard))



def shiftArray(wizards, index):
    wizards = [wizards[index]] + wizards[0:index] + wizards[index + 1:]
    return wizards

def display(wizards, startTime):
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
