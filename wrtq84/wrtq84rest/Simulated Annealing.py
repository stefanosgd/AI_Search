import re
import math
import random
import time
import numpy as np


def read_file(f_name):
    new_file = open(f_name, 'r')
    int_data = []
    name = new_file.read().replace('\n', '').split(',')[1:]
    for x in name:
        if not x.isnumeric():
            x = re.sub('\D', '', x)
        int_data.append(int(x))
    size = int_data[0]
    int_data = int_data[1:]
    return int_data, size

"""
This function writes the best tour to its' respective file. To prevent any errors
from occuring upon submission this has been commented out, and the best tour and length
are simply output instead
"""
# def write_file(f_name, size, best, best_tour):
#     new_file = open("/TourfileA/tourNEW"+f_name+".txt", 'w+')
#     new_file.write("NAME = " + f_name + ",")
#     new_file.write("\nTOURSIZE = " + str(size) + ",")
#     new_file.write("\nLENGTH = " + str(best) + ",\n")
#     for i in range(size):
#         new_file.write(str(best_tour[i]+1)+",")


def to_array(size, city_data):
    cities = create_empty(size)
    count = 0
    for i in range(0, size-1):
        for j in range(i+1, size):
            cities[i][j] = city_data[count]
            cities[j][i] = city_data[count]
            count += 1
    return cities


def create_empty(s):
    return [[0 for x in range(0, s)]for y in range(0, s)]


class SimulatedAnneal:
    def __init__(self, cities, size):
        self.iterations = 0
        self.cur_fitness = 0
        self.cities = cities
        self.file_size = size
        self.temp = math.sqrt(np.sum(self.cities))
        # self.temp = 100
        self.alpha = 0.99999
        
        self.dist_matrix = self.cities
        self.nodes = [i for i in range(self.file_size)]

        starting_city = random.choice(self.nodes)
        self.cur_fitness = 0
        self.cur_solution = self.initial_solution(starting_city)
        self.best_solution = list(self.cur_solution)
        self.best_fitness = self.cur_fitness

    def initial_solution(self, start):
        """
        Uses a random algorithm to find the initial solution
        The passed variable determines what the initial city for the tour is
        """
        cur_node = start
        solution = [cur_node]
        free_list = list(self.nodes)
        free_list.remove(cur_node)
        while free_list:
            cur_node = random.choice(free_list)
            free_list.remove(cur_node)
            solution.append(cur_node)
            self.cur_fitness += self.dist_matrix[cur_node][solution[-2]]
        self.cur_fitness += self.dist_matrix[solution[-1]][solution[0]]
        return solution

    def new_fitness(self, sol, i, l):
        """
        Uses the old fitness, along with the 2 edges that have changed, to calculate the new fitness
        in a much faster time than the initial function for calculating the length of a tour
        """
        swapped1 = i
        swapped2 = l
        if swapped2 == self.file_size-1:
            remove = self.dist_matrix[self.cur_solution[swapped1 - 1]][self.cur_solution[swapped1]] \
                     + self.dist_matrix[self.cur_solution[swapped2]][self.cur_solution[0]]
            add = self.dist_matrix[sol[swapped1 - 1]][sol[swapped1]] + self.dist_matrix[sol[swapped2]][sol[0]]
            attempt = self.cur_fitness - remove + add
        else:
            remove = self.dist_matrix[self.cur_solution[swapped1 - 1]][self.cur_solution[swapped1]] \
                     + self.dist_matrix[self.cur_solution[swapped2+1]][self.cur_solution[swapped2]]
            add = self.dist_matrix[sol[swapped1 - 1]][sol[swapped1]] + self.dist_matrix[sol[swapped2+1]][sol[swapped2]]
            attempt = self.cur_fitness - remove + add
        return attempt

    def p_accept(self, candidate_fitness):
        """
        Calculates the probability that a candidate will be accepted if it is worse than the current best
        This depends on the temperature and difference between candidate and current
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.temp)

    def accept(self, candidate, i, l):
        """
        A candidate is accepted if it is better than the current best
        If it is worse, the probability to be accepted is calculated with p_accept
        """
        candidate_fitness = self.new_fitness(candidate, i, l)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness = candidate_fitness
            self.cur_solution = candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness = candidate_fitness
                self.best_solution = candidate
        elif random.random() < self.p_accept(candidate_fitness):
            self.cur_fitness = candidate_fitness
            self.cur_solution = candidate

    def anneal(self):
        """
        Execute the algorithm
        """
        while self.iterations < 2000000:
            candidate = list(self.cur_solution)
            i = random.randint(0, self.file_size-2)
            l = random.randint(i+1, self.file_size-1)
            candidate[i:l+1] = reversed(candidate[i:l+1])
            self.accept(candidate, i, l)
            self.iterations += 1
            self.temp *= self.alpha
        return self.best_fitness, self.best_solution


def run(tour_length):
    data, size = read_file("NEW"+tour_length+".txt")
    cities = to_array(size, data)
    best = math.inf
    best_tour = []
    start_time = time.time()
    # Increasing the range for j will make the whole code loop multiple times, 
    # each time starting from a different random city
    for j in range(1):
        sa = SimulatedAnneal(cities, size)
        current, current_tour = sa.anneal()
        if current < best:
            best = current
            best_tour = current_tour
    print(size, "cities took", time.time() - start_time, "to run")
    print("The best tour was of length", best)
    print("This was the tour", best_tour)
    # write_file(tour_length, size, best, best_tour)
        

run('AISearchfile012')
run('AISearchfile017')
run('AISearchfile021')
run('AISearchfile026')
run('AISearchfile042')
run('AISearchfile048')
run('AISearchfile058')
run('AISearchfile175')
run('AISearchfile180')
run('AISearchfile535')
