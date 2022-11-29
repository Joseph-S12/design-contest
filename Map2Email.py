from CostSim import getMapping

mappingFile = "C:\\Users\\olive\\OneDrive\\Documents\\repositories\\design-contest\\Results\\4by416-30-46-199613.txt"
linesOut=[]
map = getMapping(mappingFile)
subject="EMBS Design Contest 2022 Solution – Group 4 – "+str(map["factorFc"])+" – "+str(map["factorFi"])
print("subject:")
print(subject)
print("body:")
for i in range(54):
    print(i,map[i]%map["meshX"],map[i]//map["meshX"])
