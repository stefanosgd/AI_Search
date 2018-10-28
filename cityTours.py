import re
import numpy as np

def readFile(fName):
    newFile = open(fName, 'r')
    name = []
    intData = [] 
    name = newFile.read().replace('\n','').split(',')[1:]   
    for x in name:
        if not x.isnumeric():
            x = re.sub('\D','', x)
        intData.append(int(x))
    size = intData[0]
    intData = intData[1:]
    return(intData, size)

def printArray(a):
    for x in a:
        print(x)

def toArray(size, cityData):
    cities = createEmpty(size)
    print(cityData)
    print(size)
    count = 0
    for i in range(0, size-1):
        for j in range(i+1, size):
            #print(cityData[i])
            cities[i][j] = cityData[count]
            cities[j][i] = cityData[count]
            count += 1
    print(np.matrix(cities))

def createEmpty(s):
    return [[0 for x in range(0,s)]for y in range(0,s)]

def run():    
    data, size = readFile('AISearchtestcase.txt')
    toArray(size, data)
