from heapq import heappush, heappop
from read_and_drive import *
import sys
from math import sqrt
import time
from random import randint

gen_size = 100
error_tol = 10
converg_tol = 50
num_torn = int(math.sqrt(gen_size))

# main driver program
def evolution(gen_size, num_torn, district, tol):
    """
    :param data: the training data set, a list of input output touples
    :param gen_size: the size of each generation, could vary
    :param details: a touble specifying the type of selection (1 for tournament),
    and for tournament, the number of tournaments
    :param tol: the error below which we consider ourselves to have found the solution
    """''
    output = [] #tuple list of king fitness, diversity at each generation
    kings = []
    converged = False
    timesum = 0
    #print('making original generation')
    start = time.time()
    original = new_gen(gen_size, district) # create a population
    #print('finished making original generation')

    heappush(kings, original[1]) #put original[1], the king, onto the heap kings
    timesum += time.time()-start
    output.append((original[1].fitness, int(kings[0].fitness), diversity(original[0]), (time.time() - start) / 60.0, timesum))

    old_gen = original


    # simulate generations of natural selection
    converg_count = 0
    gen_count = 0
    while not converged:
        print ('#############################################################')
        print ('         Output:', sys.argv[1], sys.argv[2])
        print ('#############################################################')
        print ('King, Emperor, Diversity, Time, Total Time')
        for entry in output:
            print (int(entry[0]), int(entry[1]), entry[2], int(entry[3]), int(entry[4]))
        print ('')

        if kings[0].fitness < tol: #smallest element in a heap is always heap[0]
            converged = True
            print("Error below tolerance, sucess! Printing king")
            kings[0].pretty_print()
            print("Broke tolerance after ", gen_count, " generations")
            break

        gen_count += 1
        start = time.time()
        next_gen = run_generation(old_gen, num_torn, district)
        king = next_gen[1]
        heappush(kings, king)
        timesum += time.time() - start #caclulate time to run generation
        output.append((king.fitness, kings[0].fitness, diversity(next_gen[0]), time.time() - start, timesum)) #record results

        # age generation
        old_gen = next_gen

        # if we don't improve converg_count + 1 times in a row, consider us converged
        # kings[0] gets the smallest element in the heap
        if king.fitness > kings[0].fitness:
            converg_count += 1
            if converg_count > converg_tol:
                print("fitness has not improved in",  converg_count, " generations")
                converged = True
        else:
            converg_count = 0

def run_generation(old_gen, num_tourns, district):
    """
    :param old_gen: the generation to produce children from in index zero, the king in index 1
    :param details: a touple, the first integer specifying the type of
    parent selection (1 for tournament), the second entry specifying the
    number of tournaments (for tournament)
    :param district: district object for the problem
    :return: tuple: the first entry is the new population, of size equal to the
    old_gen, the second is the best overall tree from the new generation
    """
    next_gen = []
    best_fitness = float('inf')
    king = None
    old_king = Assignment(old_gen[1].rs_list)  #add the old king
    old_king.fitness = old_gen[1].fitness
    next_gen.append(old_king)
    while len(next_gen) < len(old_gen[0]):
        champs = tournament(old_gen[0], num_tourns, district)
        # get n kids from a tournament that splits the population into n groups
        for i in range(num_tourns):
            #print ' breeding child ', i, ' of ', num_tourns
            # randomly select a parent
            index1 = randint(0, len(champs) - 1)
            parent1 = champs[index1]

            rand = randint(0, 100)#reproduction options, currently set only to mutate
            #normal crossover
#             if rand < 50:
#                 print 'crossing over'
#                 child = parent1.crossover(parent2, district)
#
#             #crossover without considering fitness
#             elif rand < 75:
#                 print 'crossing over random'
#                 r_index1 = randint(0, len(old_gen[0]) - 1)
#                 r_index2 = randint(0, len(old_gen[0]) - 1)
#                 child = old_gen[0][r_index1].crossover(old_gen[0][r_index2], district)

            #regular mutate
            if rand < 90:
                #print 'mutating'
                parent1.mutate(district)
                child = parent1
            #new original
            else:
                #print 'spawning'
                child = district.spawn()

            if child.fitness < best_fitness:
                best_fitness = child.fitness
                king = Assignment(child.rs_list)
                king.fitness = child.fitness
            next_gen.append(child)

    #print 'the king has fitness ', king.fitness
    return next_gen, king

