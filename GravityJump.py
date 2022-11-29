from random import random

## CPU load repels eachother
## Link Load Attracts

## Get Center of gravity of the grid and repell from that
## Direction/angle of repell is based on the attraction of the links

## Should cause heavy load tasks to be split apart and heavy link tasks to attract


def get_load_cog(mapping_in,loads):
    x = 0
    y = 0
    mass = 0
    for i in range(len(loads)):
        x += (mapping_in[i]%mapping_in["meshX"])*loads[i]
        y += int(mapping_in/mapping_in["meshX"])*loads[i]
        mass += loads[i]
    return x/mass, y/mass



def get_link_cog(mapping_in,id,links):
    ## links[index] = (sender,reciever,load)
    x_mass = 0
    y_mass = 0
    total_mass = 0
    total_link = 0
    for i in links:
        if(i[0]==id or i[1] == id):
            xs = mapping_in[i[1]]%mapping_in["meshX"]
            ys = mapping_in[i[1]]/mapping_in["meshX"]

            xt = mapping_in[i[2]]%mapping_in["meshX"]
            yt = mapping_in[i[2]]/mapping_in["meshX"]

            ## Run x_y routing
            x = xs
            y = ys
            ##Traverse x first
            while x != xt:
                if(xt-x>0):## East bound
                    x_mass += x*i[2]
                    total_mass+= i[2]
                    x += 1
                elif(xt-x<0):## West Bound
                    x_mass += x*i[2]
                    total_mass+= i[2]
                    x -= 1
                else: ## finish x traverse
                    break        
            while y != yt:
                if(yt-y>0):## South bound
                    y_mass += y*i[2]
                    total_mass+= i[2]
                    y += 1
                elif(yt-y<0):## West Bound
                    y_mass += y*i[2]
                    total_mass+= i[2]
                    y -= 1
                else: ## finish y traverse
                    break
            total_link += i[2]     
    if total_link == 0:
        return mapping_in[i[1]]%mapping_in["meshX"], mapping_in[i[1]]/mapping_in["meshX"], 0
    else:
        return x_mass/total_mass,y_mass/total_mass,total_link

        



## Apply a repel force to the task given the load. Apply a attraction force to the load given the link
## With the given vector plot a line
## 
def get_jump_location(mapping_in,id,loads,links,prob):

    x,y = mapping_in[id]%mapping_in["meshX"], mapping_in[id]/mapping_in["meshX"]

    x_link, y_link, total_link = get_link_cog(mapping_in,id,links)
    x_load, y_load = get_load_cog(mapping_in,loads)

    xv = ((x-x_load)*loads[id]+(x_link-x)*total_link)/(loads[id]+total_link)
    yv = ((y-y_load)*loads[id]+(y_link-y)*total_link)/(loads[id]+total_link)

    ## Chance of moving
    if random()<=prob:
        if(xv > yv):
            if(xv<0):
                if(x!=0):
                    x -= 1
                else:
                    pass
            else:
                if(x!=mapping_in["meshX"]-1):
                    x += 1
                else:
                    pass
        else:
            if(yv<0):
                if(y!=0):
                    y -= 1
                else:
                    pass
            else:
                if(y!=mapping_in["meshY"]-1):
                    y += 1
                else:
                    pass
    
    return x,y
    


