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


def write_file(f_name, size, best, best_tour):
    new_file = open("Checking Tours/Genetic/TourfileA/tourNEW"+f_name+".txt", 'w+')
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


class Genetic:
    def __init__(self, cities, size):
        # self.mutation_count = 0
        self.loops = 50
        self.cities = cities
        self.file_size = size
        self.best_tour = []
        self.best_tour_length = math.inf
        self.dist_matrix = cities
        self.nodes = [i for i in range(self.file_size)]

        self.population = create_empty(self.loops)
        self.tour_length = create_empty(self.loops)
        self.fitness = create_empty(self.loops)
        self.normalised_fitness = create_empty(self.loops)

        for i in range(self.loops):
            self.population[i] = self.initial_pop()
            self.tour_length[i] = self.distance(self.population[i])
            if self.tour_length[i] < self.best_tour_length:
                self.best_tour_length = self.tour_length[i]
                self.best_tour = self.population[i]
            self.fitness[i] = 1/self.tour_length[i]
        self.normalise()
        # print(self.population)
        # print("Normalised fitness =", self.fitness)
        # print("Tour length =", self.tour_length)
        # print(self.best_tour)
        # print(self.best_tour_length)

    def initial_pop(self):
        """
        Getting randomly shuffled paths
        """
        free_list = list(self.nodes)
        cur_node = random.choice(free_list)
        solution = [cur_node]
        free_list.remove(cur_node)
        while free_list:
            cur_node = random.choice(free_list)
            free_list.remove(cur_node)
            solution.append(cur_node)
        return solution

    def distance(self, sol):
        """ Objective value of a solution """
        return round(sum([self.dist_matrix[sol[i - 1]][sol[i]] for i in range(1, self.file_size)]) +
                     self.dist_matrix[sol[0]][sol[self.file_size - 1]], 4)

    # def mutated_distance(self, original_index, original, mutated, i, l):
    #     swapped1 = i
    #     swapped2 = l
    #     if swapped2 == self.file_size - 1:
    #         remove = self.dist_matrix[original[swapped1 - 1]][original[swapped1]] \
    #                  + self.dist_matrix[original[swapped2]][original[0]]
    #         add = self.dist_matrix[mutated[swapped1 - 1]][mutated[swapped1]] + self.dist_matrix[mutated[swapped2]][mutated[0]]
    #         attempt = self.tour_length[original_index] - remove + add
    #     else:
    #         remove = self.dist_matrix[original[swapped1 - 1]][original[swapped1]] \
    #                  + self.dist_matrix[original[swapped2 + 1]][original[swapped2]]
    #         add = self.dist_matrix[mutated[swapped1 - 1]][mutated[swapped1]] + self.dist_matrix[mutated[swapped2 + 1]][
    #             mutated[swapped2]]
    #         attempt = self.tour_length[original_index] - remove + add
    #     return attempt

    def normalise(self):
        # for i in range(self.loops):
        #     sum += self.fitness[i]
        fitness_sum = np.sum(self.fitness)
        for i in range(self.loops):
            self.normalised_fitness[i] = self.fitness[i] / fitness_sum

    def next_generation(self):
        new_population = self.population
        new_length = self.tour_length
        new_fitness = self.fitness
        for i in range(self.loops):
            order_a = self.pick_one()
            order_b = order_a
            while order_a == order_b:
                order_b = self.pick_one()
            order = self.crossover(order_a, order_b)
            order_length = self.distance(order)
            # print(order)
            # print(index)
            new_population[i], new_length[i] = self.mutate(order, order_length, 0.05)
            new_fitness[i] = 1/new_length[i]
            if new_length[i] < self.tour_length[i]:
                self.tour_length[i] = new_length[i]
                self.population[i] = new_population[i]
                self.fitness[i] = new_fitness[i]
        # self.population = new_population
        # self.tour_length = new_length
        # self.fitness = new_fitness
        self.normalise()
        # print(self.population)
        #
        # print("Normalised fitness =", self.fitness)
        # print("Tour length =", self.tour_length)
        return new_population, new_length

    def pick_one(self):
        index = 0
        r = random.random()
        while r > 0 and index < self.loops:
            r = r - self.normalised_fitness[index]
            index += 1
        index -= 1
        return self.population[index]

    def mutate(self, order, order_length, mutation_rate):
        mutate_attempt = order
        mutate_length = order_length
        # print("Before", mutate_attempt)
        for i in range(self.loops):
            if random.random() < mutation_rate:
                # self.mutation_count += 1

                i = random.randint(0, self.file_size - 2)
                l = random.randint(i + 1, self.file_size - 1)
                # i = random.randint(0, self.file_size-1)
                # l = i
                # while l == i:
                #     l = random.randint(0, self.file_size-1)
                # mutate_attempt = self.swap(mutate_attempt, i, l)

                mutate_attempt[i:l + 1] = reversed(mutate_attempt[i:l + 1])
            mutate_length = self.distance(mutate_attempt)
        # print("After ", mutate_attempt)
        return mutate_attempt, mutate_length

    # def swap(self, attempt, a, b):
    #     temp = attempt[a]
    #     attempt[a] = attempt[b]
    #     attempt[b] = temp
    #     return attempt

    def crossover(self, a, b):
        start = random.randint(0, len(a)-1)
        end = random.randint(start+1, len(a))
        new_order = a[start:end]
        for i in range(len(b)):
            city = b[i]
            if not new_order.__contains__(city):
                new_order.append(city)
        return new_order

    def run_genetic(self):
        # self.normalise()
        # print(self.population)
        # print("second :", self.fitness)
        # print(self.tour_length)
        # print("Best =", self.best_tour)
        # print("Best =", self.best_tour_length)
        for j in range(100):
            new_pop, new_len = self.next_generation()
            for i in range(self.loops):
                if new_len[i] < self.best_tour_length:
                    self.best_tour_length = new_len[i]
                    self.best_tour = new_pop[i]
                    # print("New Best =", self.best_tour)
                    # print("New Best =", self.best_tour_length)
                # print(new_pop)
        # print(self.mutation_count)
        return self.best_tour, self.best_tour_length


