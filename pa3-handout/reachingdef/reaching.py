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
        
    print(basicBlocks)
    print(edges)



if __name__ == "__main__":
    main()