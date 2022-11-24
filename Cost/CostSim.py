def getData()    
    # Tasks -> list of [id, utilisation]
    # Comms -> list of [id, send, recieve, load]
    Tasks = []
    Comms = []
    with open('tasks.txt', "r") as f:
        Tasks = f.readlines()
    for i in range(len(Tasks)):
        Tasks[i] = [i, Tasks[i]]
    with open('comms.txt', "r") as f:
        Comms = f.readlines()
    for i in range(len(Comms)):
        Comms[i] = [i]+Comms[i].split()
    return Tasks, Comms



def getMapping(mapping="Mapping")
    # Mapping -> dictionary of TaskID:CoreID
    # 
    Mapping = {}
    with open(mapping+'.txt', "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
        



class Core:
    def __init__(self):
        self.usage=0
    
    def addTask(self, utilisation):
        self.usage+=utilisation



class Router:
    def __init__(self):
        self.linkUsage=[]
        self.neighbours=[]
    
    def addTask(self, link, utilisation):
        self.linkUsage[link] += utilisation
    
    def recieveTask(self, destination):