def run(tour_length):
    start_time = time.time()
    data, size = read_file("NEW"+tour_length+".txt")
    cities = to_array(size, data)
    # best = math.inf
    # best_tour = []
    # very_best = math.inf
    # very_best_tour = []
    for i in range(1):
        g = Genetic(cities, size)
        current_tour, current_tour_length = g.run_genetic()
        print("Best tour =", current_tour)
        print("Best tour length =", current_tour_length)
#         current, current_tour = g.anneal()
#         if current < best:
#             best = current
#             best_tour = current_tour
#     #     print('Starting with the greedy algorithm at city', i+1, 'the best tour for', size, 'cities is ', current)
#     #     for i in range(size):
#     #         print((current_tour[i] + 1), end=",")
#     #     print()
#     # print('The best tour for', size, 'cities is ', best)
#     # for i in range(size):
#     #     print((best_tour[i] + 1), end=",")
#     # print()
#     # print('This took', time.time() - start_time, 'to run')
#     if best < very_best:
#         very_best = best
#         very_best_tour = best_tour
# print('The very best tour for', size, 'cities is ', very_best)
# # for i in range(size):
# #     print((very_best_tour[i] + 1), end=",")
# # print()
    print(size, 'cities took', time.time() - start_time, 'to run')
    write_file(tour_length, size, current_tour_length, current_tour)
        

run('AISearchfile012')
# run('AISearchfile017')
# run('AISearchfile021')
# run('AISearchfile026')
# run('AISearchfile042')
# run('AISearchfile048')
# run('AISearchfile058')
# run('AISearchfile175')
# run('AISearchfile180')
# run('AISearchfile535')