import sys
import re

def main(argv):
    inputFile = open('inputs/' + argv + '.in', 'r')
    names = createSet(inputFile)
    for line in f:
        names = re.sub("[^\w]", " ", line).split()
        


def createSet(f):
    f.readline()
    f.readline()
    s = set()
    for line in f:
        names = re.sub("[^\w]", " ", line).split()
        for name in names:
            s.add(name)
        if len(s) == 20:
            return s
    return s

        



if __name__ == "__main__":
    main(sys.argv[1])
