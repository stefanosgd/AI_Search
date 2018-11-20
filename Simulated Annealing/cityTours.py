import re
import numpy as np
import math
import random
import time

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


def write_file(f_name, size, best, best_tour):
    new_file = open("../Checking Tours/Simulated Annealing/TourfileA/tourNEW"+f_name+".txt", 'w+')
    new_file.write("NAME = " + f_name + ",")
    new_file.write("\nTOURSIZE = " + str(size) + ",")
    new_file.write("\nLENGTH = " + str(best) + ",\n")
    for i in range(size):
        new_file.write(str(best_tour[i]+1)+",")


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
    def __init__(self, starting_city, cities, size):
        # self.iterations = 0
        self.cities = cities
        self.file_size = size
        self.temp = math.sqrt(self.file_size)
        # print(self.temp)
        self.alpha = 0.999
        self.stopping_temperature = 0.000001

        self.dist_matrix = self.cities
        self.nodes = [i for i in range(self.file_size)]

        self.cur_solution = self.initial_solution(starting_city)
        self.best_solution = list(self.cur_solution)

        self.cur_fitness = self.fitness(self.cur_solution)
        self.initial_fitness = self.cur_fitness
        self.best_fitness = self.cur_fitness

    def initial_solution(self, start):
        """
        Greedy algorithm to get an initial solution (closest-neighbour)
        """
        cur_node = start
        solution = [cur_node]
        closest_dist = math.inf
        free_list = list(self.nodes)
        free_list.remove(cur_node)
        while free_list:
            for j in free_list:
                if self.dist_matrix[cur_node][j] < closest_dist:
                    closest_dist = self.dist_matrix[cur_node][j]
                    next_node = j
            cur_node = next_node
            free_list.remove(cur_node)
            solution.append(cur_node)
            closest_dist = math.inf
        return solution

    def fitness(self, sol):
        """ Objective value of a solution """
        return round(sum([self.dist_matrix[sol[i - 1]][sol[i]] for i in range(1, self.file_size)]) +
                     self.dist_matrix[sol[0]][sol[self.file_size - 1]], 4)

    def p_accept(self, candidate_fitness):
        """
        Probability of accepting if the candidate is worse than current
        Depends on the current temperature and difference between candidate and current
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.temp)

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
        while self.temp >= self.stopping_temperature:
            candidate = list(self.cur_solution)
            l = random.randint(2, self.file_size - 1)
            i = random.randint(0, self.file_size - l)
            candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
            self.accept(candidate)
            self.temp *= self.alpha
            # self.iteration += 1
        return self.best_fitness, self.best_solution


def run(tour_length):
    data, size = read_file("../NEW" + tour_length + ".txt")
    cities = to_array(size, data)
    best = math.inf
    best_tour = []
    very_best = math.inf
    very_best_tour = []
    start_time = time.time()
    for j in range(1):
        for i in range(size):
            sa = SimulatedAnneal(i, cities, size)
            current, current_tour = sa.anneal()
            if current < best:
                best = current
                best_tour = current_tour
        if best < very_best:
            very_best = best
            very_best_tour = best_tour
    print(size, 'cities took', time.time() - start_time, 'to run')
    print(very_best)
    print(very_best_tour)
    write_file(tour_length, size, very_best, very_best_tour)


run('AISearchfile012')
run('AISearchfile017')
run('AISearchfile021')
run('AISearchfile026')
run('AISearchfile042')
# run('AISearchfile048')
# run('AISearchfile058')
# run('AISearchfile175')
# run('AISearchfile180')
# run('AISearchfile535')
