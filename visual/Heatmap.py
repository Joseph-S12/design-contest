


grid = (8,7)

tasks = open("tasks.txt").read()
tasks = tasks.split("\n")

links_raw = open("comms.txt").read()
links_raw = links_raw.split("\n")
links = []
for l in links_raw:
    temp = l.split(' ')
    links.append((int(temp[0]),int(temp[1]),float(temp[2])))


processor_map = []

for i in range(grid[0]):
    temp =[]
    for j in range(grid[1]):
        temp.append(-1)
    processor_map.append(temp)


    