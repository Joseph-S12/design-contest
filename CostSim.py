import sys
from copy import deepcopy

meshHistory={}

def getData(tname='../tasks.txt', cname='../comms.txt'):
    # Tasks -> list of [id, utilisation]
    # Comms -> list of [id, send, recieve, load]
    Tasks = []
    Comms = []
    with open(tname, "r") as f:
        Tasks = f.readlines()
    for i in range(len(Tasks)):
        Tasks[i] = [int(i), float(Tasks[i].strip())]
    with open(cname, "r") as f:
        Comms = f.readlines()
    for i in range(len(Comms)):
        Comms[i] = [i]+Comms[i].split()
        Comms[i][1]= int(Comms[i][1])
        Comms[i][2]= int(Comms[i][2])
        Comms[i][3]= float(Comms[i][3])
    return Tasks, Comms



def getMapping(name="mapping.txt"):
    # mapping -> dictionary of TaskID:CoreID AND stores meshX, meshY, factorFc, factorFi
    mapping = {}
    with open(name, "r") as f:
        lines = f.readlines()
        info=lines[0].strip().split(",")
        meshX = int(info[0])
        meshY = int(info[1])
        factorFc = float(info[2])
        factorFi = float(info[3])
        mapping["meshX"]=meshX
        mapping["meshY"]=meshY
        mapping["factorFc"]=factorFc
        mapping["factorFi"]=factorFi
        for i in range(1,len(lines)):
            mapping[i-1]=int(lines[i])
            #print(i-1, mapping[i-1])
        print("Mapped", len(lines)-1,"tasks to cores")
        #print(mapping[len(lines)-2])
    return mapping



class Router:
    def __init__(self,i):
        self.id=i
        self.coreUsage=0
        self.l=None
        self.r=None
        self.u=None
        self.d=None
        self.Tx=0
        self.Rx=0
        
    def addTask(self, utilisation):
        self.coreUsage+=utilisation



class Link:
    def __init__(self, s , r):
        self.sender = s
        self.reciever = r
        self.usage = 0
    
    def addTask(self, utilisation):
        self.usage+=utilisation



def generateMesh(x, y):
    def i2xy(index):
        pass
    def xy2i(Xval, Yval):
        return Yval*x + Xval
    routers = [Router(i) for i in range(x*y)]
    links = []
    # for every row there is a link in between each router
    for a in range(y):
        for b in range(x-1):
            sender = routers[xy2i(b,a)]
            reciever = routers[xy2i(b,a)+1]
            links.append(Link(sender,reciever))
            routers[xy2i(b,a)].r=links[-1]
            links.append(Link(reciever,sender))
            routers[xy2i(b,a)+1].l=links[-1]
    # for every row other than the last link very router to the one below
    for a in range(y-1):
        for b in range(x):
            sender = routers[xy2i(b,a)]
            reciever = routers[xy2i(b,a)+x]
            links.append(Link(sender,reciever))
            routers[xy2i(b,a)].d=links[-1]
            links.append(Link(reciever,sender))
            routers[xy2i(b,a)+x].u=links[-1]
    # I know. I know. "that could be one for loop!". Yeah good luck reading that hot mess.
    # I like my double double for loop and you can't take it away from me.
    return routers, links



def mapTasks(Routers, Mapping, Tasks):
    for i in range(len(Tasks)):
        coreId=Mapping[Tasks[i][0]]
        utilisataion=Tasks[i][1]
        Routers[coreId].addTask(utilisataion)



def route(senderX, senderY, senderID, reciverX, reciverY, recieverID, c, Routers, Mapping):
    #print("senderX=", senderX , "   reciverX=", reciverX)
    #print("senderY=", senderY , "   reciverY=", reciverY)
    # first resolve X movement
    dx = senderX - reciverX
    dy = senderY - reciverY
    if dx != 0 and dy != 0:
        Routers[senderID].Tx+=c[3]
        Routers[recieverID].Rx+=c[3]
    if dx > 0:#go left
        for i in range(abs(dx)):
            #print(senderID-i)
            Routers[senderID-i].l.addTask(c[3])
    elif dx < 0:#go left
        for i in range(abs(dx)):
            #print(senderID+i)
            Routers[senderID+i].r.addTask(c[3])
    else:
        pass # do nothing, do not need to move in x plane
    # resolve Y movement
    if dy > 0:#go up
        #print("up", dy)
        for i in range(abs(dy)):
            #print(recieverID+(Mapping["meshX"]*(i+1)))
            Routers[recieverID+(Mapping["meshX"]*(i+1))].u.addTask(c[3])
    elif dy < 0:#go down
        #print("down", dy)
        for i in range(abs(dy)):
            #print(recieverID-(Mapping["meshX"]*(i+1)))
            Routers[recieverID-(Mapping["meshX"]*(i+1))].d.addTask(c[3])
    else:
        pass # do nothing, do not need to move in y plane   



