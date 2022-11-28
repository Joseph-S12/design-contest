from CostSim import getCost
import random
from math import exp

NUM_TASKS = 54
T0 = 100
T_FINAL = 0
K = 1.380649*(10**-23)
Is = 100
TAKE_WORSE_RATE=0.01

def generateRandomMap():
    mapping = {}
    mapping["meshX"]=10
    mapping["meshY"]=6
    mapping["factorFc"]=1.199
    mapping["factorFi"]=1.199
    for i in range(NUM_TASKS):
        mapping[i] = random.randint(0,mapping["meshX"]*mapping["meshY"]-1)
    return mapping

def modifyMapBySwaps(map, t):
    SWAP_RATE=0.1
    for i in range(NUM_TASKS):
        if t*SWAP_RATE < random.random(100):
            map[i] = random.randint(0,map["meshX"]*map["meshY"]-1)


def anneal():
    oldMap = generateRandomMap()
    oldCost, oldOveruse=getCost('tasks.txt', 'comms.txt', MappingFileName=None, map=oldMap, returnOveruse=True)
    t=T0
    maps=[oldMap]
    while t > T_FINAL:
        print(t)
        N=0
        while N <= Is:
            map = generateRandomMap()
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
        maps.append(oldMap)
        t-=1
    return oldMap, oldCost, oldOveruse
            
            
if __name__ == "__main__":
    print (anneal())