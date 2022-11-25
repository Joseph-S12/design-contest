tasks = open("tasks.txt").read()
tasks = tasks.split("\n")

links_raw = open("comms.txt").read()
links_raw = links_raw.split("\n")
links = []
for l in links_raw:
    temp = l.split(' ')
    links.append((int(temp[0]),int(temp[1]),float(temp[2])))


f = open("mapping.txt").read().split('\n')

x_size,y_size,scaleFc,ScaleFi = tuple(f[0].split(','))

x_size = int(x_size)
y_size = int(y_size)

del(f[0])

processor_map = {}

task_id = 0
for i in f:
    try:
        processor_map[i]=processor_map[i].append(task_id)
    except:
        processor_map[i] = [task_id]
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
        temp.append(0)
    output.append(temp)

print(output)
print(processor_map)


##[totaltaskload,north_link,east_link,south_link,west_link]


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
        output[x*6][y*6+2] = load
        output[x*6+1][y*6+2] = load
    else:
        output[x*6][y*6+3] = load
        output[x*6+1][y*6+3] = load

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
