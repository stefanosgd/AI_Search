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
    return cities

def createTourGreedy(size, cityDistance):
    tour = createEmptyTour(size)
    currentCity=0
    shortest = 100000
    nextCity = 0
    visited = 0
    tourLength = 0
    while (visited<size-1):
        print(currentCity+1 , ",")
        for i in range(0,size):
           # print(cityDistance[currentCity][i])
            if ((cityDistance[currentCity][i] < shortest) & (currentCity != i)):
                if (tour[i] == 0):
                    shortest = cityDistance[currentCity][i]
                    nextCity = i
        tour[currentCity] = nextCity
        currentCity = nextCity
        tourLength += shortest
        shortest = 100000
        visited += 1
        #print(visited)
    tourLength += cityDistance[currentCity][0]
    print(currentCity+1)
    print()
    print(tourLength)

def createEmptyTour(s):
    return [0 for x in range(0,s)]

def createEmpty(s):
    return [[0 for x in range(0,s)]for y in range(0,s)]

def run():    
    data, size = readFile('NEWAISearchfile026.txt')
    cities = toArray(size, data)
    createTourGreedy(size, cities)
