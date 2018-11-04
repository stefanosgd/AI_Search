import re
import numpy as np
import math
import random
import time

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
    count = 0
    for i in range(0, size-1):
        for j in range(i+1, size):
            #print(cityData[i])
            cities[i][j] = cityData[count]
            cities[j][i] = cityData[count]
            count += 1
    return cities

def createEmpty(s):
    return [[0 for x in range(0,s)]for y in range(0,s)]

class SimAnneal:
    def __init__(self, startingCity, cities, size, T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):
        self.cities = cities
        self.N = size
        self.T = math.sqrt(self.N) if T == -1 else T
        self.alpha = 0.9995 if alpha == -1 else alpha
        self.stopping_temperature = 0.00000000000001 if stopping_T == -1 else stopping_T
        self.stopping_iter = 1 if stopping_iter == -1 else stopping_iter
        self.iteration = 1

        self.dist_matrix = self.cities
        self.nodes = [i for i in range(self.N)]

        self.cur_solution = self.initial_solution(startingCity)
        self.best_solution = list(self.cur_solution)

        self.cur_fitness = self.fitness(self.cur_solution)
        self.initial_fitness = self.cur_fitness
        self.best_fitness = self.cur_fitness

        self.fitness_list = [self.cur_fitness]

    def initial_solution(self, start):
        """
        Greedy algorithm to get an initial solution (closest-neighbour)
        """
        cur_node = start
        solution = [cur_node]
        closest_dist = 100000
        free_list = list(self.nodes)
        free_list.remove(cur_node)
        while free_list:
            for j in free_list:
                if (self.dist_matrix[cur_node][j] < closest_dist):
                    closest_dist = self.dist_matrix[cur_node][j]
                    next_node = j
            cur_node = next_node
            free_list.remove(cur_node)
            solution.append(cur_node)
            closest_dist = 100000
        return solution

    def fitness(self, sol):
        """ Objective value of a solution """
        return round(sum([self.dist_matrix[sol[i - 1]][sol[i]] for i in range(1, self.N)]) +
                     self.dist_matrix[sol[0]][sol[self.N - 1]], 4)

    def p_accept(self, candidate_fitness):
        """
        Probability of accepting if the candidate is worse than current
        Depends on the current temperature and difference between candidate and current
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.T)

    def accept(self, candidate):
        """
        Accept with probability 1 if candidate is better than current
        Accept with probabilty p_accept(..) if candidate is worse
        """
        candidate_fitness = self.fitness(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness = candidate_fitness
            self.cur_solution = candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness = candidate_fitness
                self.best_solution = candidate

        else:
            if random.random() < self.p_accept(candidate_fitness):
                self.cur_fitness = candidate_fitness
                self.cur_solution = candidate

    def anneal(self):
        """
        Execute simulated annealing algorithm
        """
        while self.T >= self.stopping_temperature and self.iteration < self.stopping_iter:
            candidate = list(self.cur_solution)
            l = random.randint(2, self.N - 1)
            i = random.randint(0, self.N - l)
            candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
            self.accept(candidate)
            self.T *= self.alpha
            self.iteration += 1
            self.fitness_list.append(self.cur_fitness)

##        if self.T <= self.stopping_temperature:
##            print('Min temperature reached')
##        elif self.iteration == self.stopping_iter:
##            print('Max iterations reached')
        return self.best_fitness, self.best_solution


def run():
    start_time = time.time()
    data, size = readFile('C:/Users/Stefanos Demetriou/Documents/Year 2/Software Methodologies/AI Search/Assignment/NEWAISearchfile535.txt')
    cities = toArray(size, data)
    print(np.matrix(cities))
    best = 10000000
    best_tour = []
    for i in range(size):
##        print(i)
        sa = SimAnneal(i, cities, size, stopping_iter = 100000)
        current, current_tour = sa.anneal()
        if current < best:
            best = current
            best_tour = current_tour
    print('The best one is ', best)
    for i in range(size):
        print((best_tour[i]+1), end=",")
    print()
    print('This took', time.time() - start_time, 'to run')
        
