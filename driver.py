import Tree as Tree
import readData as readData
from random import *
from heapq import heappush, heappop
import copy
import math


# next implement mutate and debug


##main driver program
##population, and list of lists for train data
def evolution(data, gen_size, details, tol):
    """
    :param data: the training data set, a list of input output touples
    :param gen_size: the size of each generation, could vary
    :param details: a touble specifying the type of selection (1 for tournament),
    and for tournament, the number of tournaments
    :param tol: the error below which we consider ourselves to have found the solution
    """
    # assumes a 1 dimensional output
    input_dim = len(data[0]) - 1
    kings = []
    converged = False
    # create a population
    print('making original generation')
    original = new_gen(gen_size, data, input_dim)
    print('finished making original generation')

    heappush(kings, original[1])

    old_gen = original
    # simulate generations of natural selection
    converg_count = 0
    gen_count = 0
    while not converged:
        try:
            if kings[0].fitness < tol:
                converged = True
                print("Error below tolerance, sucess! Printing king")
                kings[0].root.display()
                print("Broke tolerance after ", gen_count, " generations")
                break

            gen_count += 1
            #print("generation:", gen_count)
            #most fit individual ever, diversity, and size
            #########################################################################
            print gen_count, kings[0].fitness, diversity(old_gen[0]), old_gen[1].fitness, len(old_gen[0])
            #########################################################################
            #print('The diversity of generation ', gen_count, " is ", diversity(old_gen[0]))
            next_gen = run_generation(old_gen, details, data)
            king = next_gen[1]
            #print('most fit individual from generation ', gen_count, ' has fitness', king.fitness)

            try:
                heappush(kings, king)
            except:
                #print(' tie break error')
                continue

            # aging the population
            old_gen = next_gen

            # if we don't improve five times in a row, consider us converged
            # kings[0] gets the smallest element in the heap
            if king.fitness > kings[0].fitness:
                converg_count += 1
                if converg_count > 7:
                    print("fitness has not improved in",  converg_count, " generations")
            else:
                converg_count = 0
        except:
            continue




def tournament(pop, num_torns, data):
    """
    split the population into num_torn groups, plus one for the leftovers,
    then return the best of those groupsas the mating pool

    Requires that the list of trees, pop, is randomized


    For added complexity, we can change from just giving the best,
    to giving the best with probability p (probably around .8), the
    second best with probability p*(1-p), and the third best with probability
    p((1-p)^2), giving the remainder to the first best

    :param pop: the population to select a mate pool from
    :param num_torns: the number of tornaments to hold
    :param data: the data to test each individual's fitness on
    :return champions: a list of num_torns different champions, who
    are the most fit
    """
    champions = []
    # the size of each tournament
    torn_size = int(len(pop) / num_torns)
    # torns = []

    # create num_torn tournaments from which to choose a winner
    for i in range(num_torns):
        # 2nd place implementation
        # torns.append([])
        # run tournaments
        best = float('inf')
        best_tree = None
        for j in range(torn_size):
            if pop[(i * torn_size) + j].depth > 15:
                pop.remove(pop[(i * torn_size) + j])
            fitness = pop[(i * torn_size) + j].calcFitness(data)
            # see if its the best
            if fitness < best:
                best = fitness
                best_tree = copy.deepcopy(pop[(i * torn_size) + j])
            # Use this if you want to keep track and give second place a chance
            # torns[i].append(pop[(i * torn_size) + j])
        # final best
        if best_tree is not None:
            champions.append(best_tree)

    if len(pop) % num_torns != 0:
        # add the stragglers leftover from integer division to the last one
        # definitely check this
        best = float('inf')
        best_tree = None
        for j in range(len(pop) % num_torns):
            fitness = pop[((num_torns - 1) * torn_size) + torn_size + j].calcFitness(data)
            if fitness < best:
                best = fitness
                best_tree = copy.deepcopy(pop[((num_torns - 1) * torn_size) + torn_size + j])
        if best_tree is not None:
            champions.append(best_tree)
        # torns.append([])
        # Use for 2nd place chance
        # torns[num_torns].append(pop[((num_torns - 1) * torn_size) + torn_size + i])
    return champions


def roulette(old_gen, num_, data):
    return


