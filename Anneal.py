from CostSim import getCost
import random
from math import exp



NUM_TASKS = 54
T0 = 50
T_FINAL = 0
K = 1.380649*(10**-23)
I = 200
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
    for i in range((meshX*meshY)-meshX, meshX*meshY):
        if i in reverseMap:
            Table[1] = False
    # is left side empty?
    for i in range(0, meshX*meshY, meshX):
        if i in reverseMap:
            Table[2] = False
    # is right side empty?
    for i in range(meshX-1, meshX*meshY, meshX):
        if i in reverseMap:
            Table[3] = False
    return Table



def dropCollumn(map, minline):
    meshX=map["meshX"]
    for i in range(NUM_TASKS):
        if map[i] % meshX >= minline: 
            map[i] -= 1
        map[i] -= i//map["meshX"] # row number
    map["meshX"] -= 1



def dropRow(map, minline):
    meshX=map["meshX"]
    for i in range(NUM_TASKS):
        if map[i] >= (minline+1)*meshX: 
            map[i] -= meshX
    map["meshY"] -= 1



def dropLine(map, minline, collumn):
    if collumn:
        dropCollumn(map, minline)
    else:
        dropRow(map, minline)



def getMinimallyActiveLine(map):
    def xy2i(Xval, Yval):
        return Yval*x + Xval
    mintotal = 0
    minline = 0
    collumn = False
    meshX=map["meshX"]
    meshY=map["meshY"]
    # map is TaskID:CoreID
    # We want CoreID:TaskID so we can quickly query to see if there is a task on every core in a row/collumn
    reverseMap={}
    for i in range(NUM_TASKS):
        reverseMap[map[i]] = i
    # look at every row
    for y in range(meshY):
        total = 0
        for x in range(meshX):
            if xy2i(x,y) in reverseMap: total +=1
        if total < mintotal: minline = y
    # look at every collumn
    for x in range(meshX):
        total = 0
        for y in range(meshY):
            if xy2i(x,y) in reverseMap: total +=1
        if total < mintotal:
            minline = y
            collumn = True
    return minline, collumn

            


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
        if float(t)*SWAP_RATE < random.uniform(0,100):
            map[i] = random.randint(0,map["meshX"]*map["meshY"]-1)
    return map


def anneal():
    oldMap = generateRandomMap()
    oldCost, oldOveruse=getCost('tasks.txt', 'comms.txt', MappingFileName=None, map=oldMap, returnOveruse=True)
    t=T0
    maps=[(oldMap,oldCost,oldOveruse)]
    while t > T_FINAL:
        N=0
        while N <= I:
            map = modifyMapBySwaps(oldMap, t)
            cost, overuse=getCost('tasks.txt', 'comms.txt', MappingFileName=None, map=map, returnOveruse=True)
            if overuse <= oldOveruse and cost <= oldCost:
                oldMap = map
                oldOveruse = overuse
                oldCost = cost
                if overuse == 0:
                    table = isDropSidePossible(oldMap)
                    if table[0]:
                        dropRow(oldMap, 0)
                    if table[1]:
                        dropRow(oldMap, oldMap["meshX"]-1)
                    if table[2]:
                        dropCollumn(oldMap, 0)
                    if table[3]:
                        dropCollumn(oldMap, oldMap["meshY"]-1)
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
        print("size:", i[0]["meshX"]*i[0]["meshX"], "  cost  ", i[1], "   overuse  ", i[2])