def routeCommsXY(Routers, Mapping, Comms):
    def i2xy(index):
        return index%Mapping["meshX"],index//Mapping["meshX"]
    for c in Comms:
        senderX, senderY = i2xy(Mapping[c[1]])
        reciverX, reciverY = i2xy(Mapping[c[2]])
        route(senderX, senderY, Mapping[c[1]], reciverX, reciverY, Mapping[c[2]], c, Routers, Mapping)



def getCost(TaskFileName='../tasks.txt', CommsFileName='../comms.txt', MappingFileName="mapping.txt", map = None, returnOveruse=False):
    cost = 0
    ts, cs = getData(TaskFileName, CommsFileName)
    if map is None:
        map = getMapping(MappingFileName)
    # for i in map:
        # print(i, type(i), map[i])
    if len(ts)+4 != len(map):
        print("recieved", len(ts), "tasks, but mapping has", len(map)-4, "tasks")
        return sys.maxsize
    rs, ls = generateMesh(map["meshX"],map["meshY"])
    if (not (0 <= map["factorFc"] <= 1.99)) or (not (0 <= map["factorFi"] <= 1.99)):
        print("factors must be >0 and <1.99")
        return sys.maxsize
    mapTasks(rs, map, ts)
    routeCommsXY(rs, map, cs)
    overused = False
    overuse = 0
    # infinite cost if any of the tiles have a scaled usage greater than 1
    for i in range(len(rs)):
        if (rs[i].coreUsage / map["factorFc"]) > 1:
            #print("core connected to router", i, "is overused")
            overused = True
            overuse+=1
        if (rs[i].Tx / map["factorFi"]) > 1:
            #print("Tx link for core", i, "is overused")
            overused = True
            overuse+=1
        if (rs[i].Rx / map["factorFi"]) > 1:
            #print("Rx link for core", i, "is overused")
            overused = True
            overuse+=1
    # infinite cost if any of the links between tiles have a scaled usage greater than 1  
    for i in range(len(ls)):
        if (ls[i].usage / map["factorFi"]) > 1:
            #print("link", i, "(send from", ls[i].sender.id, "and to", ls[i].reciever.id, ")is overused (", ls[i].usage, ")")
            overused = True
            overuse+=1
    if overused:
        if returnOveruse:
            return sys.maxsize, overuse
        return sys.maxsize
    cost = (map["meshY"]*map["meshX"])+map["factorFc"]+map["factorFi"]
    if returnOveruse:
        return cost, overuse
    return cost



def reduceFactors(TaskFileName='../tasks.txt', CommsFileName='../comms.txt', MappingFileName="mapping.txt", map = None):
    ts, cs = getData(TaskFileName, CommsFileName)
    if map is None:
        map = getMapping(MappingFileName)
    if len(ts)+4 != len(map):
        print("recieved", len(ts), "tasks, but mapping has", len(map)-4, "tasks")
        return sys.maxsize
    rs, ls = generateMesh(map["meshX"],map["meshY"])
    if (not (0 <= map["factorFc"] <= 1.99)) or (not (0 <= map["factorFi"] <= 1.99)):
        print("factors must be >0 and <1.99")
        return sys.maxsize
    mapTasks(rs, map, ts)
    routeCommsXY(rs, map, cs)
    mostUsedLink=0
    mostUsedCore=0
    for l in ls:
        if mostUsedLink < l.usage:
            mostUsedLink = l.usage
    for r in rs:
        if mostUsedCore < r.coreUsage:
            mostUsedCore = r.coreUsage
    map["factorFi"] = mostUsedLink
    map["factorFc"] = mostUsedCore
    return map





if __name__ == "__main__":
    print("cost  ",getCost('tasks.txt', 'comms.txt'))
















 







