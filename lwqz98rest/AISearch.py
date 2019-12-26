import numpy as np
import fileinput
import math
import random
import statistics

#########    Read file and place distances in a matrix (Task 1) ##########################3
def readFile(file):
    mylist=[]
    with open(file) as f_in:
        lines = (line.rstrip() for line in f_in) # All lines including the blank ones
        lines = list(line for line in lines if line) # Non-blank lines
        #print(lines)
        return lines

    
def createMatrix(content):
    newlist=[]
    mylist=[]
    counter=0
    #If there is only one line
    if (len(content)==1):
    #Convert list to string
        print(content)
        string=''.join(str(e) for e in content)
    #Split the string using the commas
        string=string.split(",")
    #Ignore the name and size and start reading the cities
        for i in string[2:]:
    #If the data read is a number (no dirty data) add them to a new list
            if (i.isdigit()==True):
                newlist.append(i)
    #If dirty data is found ignore the dirty data and get the number only
            else:
                for j in i:
                    if (j.isdigit()==False):
                        newnumb=i.replace(j,"")             
                        newlist.append(newnumb)
        newstring=''.join(str(e) for e in newlist)                     
    #Get the size of the problem    
        size=[int(s) for s in string[1].split() if s.isdigit()]
    #Create a matrix of 0s
        matrix=np.zeros((size[0],size[0]),dtype=int)   
        
    #Iterate through the string and place everything in a list
        for i in newlist:
            mylist.append(i)
    #Place numbers in the upper triangle of the matrix
        for row in range(size[0]):
            for col in range(size[0]):
                if (row>=col):
                    matrix[row,col]=0
                else:
                    matrix[row,col]=mylist[counter]
                    couter=counter+1
                    del mylist[counter]
    #Copy the upper triangle of the matrix to the lower triangle to have a complete matrix
        for i in range(size[0]):
            for j in range(i, size[0]):
                matrix[j][i] = matrix[i][j]       
        return matrix
    else:
        mystr = ''.join([line.strip() for line in content])
        mystr1=mystr.split(',')
        size=[int(s) for s in mystr1[1].split() if s.isdigit()]
        matrix=np.zeros((size[0],size[0]),dtype=int)
        for i in mystr1[2:]:
            mylist.append(i)
        for row in range(size[0]):
            for col in range(size[0]):
                if (row>=col):
                    matrix[row,col]=0
                else:
                    matrix[row,col]=mylist[counter]
                    couter=counter+1
                    del mylist[counter]
    #Copy the upper triangle of the matrix to the lower triangle to have a complete matrix
        for i in range(size[0]):
            for j in range(i, size[0]):
                matrix[j][i] = matrix[i][j]       
        return matrix



###################  simulated annealing   ###################


        

def Distance(mat,tour): #find total distance in a tour
    counter=0
    totalDistance=0
    distance=0
    while counter != (len(tour)-1):
        city1=tour[counter]
        city2=tour[counter+1]
        distance=mat[city1][city2]
        totalDistance=totalDistance+distance
        counter=counter+1
    firstNode=tour[0]
    lastNode=tour[len(tour)-1]
    dist=mat[firstNode][lastNode]
    totalDistance=totalDistance+dist
    return totalDistance
        
        
        

def generateRandomState(size): #generate a random tour
    tour=[]
    for i in range(0,size):
        x = random.randint(0,size-1)
        while x in tour:
            x = random.randint(0,size-1)
        tour.append(x)
    return tour

def generateNextState(state): #get a tour and swap two cities randomly
    state = state[:]    
    city, city1 = random.sample(range(len(state)), 2)
    state[city], state[city1] = state[city1], state[city]
    return state

   

    
def simulatedAnnealing(mat): #simulated annealing function. Gets only 1 parameter, the matrix
    best_cost=[]
    oldTour=generateRandomState(len(mat)) #generate a random tour
    print("Old tour: ", oldTour)
    oldCost=Distance(mat,oldTour)
    print ("Old Cost: ",oldCost) #find its length
    T=9999999 #high starting temperature
    T_min = 0.00001 #minimum temperature
    beta = 0.9 #constant to multiply temperature with at each round
    while (T>T_min):
        newTour = generateNextState(oldTour) #generate a new tour by swapping two cities with each other of the old tour. The old tour can be the original tour or the most optimal tour that I found so far
        print("New tour: ", newTour)
        newCost = Distance(mat,newTour)
        print("New Cost: ", newCost) #find its length
        T=T*beta #reduce Temperature
        De=-(newCost-oldCost) #find the difference in the lengths of the two tours
        if (De>=0): #if the length of the new tour is better then swap the variables old tour and new tour, and now the variable old tour contains the most optimal tour. The same is done with the old cost and new cost variables where these variables store the lengths of tours
            print("De>0")
            print("old Cost:", oldCost)
            print("new Cost:", newCost)
            oldCost=newCost
            oldTour=newTour
        else:
            print("De<0") #if the length of the old tour is better than the length of the new tour then it has a probability to still become the most efficient tour. This depends on the acceptance probability
            print("old Cost:", oldCost)
            print("new Cost:", newCost)
            prob=(2.71728)**((De)/T) #acceptance probability
            if (prob>=0.9): #if this probability is greater than 0.9 then the new tour and new cost will become the most optimal tour and cost regardless of the fact that they are worse than the old tour.
                print("ACCEPT")
                oldCost=newCost #this helps the algorithm to jump out of any local optimums
                oldTour=newTour
    
    print("new Cost: ",oldCost)
    shortDist=Distance(mat,oldTour)
    final_path = [x+1 for x in oldTour] #add one since my list starts from zero but we want to start at 1


    print("Path: ",final_path)
    print("Shortest Distance: ", shortDist )
    return final_path,shortDist
       
        

