from cmath import sqrt
import sys
import time

time_start = time.time()

class Node:
    def __init__ (self, name, coord, section):
        self.name = name
        self.coord = coord
        self.section = section
        self.visited = 0

arrayNodes = []
instancesFile = sys.argv[1] # Passar o arquivo com a instancia
                            # como primeiro argumento da chamada
                            # python instancia.txt tsp.py

def readFromFile ():
    f1 = open (instancesFile)
    i = 0
    lines = len(f1.readlines())
    f1.seek(0)
    for i in range (lines):
        tmpName, tmpCoord, tmpSection = f1.readline().split()
        Name = int(tmpName)
        Coord = float(tmpCoord)
        Section = float(tmpSection)
        arrayNodes.append(Node(Name, Coord, Section))
        i += 1
    f1.close()

readFromFile()

def dist (i, j): # Returns the Euclidean distance between 2 nodes (From global arrayNodes)
    distance =  sqrt( ((arrayNodes[j].coord-arrayNodes[i].coord)**2) + ((arrayNodes[j].section-arrayNodes[i].section)**2) )
    return distance.real

def distFromSeq (arraySeq): # Calcula a distancia de uma solução no formato de uma sequencia (arraySeq)
    distance = 0
    for i in range (0, len(arrayNodes)-1):
        distance = distance + dist (arraySeq[i],  arraySeq[i+1])
    return distance

arraySeq = [0]

def tspClosest (startingNode, currentNode): # Heurística Construtiva, vizinho mais proximo

    if arrayNodes[currentNode].visited == 1 and currentNode == startingNode: 
        return 0
    else:
        arrayNodes[currentNode].visited = 1
        minDist = float ('inf')
        nextNode = 0
        for i in range (0, len(arrayNodes)):
            if arrayNodes[i].visited == 1:
                pass
            else:
                currDist = dist(currentNode, i)
                if currDist < minDist:
                    minDist = currDist
                    nextNode = i
        if minDist == float('inf'): # Pra tirar a última iteração que soma float('inf')
            minDist = 0
        arraySeq.append(nextNode)
        return (minDist + tspClosest (startingNode, nextNode))

def twoOpt (improvementThreshold, arraySeq): #2-Opt (improvment threshold = 0)
    improvementFactor = 1
    bestDistance = distFromSeq (arraySeq)
    while improvementFactor > improvementThreshold:
        distanceToBeat = bestDistance
        for swapFirst in range (1, len(arraySeq)-2):
            for swapLast in range (swapFirst+1, len(arraySeq)-1):
                newRoute = arraySeq
                tmpNode = newRoute[swapFirst]
                newRoute[swapFirst] = newRoute[swapLast]
                newRoute[swapLast] = tmpNode
                newDistance = distFromSeq (newRoute)
                if newDistance < bestDistance:
                    arraySeq = newRoute
                    bestDistance = newDistance
        improvementFactor = 1 - (bestDistance/distanceToBeat)
    return bestDistance, arraySeq

minimumDistance = tspClosest (0, 0)
distanceFromSeq = distFromSeq (arraySeq)
print ("Vizinho mais próximo:", round(minimumDistance, 0)) 

newMinimumDistance, newArraySeq = twoOpt (0, arraySeq)
print ("Vizinho mais próximo + 2-Opt:", round(newMinimumDistance, 0))

time_end = time.time()
print ("Tempo de execução:",round(time_end - time_start, 2))