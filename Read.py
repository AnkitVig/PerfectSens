import csv
import math
from datetime import datetime

import numpy as np
from numpy import linalg as LA
from tkinter import *
from tkinter import filedialog
import sys
import tkinter as tk
from subprocess import *



class sensor(object):
    def __init__(self, time, name,val):
        self.time = time
        self.name = name
        self.val = val
sensorlist = []
sensvallist = []
sensnamelist = []
senstimelist = []
group_count = 0



def start():

        x=app.entry_1.get()
        #x = root.filename

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
            alert = 0
            while j < line_count:
                temp2 = sensorlist[j].time
                if temp2 == first_time:
                    k=0
                    while i<line_count:
                        #print("Here 1")
                        temp = sensorlist[i].time
                        if temp == first_time:
                            sensnamelist.insert(k, str(sensorlist[i].name))
                            #print(sensnamelist[i])
                            senstimelist.insert(k, str(sensorlist[i].time))
                            sensvallist.insert(k, float(sensorlist[i].val))
                            #print(k)
                            #print(sensnamelist[i])
                            k += 1
                            count += 1
                        else:
                            first_time = sensorlist[i].time
                            break
                        i += 1

                    support_degree(sensvallist,sensnamelist,senstimelist, k)
                print(j)
                j =i

def support_degree(sensvallist,sensnamelist,senstimelist,k):
        print(k)
        #sens_name = np.empty(k)
        expo = np.empty((k, k))
        for x in range(0,k):
            #sens_name[x] = sensnamelist[x]
            sensvallist[x] = float(sensvallist[x])
            print("val of sensor ",sensnamelist[x]," at time ",senstimelist[x],"is :", sensvallist[x])
            print()


        for y in range(0, k):
           for z in range(0, k):
               ans = abs(float(sensvallist[y]-sensvallist[z]))
               print(ans)
               expo[y][z]= math.exp(-ans)
               print(y, "     ", z,"        ",expo[y][z])

        egnval_egnvec(expo,sensvallist,sensnamelist,senstimelist,k)


        arr = []
        for i in range(k):
            arr.append([])
            for j in range(k):
                arr[i].append(i * j)
        #sensnamelist.clear()
        sensvallist.clear()
        sensnamelist.clear()
        senstimelist.clear()


def egnval_egnvec(expo,sensvallist,sensnamelist,senstimelist,k):


        eigenvalues, eigenvectors = LA.eig(expo)
        print ("Eigen Values: ",eigenvalues)
        eigenvectors_trans=np.negative(eigenvectors.transpose())
        print("Eigen Vectors: ", eigenvectors_trans)

        cal_principal_component(expo,eigenvalues,eigenvectors_trans,sensvallist, sensnamelist,senstimelist,k)



def cal_principal_component(expo,eigenvalues,eigenvectors_trans,sensvallist, sensnamelist,senstimelist,k):
        r=0
        c=0
        z=0
        principal_component = np.empty((k,k))
        for z in range(0, k):
            for r in range(0,k):
                for c in range(0,k):
                    principal_component[z][r] += eigenvectors_trans[z][c] * expo[r][c]
                   # principal_component[z][r] = principal_component[r] + eigenvalues[c]*eigenvectors[r][c]

        print("Principal compnent :", principal_component)
        cal_contribution_rate(eigenvalues,principal_component,sensvallist, sensnamelist,senstimelist,k)


def cal_contribution_rate(eigenvalues,principal_component,sensvallist, sensnamelist,senstimelist,k):
    r = 0
    c = 0
    contribution_rate = np.empty(k)
    sum_contribution_rate = np.empty(k)
    egval_sum = 0
    for c in range(0,k):
        egval_sum = egval_sum + eigenvalues[c]
    for r in range(0,k):
        contribution_rate[r] = eigenvalues[r]/egval_sum
    print("contribution_rate\n", contribution_rate)
    r = 0
    sum = 0
    for r in range(0,k):
        sum += contribution_rate[r]
        sum_contribution_rate[r] = sum
    cal_integrated_support_degree(contribution_rate, sum_contribution_rate, principal_component,sensvallist, sensnamelist,senstimelist, k)

def cal_integrated_support_degree(contribution_rate, sum_contribution_rate,principal_component,sensvallist, sensnamelist,senstimelist, k):
    i = 0
    counter = 0
    for i in range(0, k):
        if (sum_contribution_rate[i] * 100 <= 85):
            counter += 1
        else:
            break

    r = 0
    calc_integrated_support_degree = np.empty((k, k))
    for r in range(0, counter):
        for c in range(0, k):
            calc_integrated_support_degree[r][c] = principal_component[r][c] * contribution_rate[r]

    r = 0
    integrated_support_degree = np.empty(k)
    for r in range(0, k):
        sum = 0
        for c in range(0, counter):
            sum += calc_integrated_support_degree[c][r]
        integrated_support_degree[r] = sum

    sum_integrated_support_degree = 0
    for r in range(0, k):
        sum_integrated_support_degree += integrated_support_degree[r]

    print("integrated_support_degree: ", integrated_support_degree)
    print(" sum integrated_support_degree: ", sum_integrated_support_degree)
    X_Thresh = abs(1/k*(sum_integrated_support_degree))*(0.7)

    print(" Threshold: ", X_Thresh)

    eliminate_sensor(integrated_support_degree, sum_integrated_support_degree, X_Thresh,sensvallist,sensnamelist, senstimelist, k)


