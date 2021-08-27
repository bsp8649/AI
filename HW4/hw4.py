import pandas as pd
import numpy as np
from scipy.stats import entropy
import math

class Node:
    def __init__(self, bools=None, abClass=None):
        self.bools = bools
        abClass = abClass

def read():
    nodelist = []
    filepath = 'dtree-data'
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            node = Node()
            x = []
            bools = line.split()
            for i in range (0, 7):
                x.append(bools[i])
            node.bools = x
            node.abClass = bools[8]
            nodelist.append(node)
            line = fp.readline()
    return nodelist

def entropy(p):
    part1 = -p*math.log2(p)
    comp = 1-p
    part2 = -(comp)*math.log2(comp)
    return part1 + part2
    

def cEntropy(i, nodes, abClass):
    values = []
    truecount = 0
    count = 0
    for node in nodes:
        if node.abClass == abClass:
            value = node.bools[i]
            if (value == "True"):
                truecount += 1
            count += 1
    p = float(truecount)/float(count)
    cEntropy = entropy(p)
    return cEntropy

def main():
    nodelist = read()
    data = 'dtree-data'
    for i in range(0, 7):
        print("Information Gain Values for Column", i)
        cE1 = cEntropy(i, nodelist, 'B')
        ig1 = 1 - cE1
        print(i, cE1)
        print(".........")
        for j in range(0, 7):
            if i == j:
                continue
            cE2 = cEntropy(j, nodelist, 'B')
            ig2 = cE1 - cE2
            print(i, j, ig2)


if __name__ == "__main__":
    main()
