from __future__ import division
import csv
import random
import math
import time
import copy

k = 100
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
        #Each row read from the csv file is returned as a list of strings
        rc_dataset = list(csv.reader(rc_file,delimiter=','))
        schools_dataset = list(csv.reader(schools_file, delimiter=','))
        
        road_list = []
        row_count = 0
        rc_dataset.pop(0)
        for row in rc_dataset:
            #testing stopping condition for small datasets
            row_count += 1
            if row_count == k:
                break
            road_id = int(row[0])
            ses = int(row[3])
            pop = float(row[1])
            
            #read in schools
            schools = row[8:]
            close_schools = []
            for school_count in range(len(schools)):
                #only read in real distances
                dist = float(schools[school_count])
                if dist < 99999:
                    tup = (school_count, dist)  #is the number of the school in the column
                    close_schools.append(tup)
                    
            #keep list of roads 
            road_list.append(Road(road_id, ses, pop, close_schools))

        #position is ID, entry is capacity
        school_list = []
        #schools_dataset.pop(0) #take out the header
        for row in schools_dataset:
            school_list.append(School(float(row[4])))
        return District(road_list, school_list)   
        
    ########################################################
    #           School class many three instances       
    #   Schools don't have id's, just positions in arrays
    ######################################################
class School:
    def __init__(self, cap):
        self.cap = cap
        self.low_std = 0
        self.mid_std = 0
        self.high_std = 0
        
        self.low_pro = 0
        self.mid_pro = 0
        self.high_pro = 0
        
        self.weight = 0
        
    def calcPro(self):
        total = self.low_std + self.mid_std + self.high_std
        if total == 0:
            return
        self.low_pro = self.low_std / total 
        self.mid_pro = self.mid_std / total
        self.high_pro = self.high_std / total
        
        self.weight = abs((1.0/3.0) - self.low_pro) + abs((1.0/3.0) - self.mid_pro) + abs((1.0/3.0) - self.high_pro) + 1

    
    def pretty_print(self):
        print 'this school has ', self.low_std, ' low ses students ', self.mid_std, ' mid ses students ', \
        self.high_std, ' high ses students , so it is ', self.low_pro , ' percent low and ', self.low_pro + \
        self.mid_pro + self.high_pro , ' = 1'
    
    def reset(self):
        self.low_std = 0
        self.mid_std = 0
        self.high_std = 0
        
        self.low_pro = 0
        self.mid_pro = 0
        self.high_pro = 0

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
    
#######################################################
#           District class has two instances          #
# road_list - a list of road objects                  #
# school_list - a list of school objects              #
#######################################################
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
    def check_capacity(self, current_assignment, position, road, school_id):
        cap = self.school_list[school_id].cap
        pop = road.pop
        if self.running_cap[school_id] + pop > cap * 1.25:
            global over_capacity_assignment_count 
            over_capacity_assignment_count += 1
            return False
        else:
            current_assignment[position] = school_id
            self.running_cap[school_id] += pop
            ses = road.ses
            
            #this is actually faster than switching on the methods
            if ses == 1:
                self.school_list[school_id].low_std =+ pop
            elif ses == 2:
                self.school_list[school_id].mid_std =+ pop
            elif ses == 3:
                self.school_list[school_id].high_std =+ pop
            else: 
                raise Exception('invaldid SES, the SES is ', ses)
            return True
        
            
     #######################################################################################################
     #                                              Spawn                                                  #
     #                                                                                                     #
     # @returns assign_obj - an assignment object with road_id as the index,                               #
     #                        #school_id as the school, and none objects entered if no assignment possible #
     # #####################################################################################################  
    def spawn(self):
        best_fitness = float('inf')
        
        for school in self.school_list:
            school.reset() 
            
        assignment = [None] * len(self.road_list)
        count = 0
        for road in self.road_list:
            assigned = False
            tried = set(())
            while not assigned:
                #there are no listed close schools
                if len(road.close_schools) == 0:
                    assigned = True
                    break
                five_close = road.close_schools #not necessarily five schools
                random_close = five_close[random.randint(0, len(five_close) - 1)]
                random_school_id = random_close[0] 
                tried.add(random_school_id)
                if len(tried) == len(five_close):
                    break #we have tried every assignment and none work
                random_dist = random_close[1] #comment out
                assigned = self.check_capacity(assignment, count, road, random_school_id) #last arguement is school_id
                
            count += 1
        assign_obj = Assignment(assignment)
        
        ######Calculate proportions######
        #make sure we don't try to calculated the proprotion of a school with no one
        for school_id in range(len(self.school_list)):
            if self.running_cap[school_id] != 0.0:
                self.school_list[school_id].calcPro()
                
        self.running_cap = [0] * len(self.school_list)#re-initialize the running capacity and school populations
            
        assign_obj.calcFitness(self)
    
        return assign_obj
        
