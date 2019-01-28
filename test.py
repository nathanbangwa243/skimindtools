#-*-coding utf-8 -*-

# main function
from .setheory import createIntervalOfSet

set1 = {1, 2, 3, 4, 5}
set2 = {1, 4, 6, 7, 8}
set3 = {0, 2, 4, 9, 10}
set4 = {0, 2, 4, 9, 11}
set5 = {0, 2, 4, 17, 18}

# list of sets targets 
listOfSets = [set1, set2, set3, set4, set5]

dictOfSets = {"one": set1, 'two': set2, 'three': set3, 'four': set4, 'five': set5}

#listOfSets = [set1, set4]


# start treatement
response = createIntervalOfSet(listOfSets=listOfSets, mutualx=True)
response1 = createIntervalOfSet(listOfSets=dictOfSets)
for key, value in response1.items():
    print("%s : %s" % (key, str(value)))
#print (response == response1)