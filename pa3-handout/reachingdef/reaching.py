#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

def main():
    if (len(sys.argv) != 3):
        print("usage: alg.py infile outfile")
        exit(0)

    f = open(sys.argv[1])
    problem = []
    basicBlocks = {}
    edges = {}
    for x in f:
        #print(x)


        if x[0] == "p":

            #problem[0] = V variables
            #problem[1] = B basic blocks
            #problem[2] = E edges
            #problem[3] = entry node
            #problem[4] = exit node

            spli = x.split()
            for a in spli:
                problem.append(a)
            problem = problem[1:]

        if x[0] == "b":

            spli = x.split()
            spli = spli[1:]
            spli = [int(i) for i in spli]
            command = len(spli)

            if command == 1:
                basicBlocks[(int(spli[0]))] = [None]
            if command == 2:
                basicBlocks[(int(spli[0]))] = [(int(spli[1]))]
            if command >= 3:
                basicBlocks[(int(spli[0]))] = spli[1:]

        if x[0] == "e":
            spli = x.split()
            spli = spli[1:]
            spli = [int(i) for i in spli]
            if spli[0] in edges:
                edges[spli[0]].append(spli[1])
            else:
                edges[spli[0]] = [spli[1]]

        if x[0] == "c":
            pass

    print("Basic Blocks:")
    print(basicBlocks)

    print("\nEdges:")
    print(edges)

    #get predecesors.
    #look for value within the value of edges

    preds = {}
    for x in list(basicBlocks.keys()):
        preds[x] = [None]
    for x in list(basicBlocks.keys()):
        for y in list(edges.keys()):
            for z in edges[y]:
                if z == x:
                    if x in preds.keys():
                        preds[x].append(y)
                    else:
                        preds[x] = [y]

    for x in list(preds.keys()):
        if len(preds[x])>1:
            preds[x] = preds[x][1:]
    
    print("\nPredecesors:")
    print(preds)


    #get gen sets

    gen = {}
    for x in list(basicBlocks.keys()):
        if len(basicBlocks[x]) == 1:
            if basicBlocks[x][0] == None:
                #print("fuihasfasd")
                gen[x] = [basicBlocks[x][0]]
            else:
                gen[x] = [basicBlocks[x][0]]
        elif basicBlocks[x][0] == 0:
                gen[x] = [None]
        else:
                gen[x] = [basicBlocks[x][0]]
    for x in list(gen.keys()):
        for y in gen[x]:
            if y == None:
                gen[x] = []
    print("\nGen sets:")
    print(gen)

    #gen for calc
    genC = {}
    for x in list(basicBlocks.keys()):
        if len(basicBlocks[x]) == 1:
            if basicBlocks[x][0] == None:
                #print("fuihasfasd")
                genC[x] = [basicBlocks[x][0]]
            else:
                genC[x] = [x]
        elif basicBlocks[x][0] == 0:
                genC[x] = [None]
        else:
                genC[x] = [x]
    for x in list(genC.keys()):
        for y in genC[x]:
            if y == None:
                genC[x] = []
    print("\genC sets:")
    print(genC)




    #? is this wrong
    #gen[3] = [3]
    #gen[4] = [4]
    #get kill

    kill = {}
    for x in list(basicBlocks.keys()):
        kill[x] = [None] 
    for x in list(basicBlocks.keys()):
        for y in list(gen.keys()):
            if y == x:
                pass
            else:
                for z in gen[x]:
                    for z1 in gen[y]:
                        if z == z1 and z == None:
                            kill[x] = [None]
                        elif z == z1:
                            if x in kill.keys():
                                kill[x].append(y)
                            else:
                                kill[x] = [y]
    for x in list(kill.keys()):
        if len(kill[x])>1:
            kill[x] = kill[x][1:]
        else:
            kill[x] = []

    print("\nKill sets:")
    print(kill)

    #gen[3] = [3]
    #gen[4] = [4]
    #iterative algorithm for reaching definitions
    OUT = {}
    IN = {}
    for x in list(basicBlocks.keys()):
        OUT[x] = []
        IN[x] = []

    changed = True
    while(changed):
        changed = False
        for x in list(basicBlocks.keys()):
            temp = OUT[x]
            union = []
            for elem in preds[x]:
                if elem == None:
                    pass
                else:
                    union.append(OUT[elem])
            union = [item for sublist in union for item in sublist]
            union = set(union)
            IN[x] = union
            
            #gen[x] union (IN[x] - kill[x])
            #IN[B] - kill[B]
            inMinusKill = (set(IN[x]) - set(kill[x]))
            OUT[x] = list(set(genC[x]).union(set(inMinusKill)))


            #OUT[x] = #genB union (IN[B] - killB)
            if temp == OUT[x]:
                changed = False
            else: 
                changed = True

    print(OUT)

    #create file and write to it


    f = open(sys.argv[2], "w")
    for x in OUT:
        print(x)
        print(OUT[x])
        f.write('rdout ' + str(x))
        for i in OUT[x]:
            f.write(' '+ str(i))
        f.write('\n')
    f.close()
    #for x in OUT:
        #f.write('rdout ')
    #for pair in pointsTo:
    #    f.write('pt ' + str(pair[0]) + ' ' +  str(pair[1]) + '\n')
    #f.close()


if __name__ == "__main__":
    main()