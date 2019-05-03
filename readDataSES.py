import csv
import random
import math
#temporarily changing .8 to .001 to make testing easier
SPLIT = .05


#Reads a csv of datapoints into an array of datapoint pairs
def readData(filename):
    with open(filename) as csv_file:
        #dialect = csv.Sniffer().sniff(csv_file.read(1024))
        #csv_file.seek(0)
        csv_reader = csv.reader(csv_file,delimiter=',')
        dataset=list(csv_reader)
        schoolIDs = dataset[:0]
        capacities = dataset[:4]
        
        print(schoolIDS[1])
        for row in range(len(schoolIDs)):
                schoolIDs[row] = float(dataset[row])
                capacities[row] = float(capacities[row])

#Splits a dataset into training and test sets with the ratio of constant SPLIT
def splitData(dataset):
    #Shuffle the data points
    random.shuffle(dataset)

    #Find the 80% mark to split the data into train and test
    subset = dataset[:12500]
    split = int(math.floor(len(dataset)*SPLIT))
    train = subset[:10000]
    test = subset[10000:]

    return train, test

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
readData("rc-bluegreen.csv")