def run_generation(old_gen, details, data):
    """

    :param old_gen: the generation to produce children from in index zero, the king in index 1
    :param details: a touple, the first integer specifying the type of
    parent selection (1 for tournament), the second entry specifying the
    number of tournaments (for tournament)
    :param data: the test data set
    :return: tuple: the first entry is the new population, of size equal to the
    old_gen, the second is the best overall tree from the new generation
    """
    next_gen = []
    best_fitness = float('inf')
    king = None
    # get the tournament size if we are having a tournament
    if details[0] == 1:
        # add the old king
        old_king = old_gen[1]
        next_gen.append(old_king)

        num_tourns = details[1]
        count = 0
        while len(next_gen) < len(old_gen[0]):
            count += 1
            champs = tournament(old_gen[0], num_tourns, data)
            # get n kids from a tournament that splits the population into n groups
            for i in range(num_tourns):
                # randomly select two parents
                index1 = randint(0, len(champs) - 1)
                index2 = randint(0, len(champs) - 1)

                # no asexual reproduction
                while index1 == index2:
                    index2 = randint(0, len(champs) - 1)

                parent1 = champs[index1]
                parent2 = champs[index2]

                # reproduction, parameters taken from Kinnear Generality and difficulty
                rand = randint(0, 100)
                #normal crossover
                if rand < 35:
                    child = parent1.crossover(parent2)
                #crossover without considering fitness
                elif rand < 70:
                    r_index1 = randint(0, len(old_gen[0]) - 1)
                    r_index2 = randint(0, len(old_gen[0]) - 1)
                    child = old_gen[0][r_index1].crossover(old_gen[0][r_index2])
                #regular mutate
                elif rand < 80:
                    parent1.mutate_tree()
                    child = parent1
                #hoist
                elif rand < 90:
                    child = parent1
                    child = parent1.hoist()
                #new original
                else:
                    size = randint(6, 12)
                    if size > 10:
                        size = randint(6, 12)
                    #get the input_dim from the king
                    child = Tree.Tree(size, old_king.input_dim)

                child.calcFitness(data)
                if child.fitness < best_fitness:
                    best_fitness = child.fitness
                    king = copy.deepcopy(child)
                next_gen.append(child)


    if details[0] == 2:
        champs = roulette(old_gen[0], details[1], data)

    #print("size of the old generation is", len(old_gen[0]))
    #print("size of new gen is", len(next_gen))
    return next_gen, king


def new_gen(size, data, input_dim):
    """
    :param data: the data set against which to test the fitness
    :return: the forest of the new generation, and the most fit individual, in a tuple
    :param input_dim: the size of the input dimension
    :type size: size of the generation
    :return tuple: the new generation in the first entry,
    the very best individual in the second entry
    """
    forest = []
    best_fitness = float('inf')
    king = None
    ##create population and rank them by fitness
    for i in range(size):
        #weight the size against numbers over 12
        size = randint(6, 12)
        if size > 10:
            size = randint(6, 12)
        forest.append(Tree.Tree(size, input_dim))
        # calculate fitness
        print("the fitness of new tree ", i, " is ", forest[i].calcFitness(data))
        if forest[i].fitness < best_fitness:
            if forest[i].fitness < 10:
                forest[i].display_tree()
                forest[i].calcFitness(data)
            best_fitness = forest[i].fitness
            king = copy.deepcopy(forest[i])

    return forest, king


#calculates the diversity of the forest
def diversity(forest):
    biggest = None
    worst_fitness = float('inf')
    for i in range(len(forest)):
        if forest[i].fitness < worst_fitness and forest[i].fitness != float('inf'):
            worst_fitness = forest[i].fitness
            biggest = forest[i]
    sum = 0
    for i in range(len(forest)):
        if forest[i].fitness and forest[i].fitness != float('inf'):
            sum += (forest[i].fitness / worst_fitness)
    mean = sum / len(forest)

    diff_sum = 0
    for i in range(len(forest)):
        if forest[i].fitness != float('inf'):
            diff = ((forest[i].fitness / worst_fitness) - mean) ** 2
            diff_sum += diff

    var = math.sqrt(diff_sum)
    return var

#find the mse of our modeling function
def test(test_data):
    mse = 0
    for row in range(len(test_data)):
        f_x = f(test_data[row][0], test_data[row][1], test_data[row][2])
        mse = mse + ((f_x- test_data[row][3]) ** 2)
    mse = mse/len(test_data)
    msqe = math.sqrt(mse)
    return msqe

#our winner function, handwritten
def f(x1,x2,x3):
    return 1025/x3 -5


##testing
# Tree1 = Tree.Tree(5)
# Tree1.display_tree()

# print('reading data')
# data = readData.readData('small_train2.csv')
# print('done reading data')

##Set parameters
# evolution with the data set, 100 people in a generation, (tournament selction with fifteen tournaments),
# and mse error tolerance of 1
# gen_size = 100
# error_tol = 50
# # tournament
# selection_type = 1
# torn_size = int(math.sqrt(gen_size))
# evolution(data, gen_size, (selection_type, torn_size), error_tol)

testdata = readData.readData('test2.csv')
error = test(testdata)
print("error is", error)
