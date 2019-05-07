import csv
import random
import math
import time
k = 25000
over_capacity_assignment_count = 0
#####################################################################################
#               ReadData                                                            #
#                                                                                   # 
#   Returns a tuple - road_list, school_cap_list                                    #
#       road_list - list of road objects, which                                     #   
#                    contains all road segments                                     #   
#       school_cap_list - position is ID as defined by the assumption that          #
#                         the schools are ordered in the same way in the            #
#                         rc file and the schools file, starting at 0 and continuing#
#                         to 54                                                     #
#####################################################################################
def readData(roads, schools):
    with open(roads) as rc_file, open(schools) as schools_file:
        #dialect = csv.Sniffer().sniff(csv_file.read(1024))
        #csv_file.seek(0)
        #Each row read from the csv file is returned as a list of strings
        rc_dataset = list(csv.reader(rc_file,delimiter=','))
        schools_dataset = list(csv.reader(schools_file, delimiter=','))
        
        road_list = []
        count = 0
        for row in rc_dataset:
            #testing stopping condition for small datasets
            # count += 1
#             if count == k:
#                 break
            road_id = int(row[0])
            ses = int(row[3])
            pop = float(row[1])
            
            #read in schools
            schools = row[8:]
            close_schools = []
            for dist in schools:
                #only read in real distances
                if float(dist) < 99999:
                    tup = (schools.index(dist), float(dist))  #schools.index(dist) is the number of the school
                    close_schools.append(tup)
                    
            #keep list of roads 
            road_list.append(Road(road_id, ses, pop, close_schools))

        #position is ID, entry is capacity
        school_list = []
        schools_dataset.pop(0) #take out the header
        for row in schools_dataset:
            school_list.append(School(float(row[4])))
            
            #testing stopping conditition for smaller dataset
            # if schools_dataset.index(row) == 700:
#                 break
            
        return District(road_list, school_list)

class Switcher(object):
    def ses_to_func(self, arg):
        """Dispatch method"""
        method_name = 'add_' + str(arg)  
        method = getattr(School, method_name)      
class School:
    def __init__(self, cap):
        self.cap = cap
        self.low_std = 0
        self.mid_std = 0
        self.high_std = 0
        
    def add_1(self, arg):
        self.low_std += arg
        
    def add_2(self, arg):
        self.mid_std += arg
        
    def add_3(self, arg):
        self.high_std += arg
        
    ##################################################
    #Road class has three instances
    #SES - 1 LOW
    #      2 MEDIUM
    #      3 HIGH
    #POP - Population of the school
    #Schools - list of five tuples of ID, Distance 
    ##################################################
class Road:
    def __init__(self, road_id, ses, pop, close_schools):
        #create instances variables
        self.road_id = road_id
        self.ses = ses  
        self.pop = pop  
        self.close_schools = close_schools  
    def pretty_print(self):
        print 'road ', self. road_id, ' has ses ', self.ses, ' population ', self.pop, \
        ' and the five closest schools have the (id, distance-pair)', self.close_schools
        print ''
    

