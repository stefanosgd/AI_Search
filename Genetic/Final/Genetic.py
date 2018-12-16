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
    new_file.close()
    return int_data, size


def write_file(f_name, size, best, best_tour):
    """
    This function writes the best tour to its' respective file. To prevent any errors
    from occurring upon submission this has been commented out, and the best tour and length
    are simply output instead
    """
    new_file = open("Checking Tours/Genetic/TourfileA/tourNEW"+f_name+".txt", 'w+')
    new_file.write("NAME = " + f_name + ",")
    new_file.write("\nTOURSIZE = " + str(size) + ",")
    new_file.write("\nLENGTH = " + str(best) + ",\n")
    for i in range(size):
        new_file.write(str(best_tour[i]+1)+",")
    new_file.close()


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
        self.loops = 100
        self.file_size = size
        self.worst = 0
        self.worst_pos = 0
        self.best_tour = []
        self.best_tour_length = math.inf
        self.dist_matrix = cities
        self.nodes = [i for i in range(self.file_size)]

        self.population = [[-1 for x in range(0, self.file_size)] for y in range(self.loops)]
        self.tour_length = [0 for y in range(self.loops)]
        self.fitness = [0 for y in range(self.loops)]
        self.normalised_fitness = self.fitness.copy()
        self.blank_order = self.population[0].copy()

        for i in range(self.loops):
            self.population[i] = self.initial_pop()
            self.tour_length[i] = self.distance(self.population[i])
            if self.tour_length[i] < self.best_tour_length:
                self.best_tour_length = self.tour_length[i]
                self.best_tour = self.population[i]
            self.fitness[i] = 1/self.tour_length[i]
        self.normalise()
        for j in range(self.loops):
            if self.worst < self.tour_length[j]:
                self.worst = self.tour_length[j]
                self.worst_pos = j

    def initial_pop(self):
        """
        Uses a random algorithm to find the initial solution
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

    def new_distance(self, prev_len, prev, sol, i, l):
        """
        Uses the old fitness, along with the 2 edges that have changed, to calculate the new fitness
        in a much faster time than the initial function for calculating the length of a tour
        """
        swapped1 = i
        swapped2 = l
        if swapped2 == self.file_size-1:
            remove = self.dist_matrix[prev[swapped1 - 1]][prev[swapped1]] \
                     + self.dist_matrix[prev[swapped2]][prev[0]]
            add = self.dist_matrix[sol[swapped1 - 1]][sol[swapped1]] + self.dist_matrix[sol[swapped2]][sol[0]]
            attempt = prev_len - remove + add
        else:
            remove = self.dist_matrix[prev[swapped1 - 1]][prev[swapped1]] \
                     + self.dist_matrix[prev[swapped2+1]][prev[swapped2]]
            add = self.dist_matrix[sol[swapped1 - 1]][sol[swapped1]] + self.dist_matrix[sol[swapped2+1]][sol[swapped2]]
            attempt = prev_len - remove + add
        return attempt

    def distance(self, sol):
        """
        Objective value of a solution
        """
        return round(sum([self.dist_matrix[sol[i - 1]][sol[i]] for i in range(1, self.file_size)]) +
                     self.dist_matrix[sol[0]][sol[self.file_size - 1]], 4)

    def normalise(self):
        """
        Uses the sum of all the fitnesses to create a normalised
        fitness array, the sum of which adds up to 1
        """
        fitness_sum = np.sum(self.fitness)
        for i in range(self.loops):
            self.normalised_fitness[i] = self.fitness[i] / fitness_sum

    def next_generation(self):
        """
        Creates the next generation of children
        Children that are better than the current worst in the population
        are added to the population and can be used to create new children immediately
        """
        new_population = self.population.copy()
        new_length = self.tour_length.copy()
        for i in range(self.loops):
            order_a = self.pick_one()
            order_b = self.pick_one()
            order = self.crossover(order_a, order_b)
            order_length = self.distance(order)
            new_population[i], new_length[i] = self.mutate(order_length, order)
            if new_length[i] < self.worst:
                self.tour_length[self.worst_pos] = new_length[i]
                self.population[self.worst_pos] = new_population[i]
                self.fitness[self.worst_pos] = 1/new_length[i]
                self.normalise()
                self.worst = 0
                for j in range(self.loops):
                    if self.worst < self.tour_length[j]:
                        self.worst = self.tour_length[j]
                        self.worst_pos = j
        return new_population, new_length

    def pick_one(self):
        """
        Uses an algorithm to randomly select a member of the population,
        where fitter members are more likely to be chosen
        """
        index = 0
        r = random.random()
        while r >= 0:
            r = r - self.normalised_fitness[index]
            index += 1
        index -= 1
        return self.population[index]

    def mutate(self, prev_length, order):
        """
        Mutates the child a set number of times, and returns the shortest found mutation
        """
        mutate_attempt = order.copy()
        mutate_length = prev_length
        best_mutate_tour = order.copy()
        best_mutate = prev_length
        for i in range(60):
            previous = mutate_attempt.copy()
            previous_length = mutate_length
            i = random.randint(0, self.file_size - 2)
            l = random.randint(i + 1, self.file_size - 1)
            mutate_attempt[i:l + 1] = reversed(mutate_attempt[i:l + 1])
            mutate_length = self.new_distance(previous_length, previous, mutate_attempt, i, l)
            if best_mutate > mutate_length:
                best_mutate = mutate_length
                best_mutate_tour = mutate_attempt.copy()
        if best_mutate < prev_length:
            return best_mutate_tour, best_mutate
        else:
            return order, prev_length

    def crossover(self, a, b):
        """
        Creates the initial child from the 2 selected parents
        """
        start = random.randint(0, len(a)-1)
        end = random.randint(start+1, len(a))
        new_order = self.blank_order.copy()
        new_order[start:end] = a[start:end]
        for i in range(len(b)):
            city = b[i]
            if not new_order.__contains__(city):
                for j in range(len(new_order)):
                    if new_order[j] == -1:
                        new_order[j] = city
                        break
        return new_order

    def run_genetic(self):
        """
        Execute the algorithm
        """
        for j in range(600):
            new_pop, new_len = self.next_generation()
            for i in range(self.loops):
                if new_len[i] < self.best_tour_length:
                    self.best_tour_length = new_len[i]
                    self.best_tour = new_pop[i]
        return self.best_tour, self.best_tour_length


def run(tour_length):
    start_time = time.time()
    data, size = read_file("NEW"+tour_length+".txt")
    cities = to_array(size, data)
    g = Genetic(cities, size)
    current_tour, current_tour_length = g.run_genetic()
    print(size, "cities took", time.time() - start_time, "to run")
    print("The best tour was of length", current_tour_length)
    print("This was the tour", current_tour)
    write_file(tour_length, size, current_tour_length, current_tour)
        

# run('AISearchfile012')
# run('AISearchfile017')
# run('AISearchfile021')
# run('AISearchfile026')
run('AISearchfile042')
run('AISearchfile048')
run('AISearchfile058')
run('AISearchfile175')
run('AISearchfile180')
run('AISearchfile535')
