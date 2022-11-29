from ast import Num
from functools import reduce
from CostSim import getCost
from CostSim import reduceFactors
import random
from datetime import datetime
import os
import math
from GravityJump import gravityJump

cur_path = os.path.dirname(__file__)
NUM_TASKS = 54
T0 = 100
T_FINAL = 40
COOLING = 5
I = 50
TAKE_WORSE_RATE=0.00003
INIT_X=5
INIT_Y=3

def storeStep(map,step,loc=cur_path):
    now = now = datetime.now()
    filename=loc+"\\Results\\Animation\\"+str(map["meshX"])+"by"+str(map["meshY"])+str(step)+".txt"
    with open(filename, "w") as f:
        f.write(str(map["meshX"])+","+str(map["meshY"])+","+str(map["factorFc"])+","+str(map["factorFi"])+"\n")
        for i in range(NUM_TASKS):
            f.write(str(map[i])+"\n")



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
    #print(Table)
    return Table



def dropCollumn(map, minline):
    meshX=map["meshX"]
    for i in range(NUM_TASKS):
        if map[i] % meshX >= minline: 
            map[i] -= 1
        map[i] -= map[i]//map["meshX"] # row number
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


def shunt(m, i):
    map = m
    dx = (map["meshX"]/2) - (i%map["meshX"]) # distance to middle x (if positive move right)
    dy = (map["meshX"]/2) - (i//map["meshX"]) # distance to middle y (if positive move down)
    if abs(dy) > abs(dx) :# further away in y axis from middle than the x axis
        if dy < 0:
            for t in range(NUM_TASKS):
                if map[t] == i: map[t]-=map["meshX"] # up one row
        elif dy > 0:
            for t in range(NUM_TASKS):
                if map[t] == i: map[t]+=map["meshX"] # down one row
    elif abs(dx) > abs(dy) : # further away in x axis from middle than the y axis
        if dx < 0:
            for t in range(NUM_TASKS):
                if map[t] == i: map[t]-=1 # left one
        elif dx > 0:
            for t in range(NUM_TASKS):
                if map[t] == i: map[t]+=1# right one
    return map


def simpleSwap(m):
    map = m
    map[random.randint(0,NUM_TASKS-1)] = random.randint(0,map["meshX"]*map["meshY"]-1)
    return map


def modifyMapBySwaps(m, t):
    map = m
    SWAP_RATE=0.1
    for i in range(math.ceil(float(t)*SWAP_RATE)):
        map[random.randint(0,NUM_TASKS-1)] = random.randint(0,map["meshX"]*map["meshY"]-1)
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
            map = None
            # map = shunt(oldMap, random.randint(0, NUM_TASKS-1))
            if random.random() > 0.5:
                map = modifyMapBySwaps(oldMap, t)
            else:
                map = simpleSwap(oldMap)
            cost, overuse=getCost('tasks.txt', 'comms.txt', MappingFileName=None, map=map, returnOveruse=True)
            if overuse == 0:
                maps.append((map, cost, overuse))
                return maps
            if overuse <= oldOveruse and cost <= oldCost:
                storeStep(map,N)
                oldMap = map
                oldOveruse = overuse
                oldCost = cost
                # if overuse == 0:
                #     table = isDropSidePossible(oldMap)
                #     if table[0]: # drop top
                #         #dropRow(oldMap, 0)
                #         dropLine(oldMap, 0, collumn=False)
                #     if table[1]: # drop bottom
                #         #dropRow(oldMap, oldMap["meshX"]-1)
                #         dropLine(oldMap, oldMap["meshX"]-1, collumn=False)
                #     if table[2]: # drop left
                #         #dropCollumn(oldMap, 0)
                #         dropLine(oldMap, 0, collumn=True)
                #     if table[3]: # drop right
                #         #dropCollumn(oldMap, oldMap["meshY"]-1)
                #         dropLine(oldMap, oldMap["meshY"]-1, collumn=True)
            else:
                delta = 1#(oldOveruse-overuse) + (oldCost-cost)
                r = random.random()
                EnergyMagnitude = (t*TAKE_WORSE_RATE)/delta
                #print(EnergyMagnitude)
                if r < EnergyMagnitude:
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
    found = False
    while not found:
        res = anneal()
        for i in res:
            print("size:", i[0]["meshX"]*i[0]["meshY"], "  cost  ", i[1], "   overuse  ", i[2])
            if i[2] == 0:
                found = True
                outmap = reduceFactors('tasks.txt', 'comms.txt', map=i[0])
                storeResults(i[0])