def eliminate_sensor(integrated_support_degree, sum_integrated_support_degree, X_Thresh,sensvallist,sensnamelist, senstimelist, k):
        i = 0
        size_eliminated = 0
        counter_outof_range = np.empty(k)
        #counter_outof_range =
        for i in range(0, k):
            if(abs(integrated_support_degree[i])< X_Thresh):
              print("i :", i)
              counter_outof_range[size_eliminated]= i
              size_eliminated +=1
            else:
                continue
                  #print("Senser Name : ",sens_name[r])
        calc_weight_cofficient(counter_outof_range, size_eliminated, integrated_support_degree, sum_integrated_support_degree,sensvallist, sensnamelist, senstimelist, k)
        print("counter out:", counter_outof_range)


def calc_weight_cofficient(counter_outof_range, size_eliminated, integrated_support_degree,sum_integrated_support_degree,sensvallist, sensnamelist,senstimelist,k):
        i = 0
        z = 0
        weight_cofficient = np.empty(k)
        for i in range(0, k):
            for z in range(0,k):
                if (i != counter_outof_range[z]):
                    weight_cofficient[i] = integrated_support_degree[i] / sum_integrated_support_degree
            print("name and time of sensor ", sensnamelist[i], senstimelist[i])
        print("weight_cofficient", weight_cofficient)
        valid_fused_output(counter_outof_range,size_eliminated,weight_cofficient,sensvallist, sensnamelist, senstimelist, k)

def valid_fused_output(counter_outof_range,size_eliminated, weight_cofficient,sensvallist, sensnamelist, senstimelist,k):
    fused_output = 0

    for i in range(0,k):
        fused_output += weight_cofficient[i] * sensvallist[i]
    global group_count
    group_count+=1
    write_csv(counter_outof_range, size_eliminated, sensvallist, sensnamelist, senstimelist, fused_output, k, group_count)


def write_csv(counter_outof_range, size_eliminated, sensvallist, sensnamelist, senstimelist, fused_output, k, group_count):
    if ((group_count - 1) == 0):
        with open("result.csv", "w+", newline='') as f:
            #thewriter = csv.writer(f)
            fieldnames = ['Time','Name','Value']
            thewriter = csv.DictWriter(f, fieldnames = fieldnames)
            #thewriter.writerow(['Time','Name','Value'])
            r = 0
            thewriter.writeheader()
            for r in range(0, k):
                for i in range(0, size_eliminated):
                        if (r != counter_outof_range[i]):
                            thewriter.writerow({'Time' : senstimelist[r], 'Name' : sensnamelist[r],'Value' : sensvallist[r]})
    else:
        with open("result.csv", "a", newline='') as f:
            #thewriter = csv.writer(f)
            fieldnames = ['Time','Name','Value']
            thewriter = csv.DictWriter(f, fieldnames = fieldnames)
            #thewriter.writerow(['Time','Name','Value'])
            r = 0
            thewriter.writeheader()
            for r in range(0, k):
                for i in range(0, size_eliminated):
                        if (r != counter_outof_range[i]):
                            thewriter.writerow({'Time' : senstimelist[r], 'Name' : sensnamelist[r],'Value' : sensvallist[r]})


class MainApplication():
    def __init__(self, master=None):

        self.root = master
#        self.testInstance = sensor()
        self.root.geometry('500x500')
        self.root.title("Perfect Sense")
        self.label_0 = Label(self.root, text="Perfect Sense", width=20, font=("bold", 20))
        self.label_0.place(x=90, y=53)

        self.label_1 = Label(self.root, text="FIle Name", width=20, font=("bold", 10))
        self.label_1.place(x=80, y=130)

        self.entry_1 = Entry(self.root)
        self.entry_1.place(x=200, y=130)
        print(self.entry_1)
        print(self.entry_1.get())
        Button(self.root, text='...', height=1, width=2, bg='brown', fg='white',
                            command=self.fileopen).place(x=330, y=130)
        Button(self.root, text='Submit', width=20, bg='brown', fg='white',
                                  command= start).place(x=180, y=180)

        #def __init__(self):

    def fileopen(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                        filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        self.file_path = self.filename
        print(self.file_path)
        self.entry_1.insert(0, self.file_path)



root = tk.Tk()
app = MainApplication(master=root)
root.mainloop()