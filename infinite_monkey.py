#The infinite monkey theorem states that a monkey hitting keys
#at random on a typewriter keyboard for an infinite amount of time
#will almost surely type a given text, such as the complete works
#of William Shakespeare.

import random

class Individual:
    def __init__(self):
        self.genes = []

class GA:
    def __init__(self, text):
        self.text = text
        self.population_size = 100
        self.num_of_parents = self.population_size / 2;
        self.num_of_genes = len(text)

        self.population = []
        self.parents = []
        self.offspring = []

        self.iteration = 0

        # choose initial populatin
        self.initialize_population()

        # sort population
        self.sort_population()

    def initialize_population(self):
        for i in range(self.population_size):
            ind = Individual()
            for i in range(self.num_of_genes):
                ind.genes.append(random.randint(32, 122))
            self.population.append(ind)

    def sort_population(self):
        sort = True
        while sort:
            sort = False
            for i in range(len(self.population)-1):
                if self.get_fitness(self.population[i]) < self.get_fitness(self.population[i+1]):
                    ind = self.population[i]
                    self.population[i] = self.population[i+1]
                    self.population[i+1] = ind
                    sort = True

    def evolution(self):
        while self.get_fitness(self.population[0]) < self.num_of_genes:
            # select best-ranking individuals to reproduse
            self.do_selection()
            self.print_best_individual()
            self.iteration += 1

    def do_selection(self):
        self.parents = []
        for i in range(self.num_of_parents):
            self.parents.append(self.population[i])

        # crossover
        self.offspring = []
        for i in range(self.num_of_parents-1):
            self.offspring.append(self.crossover(self.parents[i], self.parents[i+1]))
            # mutation
            self.offspring[i] = self.mutation(self.offspring[i])
        self.offspring.append(self.crossover(self.parents[0], self.parents[self.num_of_parents-1]))
        self.offspring[self.num_of_parents-1] = self.mutation(self.offspring[self.num_of_parents-1])

        self.population = self.parents + self.offspring
        self.sort_population()

        self.iteration += 1

    def mutation(self, individual):
        if random.choice([0, 1]) == 1:
            gene_for_mutation = random.choice(range(self.num_of_genes))
            individual.genes[gene_for_mutation] = random.randint(32, 122)
        return individual

    def crossover(self, parent1, parent2):
        point = random.choice(range(self.num_of_genes))
        ind = Individual()
        ind.genes = parent1.genes[:point] + parent2.genes[point:]
        return ind

    def print_population(self):
        print "population, fitness:"
        for ind in self.population:
            out = ""
            for gene in ind.genes:
                out += chr(gene)
            print "\t", out, self.get_fitness(ind)

    def print_best_individual(self):
        ind = self.population[0]
        out = ""
        for gene in ind.genes:
            out += chr(gene)
        print self.iteration, " : ", out, " = ", self.get_fitness(ind), " of ", self.num_of_genes

    def get_fitness(self, individual):
        fitness = 0
        for i in range(self.num_of_genes):
            if ord(self.text[i]) == individual.genes[i]:
                fitness += 1
        return fitness

ga = GA("To be, or not to be: that is the question")
ga.evolution()