def tournament(pop, num_torns, district):
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
    :param district: the district data type
    :return champions: a list of num_torns different champions, who
    are the most fit
    """
    champions = []
    # print(pop)
    # print()
    # print(list(map(lambda x : x.fitness, pop)))
    # exit()
    torn_size = int(len(pop) / num_torns) # the size of each tournament
    # create num_torn tournaments from which to choose a winner
    #print 'num_torns is', num_torns
    for i in range(num_torns):
        #print 'running tournament', i
        # run tournaments
        best = float('inf')
        best_child = None
        for j in range(torn_size):
            # print(pop[(i * torn_size) + j].fitness)
            assignment = pop[(i * torn_size) + j]
            assignment.calcFitness(district)
            fitness = assignment.fitness
            
            if fitness < best: #see if its the best
                best = fitness
                best_child = copy.deepcopy(pop[(i * torn_size) + j])
            # Use this if you want to keep track and give second place a chance
            # torns[i].append(pop[(i * torn_size) + j])
        if best_child is not None: # final best
            champions.append(best_child)


    if len(pop) % num_torns != 0:
        # add the stragglers leftover from integer division to the last one
        # definitely check this
        best = float('inf')
        best_child = None
        for j in range(len(pop) % num_torns):
            #print ' examining straggler '
            assignment = pop[((num_torns - 1) * torn_size) + torn_size + j]
            assignment.calcFitness(district)
            fitness = assignment.fitness
            if fitness < best:
                best = fitness
                best_child = copy.deepcopy(pop[((num_torns - 1) * torn_size) + torn_size + j])
        if best_child is not None:
            champions.append(best_child)
        # torns.append([])
        # Use for 2nd place chance
        # torns[num_torns].append(pop[((num_torns - 1) * torn_size) + torn_size + i])
    return champions


def new_gen(size, district):
    """
    :type size: size of the generation
    :return tuple: the new generation in the first entry,
    the very best individual in the second entry
    """
    children = []
    best_fit = float('inf')
    king = None

    for i in range(size):
        children.append(district.spawn())
        if children[i].fitness < best_fit:
            king = Assignment(children[i].rs_list)
            king.fitness = children[i].fitness #deepcopy doesn't fucking work
            best_fit = king.fitness
    return children, king


# calculates the diversity of the generation
def diversity(children):
    worst_fitness = float('inf')
    for child in children:
        if child.fitness < worst_fitness and child.fitness != float('inf'):
            worst_fitness = child.fitness
    sum = 0
    for child in children:
        if child.fitness and child.fitness != float('inf'):
            sum += (child.fitness / worst_fitness)

    mean = sum / len(children)

    diff_sum = 0
    for i in range(len(children)):
        if children[i].fitness != float('inf'):
            diff = ((children[i].fitness / worst_fitness) - mean) ** 2
            diff_sum += diff

    var = math.sqrt(diff_sum)
    return var


def main():
    if (len(sys.argv) != 3):
        print ()
        print ("***********************************************************")
        print ("You need to supply a .csv file containing the road data and school data")
        print ("as a command-line argument.")
        print()
        print ("Example:")
        print ("    python final_driver all-rc.csv allschools.csv")
        print ("***********************************************************")
        print()
        return
    for i in range(10):
        print()
    print ('Reading in ', sys.argv[1], 'with' , sys.argv[2] + '...')
    all_district = readData(sys.argv[1], sys.argv[2])
    print ('Finished')

    ##Set parameters
    # evolution with the data set, 100 people in a generation, (tournament selction with fifteen tournaments),
    # and mse error tolerance of 1
    evolution(gen_size, num_torn, all_district, error_tol)


if __name__ == "__main__":
    main()
