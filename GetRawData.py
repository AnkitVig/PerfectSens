import csv
import math
import numpy as np
from numpy import linalg as LA
from itertools import combinations


def support_degree(sensvallist,k):
    expo = np.empty((k, k))
    for x in range(0,k):
        sensvallist[x] = float(sensvallist[x])
        print("val of sensor", sensvallist[x])
        #r = np.sensvallist[x]
        #answer = np.abs(r - r[:, None])
        #print(answer)
    for y in range(0, k):
       for z in range(0, k):
           ans = abs(sensvallist[y]-sensvallist[z])

           expo[y][z]= math.exp(-ans)
          # print( math.exp(-ans))
         #S  print(aaa)
          # print(z)

    print(expo)

    eigenvalues, eigenvectors = LA.eig(expo)
    print ("Eigen Values: ",eigenvalues)
    print("Eigen Vectors: ", eigenvectors)

    principal_component = np.empty(k)
    for r in range(0,k):
        for c in range(0,k):
            principal_component[r] = principal_component[r] + eigenvalues[c]*eigenvectors[r][c]


    r = 0
    contribution_rate = np.empty(k)
    egval_sum = 0
    for r in range(0,k):
        egval_sum = egval_sum + eigenvalues[r]
        contribution_rate[r] = eigenvalues[r]/egval_sum

    r = 0
    sum_contribution_rate = 0
    for r in range(0,k):
        sum_contribution_rate = sum_contribution_rate+contribution_rate[r]

    r = 0
    integrated_support_degree = 0
    for r in range(0,k):
        integrated_support_degree = integrated_support_degree + principal_component[r]*contribution_rate[r]

    print("egval_sum", egval_sum)
    print("contribution_rate",contribution_rate)
    print("sum_contribution_rate",sum_contribution_rate)
    print("integrated_support_degree: ", integrated_support_degree)





    arr = []
    for i in range(k):
        arr.append([])
        for j in range(k):
            arr[i].append(i * j)
    sensvallist.clear()
    #print(mylist)

class sensor(object):
    def __init__(self, time, name,val):
        self.time = time
        self.name = name
        self.val = val

   # creating list

sensorlist = []
sensvallist = []

x = input("Enter File You Want to read: ")
with open(x) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
            print(f' Time :{row[0]} Name: {row[1]} Value: {row[2]}.')
            # appending instances to list
            x = row[0]
            y = row[1]
            z = row[2]
            sensorlist.append(sensor(x, y, z))
            line_count += 1
    print(f'Processed {line_count} lines.')

    first_time = sensorlist[0].time
    count = 0
    i = 0
    j = 0
    #while i < line_count:
    while j < line_count-2:
        temp2 = sensorlist[j].time
        if temp2 == first_time:
            k=0
            while i<line_count:
                #print("Here 1")
                temp = sensorlist[i].time
                if temp == first_time:
                    sensvallist.insert(k, int(sensorlist[i].val))
                    k += 1
                    count += 1
                else:
                    first_time = sensorlist[i].time
                    break
                i += 1
            support_degree(sensvallist, k)
        j += 1














