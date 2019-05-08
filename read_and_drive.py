from __future__ import division
import csv
import random
import math
import time
import copy

k = 250 
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
        for row in rc_dataset:
            #testing stopping condition for small datasets
            row_count += 1
            # if row_count == k:
            #     break
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
        schools_dataset.pop(0) #take out the header
        for row in schools_dataset:
            school_list.append(School(float(row[4])))

        return District(road_list, school_list)   
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
        self.running_cap = [0] * len(self.school_list)#re-initialize the running capacity and school populations
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
            
        assign_obj.calcFitness(self.school_list, self)
        if assign_obj.fitness < best_fitness:
            if assign_obj.fitness < 10:
                assign_obj.pretty_print()
            best_fitness = assign_obj.fitness
            king = copy.deepcopy(assign_obj)
        return assign_obj, king
        
        
class Assignment:
    def __init__(self, assignment):
        self.rs_list = assignment
        self.fitness = float('inf')
        
    #use Lena's function here
    def calcFitness(self, populated_school_list, district): #populated_school_list is the number of people (entry) in each school (id)
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
        
    def pretty_print(self):
        print 'the child has fitness: ', self.fitness

 

BG_district = readData("rc-greyviolet.csv", "schoolsgreyviolet.csv")
n = 100
start = time.time()
start2 = time.clock()
children = []
best_fit = float('inf')
king = None
for i in range(n):
    children.append(BG_district.spawn())
    children[i][0].pretty_print()
    if children[i][1].fitness < best_fit:
        king = children[i][1]
        best_fit = king.fitness
        print 'the new king has fitness ', king.fitness
print 'the best fitness we found was', king.fitness    

print 'the total number of overcapacity assignments is ', over_capacity_assignment_count
print 'The process took ', time.time() - start, ' to create ', n, ' assignments with ', len(BG_district.road_list), ' roads'