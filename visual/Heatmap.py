import matplotlib.pyplot as plt

tasks_raw = open("tasks.txt").read()
tasks_raw = tasks_raw.split("\n")


tasks = {}
for i in range(len(tasks_raw)):
    tasks[i] = float(tasks_raw[i])
    



links_raw = open("comms.txt").read()
links_raw = links_raw.split("\n")
links = {}
## [from] = [(to,load),]
for l in links_raw:
    temp = l.split(' ')
    try:
        links[int(temp[0])] += [(int(temp[1]),float(temp[2]))]
    except:
        links[int(temp[0])] = [(int(temp[1]),float(temp[2]))]

f = open("mapping.txt").read().split('\n')

x_size,y_size,scaleFc,ScaleFi = tuple(f[0].split(','))

x_size = int(x_size)
y_size = int(y_size)

del(f[0])

processor_map = {}

task_id = 0
for i in f:
    processor_map[task_id] = (int(i)%x_size,int(int(i)/x_size))
    task_id += 1


"""
      ==
      ==
    ==##==
    ==##==
      ==
      ==
"""
output = []

for i in range(x_size*6):
    temp = []
    for j in range(y_size*6):
        temp.append(0.0)
    output.append(temp)

print(processor_map)

## Create a grid containing the following info given the data in tasks and comms for the given mapping
## grid cell format: [totaltaskload,north_link,east_link,south_link,west_link]
## link format     : [in,out]
grid = []
for i in range(x_size):
    temp = []
    for j in range(y_size):
        temp.append([0,[0,0],[0,0],[0,0],[0,0]])
    grid.append(temp)

tasks
def cal_link_route(xs,ys,xt,yt,load):
    ## XY route x first then y
    ## for each link on the route add the cost
    print(xs,ys,xt,yt)
    x = xs
    y = ys
    ##Traverse x first
    while x != xt:
        if(xt-x>0):## East bound
            grid[x][y][2][1]+= load ## Out east
            grid[x+1][y][4][0]+=load ## In west
            x += 1
            print(grid[x][y])
        elif(xt-x<0):## West Bound
            print("West 1")
            grid[x][y][4][1]+=load ## Out west
            grid[x-1][y][2][0]+=load ## In east
            x -= 1
        else: ## finish x traverse
            break
    
    while y != yt:
        if(yt-y>0):## South bound
            grid[x][y][3][1]+=load ## Out south
            grid[x][y+1][1][0]+=load ## In north
            y += 1
        elif(yt-y<0):## West Bound
            grid[x][y][1][1]+=load ## Out north
            grid[x][y-1][3][0]+=load ## In south
            y -= 1
        else: ## finish y traverse
            break
    
    print("----------")



## ----------------------- DISP Section -----------------------
def print_processor_load(x,y,load):
    output[x*6+2][y*6+2] = load
    output[x*6+2][y*6+3] = load
    output[x*6+3][y*6+2] = load
    output[x*6+3][y*6+3] = load

"""
Add the link load to the graph
@x: int x
@y: int y
@load: float load
@in_out: bool inbound connection?
"""

def print_link_east(x,y,load,in_out):
    if(in_out):
        output[x*6+4][y*6+2] = load
        output[x*6+5][y*6+2] = load
    else:
        output[x*6+4][y*6+3] = load
        output[x*6+5][y*6+3] = load

def print_link_west(x,y,load,in_out):
    if(in_out):
        output[x*6][y*6+3] = load
        output[x*6+1][y*6+3] = load
    else:
        output[x*6][y*6+2] = load
        output[x*6+1][y*6+2] = load

def print_link_north(x,y,load,in_out):
    if(in_out):
        output[x*6+2][y*6] = load
        output[x*6+2][y*6+1] = load
    else:
        output[x*6+3][y*6] = load
        output[x*6+3][y*6+1] = load

def print_link_south(x,y,load,in_out):
    if(in_out):
        output[x*6+3][y*6+4] = load
        output[x*6+3][y*6+5] = load
    else:
        output[x*6+2][y*6+4] = load
        output[x*6+2][y*6+5] = load




##-------------------- CALC SECTION --------------------


for tid in processor_map.keys():
    grid[processor_map[tid][0]][processor_map[tid][1]][0] += tasks[tid]## Add task load
    try:
        for l in links[tid]:
            cal_link_route(processor_map[tid][0],processor_map[tid][1],processor_map[l[0]][0],processor_map[l[0]][1],l[1])## Calc link load
    except:
        pass## Atomic task or rx only

## ----------------- Print Section --------------

for x in range(x_size):
    for y in range(y_size):
        print_processor_load(x,y,grid[x][y][0])
        print_link_north(x,y,grid[x][y][1][0],1)
        print_link_north(x,y,grid[x][y][1][1],0)

        print_link_east(x,y,grid[x][y][2][0],1)
        print_link_east(x,y,grid[x][y][2][1],0)

        print_link_south(x,y,grid[x][y][3][0],1)
        print_link_south(x,y,grid[x][y][3][1],0)

        print_link_west(x,y,grid[x][y][4][0],1)
        print_link_west(x,y,grid[x][y][4][1],0)


print(grid[8%x_size][int(8/x_size)])
imgplot = plt.imshow(output)
plt.show()