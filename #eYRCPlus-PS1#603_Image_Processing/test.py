import numpy as np
import cv2

#Teams can add other helper functions
#which can be added here

def play(im):
		#######   training part    ###############
	samples = np.loadtxt('generalsamples.data',np.float32)
	responses = np.loadtxt('generalresponses.data',np.float32)
	responses = responses.reshape((responses.size,1))

	model = cv2.KNearest()
	model.train(samples,responses)

	############################# testing part  #######################

	#im = cv2.imread('test_image1.jpg')
	#out = np.zeros(im.shape,np.uint8)
	gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
	#cv2.imshow('basic',im)
	######################Remove the unwanted part ########
	q,k=thresh.shape
	#print q,k
	for i in range(0,50):
		for j in range(0,k):
			thresh[i][j]=0
	for i in range(360,q):
		for j in range(0,450):
			thresh[i][j]=0
					
	##############################crop the image##########
	h,w,c = im.shape
	crop = thresh[50:,:]

	D1 = crop[:,:(w/2.4)]
	D2 = crop[:,(w/2.2):]

	#######################################################

	###########################For D1############################
	print "D1=[",
	outD1=[]
	outD1=[]
	#find countours in threshold image in D1
	useFullCon=[]
	templist=[]

	contoursd1, hierarchy = cv2.findContours(D1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for aws in range(len(contoursd1)):
		area=cv2.contourArea(contoursd1[aws])
		if area<8000 and area>6000:
			#print "area of ",aws,"is",area
			cv2.drawContours(D1,contoursd1,aws,(255,255,255),2)
			useFullCon.append(aws)
			#print cv2.contourArea(contoursd1[i])
	useFullCon.reverse()		
	#print useFullCon

	for use in range(len(useFullCon)):
		#print use
		[x,y,w,h] = cv2.boundingRect(contoursd1[useFullCon[use]])
		cv2.rectangle(D1,(x,y),(x+w,y+h),(0,255,0),1)
		outD1=[]
		roi = D1[y:y+h,x:x+w]
		#cv2.imshow('roi',roi)
		contours2,hierarchy = cv2.findContours(roi,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		for cnt1 in contours2:
				if cv2.contourArea(cnt1)>450 and cv2.contourArea(cnt1)<6000:
					[x,y,w,h] = cv2.boundingRect(cnt1)

					if  h>28:
						cv2.rectangle(roi,(x,y),(x+w,y+h),(0,255,0),1)
						roi2 = roi[y:y+h,x:x+w]
						roismall = cv2.resize(roi2,(10,10))
						roismall = roismall.reshape((1,100))
						roismall = np.float32(roismall)
						retval, results, neigh_resp, dists = model.find_nearest(roismall, k = 1)
						string2 = str(int((results[0][0])))
						outD1.append(string2)
						print ''.join(outD1),",",
	#cv2.putText(out,string2,(x+500,y+h),0,1,(0,255,0))
	print "]"
	print "D2=",
	#find countours in threshold image in D2
	useFullCon=[]
	outD2=[]
	chiken=[]
	location_of_D2=[]
	loation_of_fulldigits=[]
	#Find all the contours
	contours, hierarchy = cv2.findContours(D2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for aws in range(len(contours)):
		area=cv2.contourArea(contours[aws])
		#keep only those contours whose area matches the square box thus to get only the box location
		if area<8000 and area>6000:
			#print "area of ",aws,"is",area
			cv2.drawContours(D2,contours,aws,(255,255,255),2)
			useFullCon.append(aws)
			#print cv2.contourArea(contours[i])
	#now we have the ROI from the big image then reverse the to get them in acending order
	useFullCon.reverse()		
	
	# now take each small ROI and then devide it in half and then find the contours in that part make that part ROI
	#simply divide the ROI in to half
	for use in range(len(useFullCon)):
		#print use
        #code for the full D2
		
		[x,y,w,h] = cv2.boundingRect(contours[useFullCon[use]])
		#cv2.rectangle(D2,(x,y),(x+w,y+h),(0,255,0),1)
		roi = D2[y:y+h,x:x+w]
		
		#cv2.imshow('roi',roi)
		contours1,hierarchy = cv2.findContours(roi,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		
		for cnt1 in contours1:
				if cv2.contourArea(cnt1)>450 and cv2.contourArea(cnt1)<6000:
					loation_of_fulldigits.append(use)
					[x,y,w,h] = cv2.boundingRect(cnt1)
					

					if  h>28:
						cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,255),1)
						roi2 = roi[y:y+h,x:x+w]
						roismall = cv2.resize(roi2,(10,10))
						roismall = roismall.reshape((1,100))
						roismall = np.float32(roismall)
						retval, results, neigh_resp, dists = model.find_nearest(roismall, k = 1)
						string2 = str(int((results[0][0])))
						temp= int(string2)
						chiken.append(temp)
						#outD2.append(string2)
						
		#code for the 1st half of D2
		[x,y,w,h] = cv2.boundingRect(contours[useFullCon[use]])
		#cv2.rectangle(D2,(x,y),(x+w,y+h),(0,255,0),1)
		roi = D2[y:y+h,x:x+w/2]
		
		#cv2.imshow('roi',roi)
		contours1,hierarchy = cv2.findContours(roi,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		
		for cnt1 in contours1:
				if cv2.contourArea(cnt1)>450 and cv2.contourArea(cnt1)<6000:
					location_of_D2.append(use)
					[x,y,w,h] = cv2.boundingRect(cnt1)
					

					if  h>28:
						cv2.rectangle(roi,(x,y),(x+w,y+h),(0,255,0),1)
						roi2 = roi[y:y+h,x:x+w]
						roismall = cv2.resize(roi2,(10,10))
						roismall = roismall.reshape((1,100))
						roismall = np.float32(roismall)
						retval, results, neigh_resp, dists = model.find_nearest(roismall, k = 1)
						string2 = str(int((results[0][0])))
						#print string2
						templist.append(int(string2))
						temp= int(string2)*10
						#outD2.append(string2)
		
		#code for the 2nd half of D2
		[x,y,w,h] = cv2.boundingRect(contours[useFullCon[use]])
		#cv2.rectangle(D2,(x,y),(x+w,y+h),(0,255,0),1)
		
		roi = D2[y:y+h,x+w/2:x+w]
		#cv2.imshow('roi',roi)
		contours1,hierarchy = cv2.findContours(roi,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		
		for cnt1 in contours1:
				if cv2.contourArea(cnt1)>450 and cv2.contourArea(cnt1)<6000:
					[x,y,w,h] = cv2.boundingRect(cnt1)
					

					if  h>28:
						cv2.rectangle(roi,(x,y),(x+w,y+h),(0,255,0),1)
						roi2 = roi[y:y+h,x:x+w]
						roismall = cv2.resize(roi2,(10,10))
						roismall = roismall.reshape((1,100))
						roismall = np.float32(roismall)
						retval, results, neigh_resp, dists = model.find_nearest(roismall, k = 1)
						string2 = str(int((results[0][0])))
						#print string2
						templist.append(int(string2))
						final=temp+ int(string2)
						outD2.append(final)
		'''
		if outD2==[]:
			pass
		else:
			outD2.sort()
			#print [use,''.join(outD2)],
	#2 seperate output for location and data	'''
	'''
	for listofdigits in outD2:
		singledigit=outD2[0]%10
		templist.append(singledigit)
		templist=outD2[0]/10
	'''
	#print templist
	#print "loation_of_fulldigits",loation_of_fulldigits
	#print chiken
	differenceNumber=set(chiken).difference(templist)
	num=list(differenceNumber)
	#print num[0]
	for numlocation in range(0,len(chiken)):
		#print  "numlocation",numlocation
		if num[0]==chiken[numlocation]:
			indexofmissing=numlocation
			#print "yes match found ",numlocation
	location_of_D2.append(loation_of_fulldigits[indexofmissing])
	print location_of_D2
	#print "location of missing",loation_of_fulldigits[indexofmissing]
	outD2.append(num[0])
	print outD2
	########Display the main image with contours##########
	#find countours in threshold image
	contoursf, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	#print len(contoursf)
	for l in range(len(contoursf)):
		area=cv2.contourArea(contoursf[l])
		if area<6000 and area>450:
			cv2.drawContours(im,contoursf,l,(0,255,0),2)
	#######################################################	
	
	cv2.imshow('image',im)
	
	cv2.waitKey(0)
	cv2.destroyAllWindows()
if __name__ == "__main__":
    #code for checking output for single image
    img = cv2.imread('test_images/Puzzle Solver 1.jpg')
    play(img)
    
