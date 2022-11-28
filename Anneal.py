from CostSim import getCost
import random
from math import exp

NUM_TASKS = 54
T0 = 100
T_FINAL = 0
K = 1.380649*(10**-23)
I = 100
TAKE_WORSE_RATE=0.01

def isDropSidePossible(map):
    Table = [True,True,True,True]
    meshX = map["meshX"]
    meshY = map["meshY"]
    # map is TaskID:CoreID
    # We want CoreID:TaskID so we can quickly query to see if there is a task on every core in a row/collumn
    reverseMap={}
    for i in range(NUM_TASKS):
        reverseMap[map[i]] = i
    # is top side empty?
    for i in range(meshX):
        if i in reverseMap:
            Table[0] = False
    # is bottom side empty?
    for i in range(NUM_TASKS-meshX,NUM_TASKS):
        if i in reverseMap:
            Table[1] = False
    # is left side empty?
    # is right side empty?
    return Table

def generateRandomMap():
    mapping = {}
    mapping["meshX"]=10
    mapping["meshY"]=6
    mapping["factorFc"]=1.199
    mapping["factorFi"]=1.199
    for i in range(NUM_TASKS):
        mapping[i] = random.randint(0,mapping["meshX"]*mapping["meshY"]-1)
    return mapping

def modifyMapBySwaps(m, t):
    map = m
    SWAP_RATE=0.1
    for i in range(NUM_TASKS):
        if t*SWAP_RATE < random.uniform(0,100):
            map[i] = random.randint(0,map["meshX"]*map["meshY"]-1)
    return map


def anneal():
    oldMap = generateRandomMap()
    oldCost, oldOveruse=getCost('tasks.txt', 'comms.txt', MappingFileName=None, map=oldMap, returnOveruse=True)
    t=T0
    maps=[(oldMap,oldCost,oldOveruse)]
    while t > T_FINAL:
        print(t)
        N=0
        while N <= I:
            map = modifyMapBySwaps(oldMap, t)
            cost, overuse=getCost('tasks.txt', 'comms.txt', MappingFileName=None, map=map, returnOveruse=True)
            if overuse <= oldOveruse and cost <= oldCost:
                oldMap = map
                oldOveruse = overuse
                oldCost = cost
            else:
                delta = (oldOveruse-overuse) + (oldCost-cost)
                r = random.random()
                EnergyMagnitude = t*TAKE_WORSE_RATE
                #print(EnergyMagnitude)
                if r < EnergyMagnitude:
                    oldMap = map
                    oldOveruse = overuse
                    oldCost = cost
            N+=1
        maps.append((oldMap,oldCost,oldOveruse))
        t-=1
    return maps
            
            
if __name__ == "__main__":
    res = anneal()
    for i in res:
        print("cost  ", i[1], "overuse  ", i[2])