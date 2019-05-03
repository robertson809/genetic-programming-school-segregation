import csv
import random
import math
#temporarily changing .8 to .001 to make testing easier
SPLIT = .05


#Reads a csv of datapoints into an array of datapoint pairs
#the with statement works with objects that have enter and exit statements
#so it closes the file when it's done. open is a built in function that 
#returns a file object
def readData(roads, schools):
    with open(roads) as csv_file:
        #dialect = csv.Sniffer().sniff(csv_file.read(1024))
        #csv_file.seek(0)
        #Each row read from the csv file is returned as a list of strings
        reader = csv.reader(csv_file,delimiter=',')
        dataset = list(reader)
        road_list = []
        count = 0
        for row in dataset:
            count += 1
            
            # print 'hello'
            #print row, '1'
            #print row[0], 'shitttyah'
            road_id = int(row[0])
            ses = int(row[3])
            pop = float(row[1])

    
            #print float(row[1]) + 8, 'is a big number'
            schools = row[8:]
            #print 'the ', len(schools), ' school distances are', schools 
            close_schools = []
            for dist in schools:
                if float(dist) < 99999:
                    tup = (schools.index(dist), float(dist))
                    close_schools.append(tup)
            #road = Road(row[])
            #capacities[row] = float(capacities[row])
            if count == 900:
                break
            road_list.append(Road(road_id, ses, pop, close_schools))
        
        print road_list[750].schools
    with open(schools) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        dataset = list(reader)
        for row in dataset
            school_id = row[0]
            cap = row[4]
        
            
        return road_list, school_list
            
        
                
"""Road object has three instances
    SES - 1 LOW
          2 MEDIUM
          3 HIGH
    POP - Population of the school
    Schools - list of five tuples of ID, Distance
    """
class Road:
    def __init__(self, road_id, ses, pop, schools):
        #create instances variables
        self.road_id = road_id
        self.ses = ses  #size of the board
        self.pop = pop  #board state
        self.schools = schools  #solved state
        

#Writes the split data into their own files (only needs to be done once)
def writeData(filename,dataset):
    with open(filename, mode='w') as csv_file:
        data_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in range(len(dataset)):
            data_writer.writerow(dataset[row])

# dataset1_array = readData('dataset2.csv')
# data_tuple = splitData(dataset1_array)
# small_train_2 = data_tuple[0]
# writeData("small_train2.csv", small_train_2)
# small_test_2 = data_tuple[1]
# writeData("small_test2.csv", small_test_2)
readData("rc-bluegreen.csv", "schoolsbluegreenDescribed")