#################################################################
#           Assignment class has two instances                  #
# rs_list  - a list with length of the number of roads where    #
#               each entry is a school_id, not a school object  #
#               will have a none entry if there are no schools  #
#               in range                                        # 
# fitness   - the fitness of the school assignment              #
#################################################################
class Assignment:
    def __init__(self, assignment):
        self.rs_list = assignment
        self.size = len(assignment)
        self.assignment_pop = None #length is number of schools, entry is population in school
        self.fitness = float('inf')
        
    # make the tree comparable, two trees are equal if they point to the same reference
    def __eq__(self, other):
        if self is other:
            return True
        else:
            return False

    # define equality as outputting the same number (assuming that if f(10) = g(10), then f = g
    def __lt__(self, other):
        return self.fitness < other.fitness
        print 'using __lt__'
    def cmp_lt(self, other):
        return self.fitness < other.fitness
        print 'using cmp_lt'

    #use Lena's function here
    def calcFitness(self, district): #populated_school_list is the number of people (entry) in each school (id)
        self.fitness = 0
        for road_num in range(len(self.rs_list)): #find the distance from the road to the school it's assigned to
            if self.rs_list[road_num] == None:
                continue
            five_schools = district.road_list[road_num].close_schools
            for tup in five_schools:
                if self.rs_list[road_num] == tup[0]: #tup[0] is school_id
                    dist = tup[1]
                    weight = district.school_list[tup[0]].weight
                    self.fitness += dist * weight
                    break
        #could populate schools here, but is uncessary because it doesn't affect fitness and we've
        #already checked overcapacity
                    
    def populate_schools(self, district):
        for i in range(len(self.rs_list)):
            school_id = self.rs_list[i] #school we're looking at
            if school_id is None: #this road was not assigned to any school bc nothing was within range by Lena's data
                continue
            pop = district.road_list[i].pop #number of people now going to school school_id
            self.assignment_pop[school_id] += pop
            
            
    ########################################################################
    #                             Crossover                                #
    ########################################################################
    #crossover from 20 to 80 percent
    def crossover(self, other, district):
        assigned = False
        lower = int(len(self.rs_list) * .2)
        upper = int(len(self.rs_list) * .8)
        while(not assigned):
            pos = random.randint(lower, upper)
            temp = self.rs_list[pos:]
            self.rs_list[pos:] = other.rs_list[pos:]
            other.rs_list[pos:] = temp
            assigned = self.check_valid(district) and other.check_valid(district)
        self.calcFitness(district)
        return self
    
    ########################################################################
    #                             Mutate                                   #
    ########################################################################
    #randomly swaps anywhere from 1 to 2 percent of the number of schools
    #if there are 1000 schools, we will swap 10 to 20 times
    def mutate(self, district):
        if self.assignment_pop is None: #mutating an OG child
            self.check_valid(district)
        num_mutations = int(random.uniform(.1,.2) * len(self.rs_list))
        #print ' the number of mutations is ', num_mutations
        for i in range(num_mutations):
            completed = False
            while(not completed):
                valid = True
                pos1 = random.randint(0, len(self.rs_list) - 1) #road number 1
                pos2 = random.randint(0, len(self.rs_list) - 1) #road number 2
                school_id1 = self.rs_list[pos1] #school number 1
                school_id2 = self.rs_list[pos2] #school number 2
                
                if school_id1 is None or school_id2 is None:
                    continue
                    
                #check potential for just those switches, assignment_pop should be full
                potential_school1 = self.assignment_pop[school_id1] - district.road_list[pos1].pop\
                  + district.road_list[pos2].pop
                potential_school2 = self.assignment_pop[school_id2] - district.road_list[pos2].pop\
                  + district.road_list[pos1].pop
                  
                 #overcapacity?
                if potential_school1 > district.school_list[school_id1].cap:
                     print ' bad kid'
                     valid = False
                if potential_school2 > district.school_list[school_id2].cap:
                     valid = False
                     print ' bad kid'
                 
                #swap roads
                temp = self.rs_list[pos1]
                self.rs_list[pos1] = self.rs_list[pos2]
                self.rs_list[pos2] = temp
             
                 #update populations 
                if valid:
                     self.assignment_pop[school_id1] = self.assignment_pop[school_id1] - district.road_list[pos1].pop\
                      + district.road_list[pos2].pop
                     self.assignment_pop[school_id2] = self.assignment_pop[school_id2] - district.road_list[pos2].pop\
                      + district.road_list[pos1].pop
                     completed = True
                     self.calcFitness(district)       
        return self
    
    #check to see whether an offspring produced by crossover (rather than spawn) is valid based on 
    #the potential to make a school overcapcity
    def check_valid(self, district):
        #road list and self should have same length 
        over_capacity = False
        self.assignment_pop = [0] * len(district.school_list) #total the population this assignment gives
        assert len(self.rs_list) == len(district.road_list)
        self.populate_schools(district) #populates the schools by filling self.assignment_pop
        for school_id in range(len(district.school_list)):
            if self.assignment_pop[school_id] > district.school_list[school_id].cap:
                over_capacity = True
                print 'school ', school_id, ' was assigned ', assignment_pop[school_id], \
                ' children but it has a capacity of ', district.school_list[school_id].cap
                time.sleep(5)
        return not over_capacity
        
                
    def pretty_print(self):
        print 'the child has fitness: ', self.fitness
        print self.rs_list
        
        
########################################################################
#                             Driver                                  #
########################################################################
def main():
    all_district = readData("all-rc.csv", "allschools.csv")
    n = 15
    start = time.time()
    start2 = time.clock()
    children = []
    best_fit = float('inf')
    king = None

    fitness_sum = 0
    for i in range(n):
        children.append(all_district.spawn())
        fitness_sum += children[i][0].fitness 
        if children[i][1].fitness < best_fit:
            king = children[i][1]
            best_fit = king.fitness
# print 'the best fitness we found was', king.fitness
# mean = fitness_sum / n
# print 'the mean fitness was ', mean
# children[11][1].pretty_print()
# children[11][1].crossover(children[2][1], all_district).pretty_print()
# children[10][1].mutate(all_district).pretty_print()

#print 'the total number of overcapacity assignments is ', over_capacity_assignment_count
#print 'The process took ', time.time() - start, ' to create ', n, ' assignments with ', len(all_district.road_list), ' roads'
if __name__ == "__main__":
    main()