class District:
    def __init__(self, road_list, school_list):
        self.road_list = road_list
        self.school_list = school_list
        self.assignment = []
        self.running_cap = [0] * len(school_list)
        

    def pretty_print(self):
        for road in self.road_list:
            road.pretty_print()
        for num in range(len(self.school_list)):
            print 'school ', num, ' has capacity ', self.school_list[num].cap
            
    #################################################################################
    #                               Check capacity                                  #
    #                                                                               #
    #   @param current_assignment - current assignment of roads to school positions #
    #                               in the list                                     #
    #   @param road - road being added                                              #
    #   @param school_id  - to school_id position in the current assignment list    #
    #   @returns true if assignment possible, and also makes the assignment, and updates the SES total #
    #   @returns false if assignment not possible
    #################################################################################
    def check_capacity(self, current_assignment, road_id, school_id):
        cap = self.school_list[school_id].cap
        pop = self.road_list[road_id].pop
        if self.running_cap[school_id] + pop > cap * 1.25:
            global over_capacity_assignment_count 
            over_capacity_assignment_count += 1
            return False
        else:
            current_assignment[road_id] = school_id
            self.running_cap[school_id] += pop
            ses = self.road_list[road_id].ses
            
            method_name = 'add_' + str(ses)  
            add_method = getattr(self.school_list[0], method_name)
            add_method(pop)   
            return True
            
    def ses_to_func(self, arg):
        """Dispatch method"""
        method_name = 'add_' + str(arg)  
        method = getattr(self.school_list[0], method_name)
    
            
     #############################################################################
     #                     New Gen                                               #
     # @param num_schools - the number of schools                                # 
     # @param num_roads - the number of roads                                    #
     # @param road_list - list of road objects                                   #
     # @param school_list - list of schools capacities, "ID" is position and     #
      ############################################################################  
    def spawn(self):
        #re-initialize the running capacity
        self.running_cap = [0] * len(self.school_list)
        assignment = [None] * len(self.road_list)
        for road_num in range(len(self.road_list)):
            start = time.time()
            if road_num % 100 == 0:
                print ' it took ', time.time() - start, ' seconds to  assign the last 100 schools,' \
                'which takes us up to road number ', road_num
                start = time.time()
            assigned = False
            while not assigned:
                assigned = self.check_capacity(assignment, road_num, random.randint(0,len(self.school_list) - 1)) \
                #last arguement is random school id
        assign_obj = Assignment(assignment)
        return assign_obj
        
        
class Assignment:
    def __init__(self, assignment):
        self.rs_list = assignment
        self.fitness = self.calcFitness()
    #use Lena's function here
    def calcFitness(self):
        return 10
        #find SES of the school
    def pretty_print(self):
        print self.assignment, ', fitness: ', self.fitness
 
        
###############Driver methods############
def new_gen(size, district, tol):
    """
    :param data: the district from which to create new children
    :return tuple: the new generation in the first entry,
    the very best individual in the second entry
    """
    forest = []
    best_fitness = float('inf')
    king = None
    ##create population and rank them by fitness
    for i in range(size):
        cur = district.spawn()
        forest.append(cur)
        # calculate fitness
        print("the fitness of new tree ", i, " is ", cur.fitness)
        if cur.fitness < best_fitness:
            best_fitness = cur.fitness
            king = cur
            if cur.fitness < tol:
                print ' we broke tolerance, YAY! ', cur.pretty_print()
                break
    return forest, king

def calcFitness(self, data):
    # squared error
    sqrerr = 0
    # use each set of data points
    for row in range(len(data)):
        # get a data point
        list_i = data[row]

        # take the input and leave the output
        input_i = list_i[0:self.input_dim]
        #print(input_i)
        # convert from list to tuple
        input_tup = tuple(input_i)
        # evaluate based on the tuple
        f_out = self.evaluate(input_tup)

        sqrerr += (f_out - data[row][-1]) ** 2
    mse = sqrerr / len(data)
    rmse = mse ** (.5)
    # Need to add size penalty, add 2.5% of the total fitness for each node
    rmse += SIZE_PENALTY_COEFF * self.size * rmse
    self.fitness = mse
    return mse
 

BG_district = readData("rc-bluegreen.csv", "schoolsbluegreenDescribed.csv")
#BG_district.pretty_print()
n = 100
start = time.time()
start2 = time.clock()
BG_district.spawn()
new_gen(n, BG_district, 4)
print 'the total number of overcapacity assignments is ', over_capacity_assignment_count
print 'It took ', time.time() - start, ' to create ', n, ' assignments with ', len(BG_district.road_list), ' roads'
print 'By another measure'
print 'It took ', time.clock() - start2, ' to create ', n, ' assignments with ', len(BG_district.road_list), ' roads'