###################  Genetic Alg   ###################
        


def swap(repeatList,skipElements,child1): #swap cities that are found twice in a tour with the cities that are not found in the tour.Their first occurance is swapped
    found=False    
    for i in range (0,len(child1)):
        if (found==True):
            break
        for j in range(0,len(repeatList)):
            if (child1[i]==repeatList[j]):
                child1[i]=skipElements[j]
                if (j==(len(repeatList)-1)):
                    found=True
                    break

def findRepeatedCities(child1): #find repeated cities and place them in a list. Also place in a list the cities that are not in a tour
    length = len(child1) 
    repeatList = []
    for i in range(length): 
        j = i + 1
        for k in range(j, length): 
            if child1[i] == child1[k] and child1[i] not in repeatList: 
                repeatList.append(child1[i]) 
    
    skipElements=[]
    for i in range (0,len(child1)):
        if (i not in child1):
            skipElements.append(i)
    return repeatList,skipElements

def checkRepeatedCities(seq): #check to see if there are any duplicate cities
    return any(seq.count(x) > 1 for x in seq)


def geneticAlgorithm(mat): #this is the genetic algorithm and it gets only 1 parameter, the matrix
    population=[]   
    counter=0
    for i in range (0,100): #generate 100 random tours
        aa=generateRandomState(len(mat))
        population.append(aa)
    if (checkRepeatedCities(population)): #check to see if there are any repeated cities
        return   
    while counter<=20: #iterate 20 times
        newPop=[]
        newPopDist=[]
        
        for i in range (1,len(population)):
            newPopulation=[]
            distanceList=[]
            probList=[]
            for j in population: #find the distance of each tour and place it in a list
                distanceList.append(Distance(mat,j))
            sumDistance=sum(distanceList)

            numbs=[]
            for j in distanceList: #find the fitness probability of each tour to be chosen as a parent
                prob= sumDistance/j             
                probList.append(prob)
            probListCopy=[]
            probListCopy=probList.copy()
            

            probListCopy.sort()
            percentile=0.80*len(probListCopy) #choose a percentile of the population where 2 random tours will be selected as parents. In this case the percetile is 80% and parents will be selected from 80% and above
            percentile1=math.ceil(percentile)

            percList=[]
            for j in range (0,len(probListCopy)): #place tours that are in the above the 80% percentile in a new list
                if (j>percentile1):
                    percList.append(probListCopy[j])
        
            rand1=random.randint(1,len(percList)-1) #generate 2 random numbers
            rand2=random.randint(1,len(percList)-1)
            while rand1 == rand2:
                rand2=random.randint(0,len(percList)-1)

            
            
            lowest = percList[rand1]  #use these two random numbers to select a probability from that percentile and then correspond that probability to its tour
            lowest2 = percList[rand2] #do this two times to select two tours
            a=probList.index(lowest) #the two tours will now be called parents
            b=probList.index(lowest2)

            x=population[a]
            y=population[b]
            prob1=Distance(mat,x)/sumDistance
            prob2=Distance(mat,y)/sumDistance

            distx=Distance(mat,x) #find the parents distances
            disty=Distance(mat,y)

            rand3=random.randint(0,len(mat)-1) #generate a random number from 0 to the length of the list and that random number will be used as the crossover point.
            temp1=0
            child1=[]
            child2=[]
            for m in range (rand3): #create their children. This is done by joining the cities which are to the left of the crossover point of the first parent 
                                    #with the cities to the right of the crossover point of the second parent. Likewise the same procedure is followed for child 2.
                child1.append(x[m])
            for j in range (rand3,len(x)):   
                child1.append(y[j])
            for k in range (rand3):  #the cities which are to the left of the crossover point of the second parent are joint with the cities to the right of the crossover point of the first parent
                child2.append(y[k])
            for l in range (rand3,len(x)):
                child2.append(x[l])
            
            child1Distance= Distance(mat,child1) #find the distances of the children
            child2Distance= Distance(mat,child2)          

            repeatList,skipElements=findRepeatedCities(child1) #check if there are any repeated cities in the children and also any cities that were not found in the tour
            repeatList1,skipElements1=findRepeatedCities(child2) #if there are any repeated cities swap the first occurance of the repeated cities with the cities that are not found anywhere in the tour
            swap(repeatList,skipElements,child1)
            swap(repeatList1,skipElements1,child2) #do this for both children

            newPop.append(child1)
            newPop.append(child2) #add both children to a new list 
            newPopDist.append(child1Distance) #add the length of the tours of the children to a new list
            newPopDist.append(child2Distance)
            if (checkRepeatedCities(child1) or (checkRepeatedCities(child2))): #check if there are any repeated cities
                return
        print("Counter: ", counter)
        p=0
        for j in newPop:
            rand4=random.random() #assign each child a random probability
            
            if (rand4<0.1): #if that probability is less than 0.1 then that child (tour) will mutate. Two cities of that child (tour) will be swapped with each other
                del newPop[p]
                newState=generateNextState(j)
                newPop.insert(p,newState) #replace the child with the mutated version of that child
            p=p+1
                
        counter=counter+1
    temp=0
    temp2=[]
    for j in newPop:
        temp2.append(Distance(mat,j)) #find the lengths of tours of the list newPop (including the mutations)
    mini= min(temp2) #find the minimum length
    for j in newPop:
        if (Distance(mat,j)==mini): #get the tour with the minimum length
            temp=j
    
    shortDist=Distance(mat,temp)
    print("DISTANCE: ", Distance(mat,temp) )
  
    final_path = [x+1 for x in temp] #add one since my list starts from zero but we want to start at 1
    print("Path: ",final_path)
    return final_path,shortDist


                
            

