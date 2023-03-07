#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os


class FaintVarAnalysis:
    def __init__(self, problem=""):
        self.numVariables = 0
        self.numBlocks = 0 
        self.numEdges = 0 
        self.entry = 0
        self.exit = 0
        self.basicBlocks = {}
        self.edges = {}
    
    def setProblem(self, problem:str):
        split = problem.split()
        self.numVariables = int(split[1]) # Variables labeled 1 to V
        self.numBlocks = int(split[2]) # Blocks labeled 1 to B
        self.numEdges = int(split[3])
        self.entry = int(split[4])
        self.exit = int(split[5])

    def setBasicBlock(self, problem:str):
        split = problem.split()
        # Each line is either “b i”, “b i l”, or “b i l r1 . . . rn” (1 ≤ i ≤ B, 0 ≤ l ≤ V , and 1 ≤ rk ≤ V ).
        # If “b i”, basic block i is empty.
        # If “b i l”, basic block i contains a definition that assigns a #constant to the variable l (l is never a zero for this case).
        # If “b i l r1 . . . rn” and l is not zero, basic block i contains a definition, l = r1 + . . . + rn;. If l is zero, basic block
        # i contains a print statement, print(r1, . . . , rn);.
        # i: basic block number
        split = split[1:]
        split = [int(i) for i in split]
        command = len(split)

        if command == 1:
            self.basicBlocks[(int(split[0]))] = []
        if command == 2:
            self.basicBlocks[(int(split[0]))] = [(int(split[1]))]
        if command >= 3:
            self.basicBlocks[(int(split[0]))] = split[1:]
    
    def setEdge(self, problem:str):
        split = problem.split()
        split = split[1:]
        split = [int(i) for i in split]
        if split[0] in self.edges:
            self.edges[int(split[0])].append(int(split[1]))
        else:
            self.edges[int(split[0])] = [int(split[1])]
        
    
def doAnalysis(analysis: FaintVarAnalysis):

    # Initialize IN and OUT for all n to all variables
    Out = {}
    In = {}
    VAR = list(range(1, analysis.numVariables+1))

    for b in range(1, analysis.numBlocks+1):
        Out[b] = VAR
        In[b] = VAR
    
    changed = True
    ctr = 0
    
    while (changed):
        changed = False
        # For each basic block other than exit
        for b in range(analysis.numBlocks, 0, -1):
            tempIn = In[b]

            curBlock = analysis.basicBlocks[b]
            constGen = []
            depGen = [] # Always empty set
            constKill = []
            depKill = []

            
            
            if len(curBlock) == 1:
                constGen.append(curBlock[0])
            elif len(curBlock) > 1 and curBlock[0] != 0:
                equal = False
                for x in curBlock[1:]:
                    if x == curBlock[0]:
                        equal = True
                if not equal:
                    constGen.append(curBlock[0])

            gen = list(set(constGen).union(set(depGen)))

            if len(curBlock) > 1 and curBlock[0] == 0:
                for x in curBlock[1:]:
                    constKill.append(x)

            # depKill
            if len(curBlock) > 1 and curBlock[0] != 0:
                operands = []
                if curBlock[0] not in Out[b]:
                    for x in curBlock[1:]:
                        operands.append(x)
                depKill = list(set(operands).intersection(set(VAR)))
            

            kill = list(set(constKill).union(set(depKill)))
            
            # if (None in list((set(Out[b]).difference(kill)))):
            #     print("None is in Out[b] - kill: ")
            #     print("Current Iteration: " + str(ctr) + "   Current Block: " + str(curBlock))
            #     print("Out[b]" + str(Out[b]))
            #     print("kill: " + str(kill))
            #     print()

            In[b] = list((set(Out[b]).difference(kill)).union(set(gen)))
            # In[b] = list(set(Out[b]).union(set(gen)))
            

            # Out equation
            if b == analysis.exit:
                Out[b] = VAR
            else:
                first = True
                intersect = []
                for e in analysis.edges[b]:
                    if first:
                        first = False
                        intersect = In[e]
                        # print(intersect)
                    else:
                        intersect = list(set(intersect).intersection(set(In[e])))
                Out[b] = intersect
            
            if In[b] != tempIn:
                changed = True
                ctr += 1
            
    return [In, Out]






def readFile() -> FaintVarAnalysis:
    input = FaintVarAnalysis()
    f = open(sys.argv[1])
    for x in f:
        if x[0] == 'c':
            pass
        elif x[0] == 'p': 
            input.setProblem(x)
        elif x[0] == 'b':
            input.setBasicBlock(x)
        elif x[0] == 'e':
            input.setEdge(x)
        else:
            print('unknown error')
            exit(0) 
    f.close()
    return input

def writeToFile(filename, In: dict):
    f = open(filename, "w")
    # for pair in pointsTo:
    #     f.write('pt ' + str(pair[0]) + ' ' +  str(pair[1]) + '\n')
    for key in In.keys():
        f.write('fvin ' + str(key))
        for i in In[key]:
            f.write(' ' + str(i))
        f.write('\n')
    f.close()

def main():
    if (len(sys.argv) != 3):
        print("usage: alg.py infile outfile")
        exit(0)
    
    input = readFile()
    outputfile = sys.argv[2]
    # print(input.basicBlocks)
    [In, Out] = doAnalysis(input)
    print(In)
    writeToFile(outputfile, In)
    # print(Out)
    
    return 0

if __name__ == "__main__":
    main()