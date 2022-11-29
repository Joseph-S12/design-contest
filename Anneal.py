from CostSim import getCost
import random
from datetime import datetime
import os

cur_path = os.path.dirname(__file__)
NUM_TASKS = 54
T0 = 100
T_FINAL = 0
COOLING = 1
I = 100
TAKE_WORSE_RATE=0.05
INIT_X=4
INIT_Y=5



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
    print('o',end='')
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
    mapping["meshX"]=INIT_X
    mapping["meshY"]=INIT_Y
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
        print(t)
        N=0
        while N <= I:
            map = modifyMapBySwaps(oldMap, t)
            cost, overuse=getCost('tasks.txt', 'comms.txt', MappingFileName=None, map=map, returnOveruse=True)
            if overuse == 0:
                maps.append((map, cost, overuse))
            if overuse <= oldOveruse and cost <= oldCost:
                oldMap = map
                oldOveruse = overuse
                oldCost = cost
                if overuse == 0:
                    table = isDropSidePossible(oldMap)
                    if table[0]: # drop top
                        #dropRow(oldMap, 0)
                        dropLine(oldMap, 0, collumn=False)
                    if table[1]: # drop bottom
                        #dropRow(oldMap, oldMap["meshX"]-1)
                        dropLine(oldMap, oldMap["meshX"]-1, collumn=False)
                    if table[2]: # drop left
                        #dropCollumn(oldMap, 0)
                        dropLine(oldMap, 0, collumn=True)
                    if table[3]: # drop right
                        #dropCollumn(oldMap, oldMap["meshY"]-1)
                        dropLine(oldMap, oldMap["meshY"]-1, collumn=True)
            else:
                delta = (oldOveruse-overuse) + (oldCost-cost)
                r = random.random()
                EnergyMagnitude = t*TAKE_WORSE_RATE
                #print(EnergyMagnitude)
                if r*delta < EnergyMagnitude:
                    oldMap = map
                    oldOveruse = overuse
                    oldCost = cost
            N+=1
        maps.append((oldMap,oldCost,oldOveruse))
        t-=COOLING
    return maps


def storeResults(map, loc=cur_path):
    now = now = datetime.now()
    filename=loc+"\\Results\\"+str(map["meshX"])+"by"+str(map["meshY"])+now.strftime("%H-%M-%S-%f")+".txt"
    with open(filename, "w") as f:
        f.write(str(map["meshX"])+","+str(map["meshY"])+","+str(map["factorFc"])+","+str(map["factorFi"])+"\n")
        for i in range(NUM_TASKS):
            f.write(str(map[i])+"\n")

            
if __name__ == "__main__":
    res = anneal()
    for i in res:
        print("size:", i[0]["meshX"]*i[0]["meshY"], "  cost  ", i[1], "   overuse  ", i[2])
        if i[2] == 0:
            storeResults(i[0])
            break