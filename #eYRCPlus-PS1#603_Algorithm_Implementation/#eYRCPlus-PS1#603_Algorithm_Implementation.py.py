#Eyantra Task2
import cv2
import numpy
import copy
#open the Text file for test inputs and then get the text into lists
fo = open("test_inputs/Test_input0.txt", "r")
D1=[map(int, fo.readline().split())]
#get the number list in the newD1 list 
newD1=D1[0]
#create a copy of that variable
lstBackup=copy.copy(newD1)
D2=[map(int, fo.readline().split())]
newD2=D2[0]

#deleteIndex is the function that delets the used number from the given list
def deleteIndex(indexOne,indexTwo,delist):
		#Delet number using index list
		del delist[indexTwo]
		del delist[indexOne]
		
# sumCheck function takes 1 number from D2 and finds the 
# the combination of inputs that make the sum		
def sumCheck(sum,lst):
	#find the length of the String D1
	total=len(lst)
	for n in range(0,total-1):
		indexOne=n
		
		if total==0:
			break
		else:
			for j in range(0,total-1):
				#add the 2 numbers from D2 if the addition is 
				#is equal to the sum then delet the 2 numbers from the list
				indexTwo=j+1
				added=lst[n]+lst[j+1]
				if added==sum:
					print sum,"=",lst[n],"+",lst[j+1]
					deleteIndex(indexOne,indexTwo,lst)
					return 0;
					



#rotat the list that is passed through the function
def rotate(l,n):
    return l[n:] + l[:n]

#gets the length of the function	
rep=len(newD1)					
for each_list in range(0,rep-1):
	#print the new solution evert time
	print "New Solution"	
	for num in newD2:
		#send each number from list D2 to the sumCheck Function to compute the 
		#sumCheck with the list 
		sumCheck(num,lstBackup)
		
	#Rotate the list using rotate
	newD1=rotate(newD1,1)
	#again copy the roated list to lstBackup to be sent in the function
	lstBackup=copy.copy(newD1)