path="ExperimentTourfileA/"  #The results of the code for simulated annealing are stored in the folder named ExperimentTourfileA
                            #in that way the original tour results are not affected by any tests

c=readFile("NEWAISearchfile012.txt")   
d=createMatrix(c)
final_path1,shortDist1=simulatedAnnealing(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile017.txt")   
d=createMatrix(c)
final_path1,shortDist1=simulatedAnnealing(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile021.txt")   
d=createMatrix(c)
final_path1,shortDist1=simulatedAnnealing(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile026.txt")   
d=createMatrix(c)
final_path1,shortDist1=simulatedAnnealing(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile042.txt")   
d=createMatrix(c)
final_path1,shortDist1=simulatedAnnealing(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile048.txt")   
d=createMatrix(c)
final_path1,shortDist1=simulatedAnnealing(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile058.txt")   
d=createMatrix(c)
final_path1,shortDist1=simulatedAnnealing(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile175.txt")   
d=createMatrix(c)
final_path1,shortDist1=simulatedAnnealing(d)
file = open(path+"tourNEWAISearchfile" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile180.txt")   
d=createMatrix(c)
final_path1,shortDist1=simulatedAnnealing(d)
file = open(path+"tourNEWAISearchfile" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile535.txt")   
d=createMatrix(c)
final_path1,shortDist1=simulatedAnnealing(d)
file = open(path+"tourNEWAISearchfile" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()



path="ExperimentTourfileB/"  #The results of the code for genetic algorithm are stored in the folder named ExperimentTourfileB
                            #in that way the original tour results are not affected by any tests

c=readFile("NEWAISearchfile012.txt")   
d=createMatrix(c)
final_path1,shortDist1=geneticAlgorithm(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile017.txt")   
d=createMatrix(c)
final_path1,shortDist1=geneticAlgorithm(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile021.txt")   
d=createMatrix(c)
final_path1,shortDist1=geneticAlgorithm(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile026.txt")   
d=createMatrix(c)
final_path1,shortDist1=geneticAlgorithm(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile042.txt")   
d=createMatrix(c)
final_path1,shortDist1=geneticAlgorithm(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile048.txt")   
d=createMatrix(c)
final_path1,shortDist1=geneticAlgorithm(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile058.txt")   
d=createMatrix(c)
final_path1,shortDist1=geneticAlgorithm(d)
file = open(path+"tourNEWAISearchfile0" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile0" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile175.txt")   
d=createMatrix(c)
final_path1,shortDist1=geneticAlgorithm(d)
file = open(path+"tourNEWAISearchfile" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile180.txt")   
d=createMatrix(c)
final_path1,shortDist1=geneticAlgorithm(d)
file = open(path+"tourNEWAISearchfile" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()

c=readFile("NEWAISearchfile535.txt")   
d=createMatrix(c)
final_path1,shortDist1=geneticAlgorithm(d)
file = open(path+"tourNEWAISearchfile" + str(len(d)) + ".txt" ,"w")
file.write("NAME = AISearchfile" + str(len(d)) + ",")
file.write("\n")
file.write("TOURSIZE = " + str(len(d)) + ",")
file.write("\n")
file.write("LENGTH = " + str(shortDist1) + ",")
file.write("\n")
file.write(','.join(str(e) for e in final_path1))
file.close()











