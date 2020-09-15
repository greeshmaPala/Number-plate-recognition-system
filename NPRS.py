

import cv2 
import imutils # to recognizing contours...
import numpy as np #numberpython
from PIL import Image
import pytesseract
import os
import argparse
import time
import pandas as pd
import sys


def fun_state(state):
	
	fstate = 'INVALID FORMAT'
	if state == 'HR':
		fstate = 'HARYANA'	
	elif state == 'AP':
		fstate = 'Andhra Pradesh'
	elif state == 'AR':
		fstate = 'ArunachaL Pradesh'
	elif state == 'AS':
		fstate = 'Assam'
	elif state == 'BR':
		fstate = 'Bihar'
	elif state == 'CG':
		fstate = 'Chhattisgarh'
	elif state == 'GA':
		fstate = 'Goa'
	elif state == 'GJ' :
		fstate = 'Gujarat'
	elif state == 'HP':
		fstate = 'Himachal Pradesh'
	elif state == 'JH':
		fstate = 'Jharkhand'
	elif state == 'KA':
		fstate = 'Karnataka'
	elif state == 'KL':
		fstate = 'Kerala'
	elif state == 'MP':
		fstate = 'Madhya Pradesh'
	elif state == 'MH':
		fstate = 'Maharastra'
	elif state == 'MN':
		fstate = 'Manipur'
	elif state == 'ML':
		fstate = 'Meghalaya'
	elif state == 'MZ':
		fstate = 'Mizoram'
	elif state == 'NL':
		fstate = 'Nagaland'
	elif state == 'OD':
		fstate = 'Odisha'
	elif state == 'PB':
		fstate = 'Punjab'
	elif state == 'RJ':
		fstate = 'Rajasthan'
	elif state == 'SK':
		fstate = 'Sikkim'
	elif state == 'TN':
		fstate = 'Tamil Nadu'
	elif state == 'TS':
		fstate = 'Telangana'
	elif state == 'TR':
		fstate = 'Tripura'
	elif state == 'UP':
		fstate = 'Uttar Pradesh'
	elif state == 'UK':
		fstate = 'Uttarakhand'
	elif state == 'WB':
		fstate = 'West Bengal'
	elif state == 'AN':
		fstate = 'Andaman and Nicobar Island'
	elif state == 'CH':
		fstate = 'Chandigarh'
	elif state == 'DD':
		fstate = 'Dadra and Nagar Haveli and Daman and Diu'
	elif state == 'DL':
		fstate = 'Delhi'
	elif state == 'JK':
		fstate = 'Jammu and Kashmir'
	elif state == 'LA':
		fstate = 'Ladakh'
	elif state == 'LD':
		fstate = 'Lakshadweep'
	elif state == 'PY':
		fstate = 'Puducherry'
###### There are few list of codes that shouldnt be used. They are mentioned below ######
	elif state == 'OR':
		fstate = 'INVALID FORMAT'
	elif state == 'UA':
		fstate = 'INVALID FORMAT'
	return fstate
	print ("State :", fstate)

def fun_valid(district):
	state = district[0] + district[1]
	
	int_district = district[2] + district[3]
	fvalid = 'INVALID'
	if (int_district.isdigit()):
		ld = int(int_district)
		if state == 'HR':
			if ((ld>0 and 91>ld) and (ld != 81 and ld != 85 and ld != 87 and ld != 89)): 
    				fvalid = 'VALID'
		elif state == 'MH':
			if (ld>0 and 51>ld):
				fvalid = 'VALID'
		elif state == 'AP':
			if (ld>0 and 39>ld):
				fvalid = 'VALID'
		elif state == 'DL':
			if (ld>0 and 19>ld):
				fvalid = 'VALID'
		elif state == 'KL':
			if (ld>0 and 70>ld):	
				fvalid = 'VALID'
	else:
		print('Invalid format or Wrong segmentation')	
	return fvalid


def main():
  
#######  GREY SCALE   ########
	img = cv2.imread('mc.jpeg',cv2.IMREAD_COLOR)
	img = imutils.resize(img, width=500 )
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
	gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
	edged = cv2.Canny(gray, 30, 200) #Perform Edge detection

####### CONTOURS #######
	cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	img1=img.copy()
	cv2.drawContours(img1,cnts,-1,(0,255,0),3)
	cv2.waitKey(0)

####### CONTOURS BASED ON AREA #######
#sorts contours based on minimum area 30 and ignores the ones below that
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
	screenCnt = None #will store the number plate contour
	img2 = img1.copy()
	cv2.drawContours(img2,cnts,-1,(0,255,0),3) 
	cv2.waitKey(0)
	count=0
	idx = 'cropped'
	for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            if len(approx) == 4: #chooses contours with 4 corners
                    screenCnt = approx
                    x,y,w,h = cv2.boundingRect(c) #finds co-ordinates of the plate
                    new_img=img[y:y+h,x:x+w]
                    cv2.imwrite('./'+str(idx)+'.png',new_img) #stores the new image
                    idx+=1
                    break

#draws the selected contour on original image        
	cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
	##cv2.imshow("Final image with plate detected",img)
	##cv2.waitKey(0)
	Cropped_loc='cropped.jpeg' #the filename of cropped image
	##cv2.imshow("cropped",cv2.imread(Cropped_loc))

####### IMAGE AND STRING  #######
	config = ('-l eng --oem 1 --psm 3')
	# pytessercat
	text = pytesseract.image_to_string(Cropped_loc, config=config)
	print(text)


####### INFO FROM STRING #######
	s = 0
	x = 0
	k = 0
	text = text.replace(" ", "" )#Removing spaces
	lines = text.split('\n')
	lines = [line for line in lines if line.strip()]
	str1 = ""
	text = str1.join(lines)
	#print (line)
     
	check_length_of_string = len(text)
	print(text)
	if check_length_of_string >= 10:
		for k in range(len(text)):
			if(text[0].isalpha() and text[1].isalpha and text[2].isdigit and text[3].isdigit and text[4].isalpha and text[5].isdigit and text[6].isdigit and text[7].isdigit and text[8].isdigit):
				if (ord(text[s])> 64 and ord(text[s]) < 91):
					s = x
				else:
					x = x + 1
	
				state = text[x] + text[x+1]
				district = text[x] + text [x+1] + text [x+2] + text[x+3]
				unique_num = text[x+4:]
			else:
				print('Incorrect segmentation or Wrong format')
				sys.exit()
	elif (check_length_of_string != 10 and check_length_of_string != 9):
		print('Incorrect segmentation or Wrong format')
		sys.exit()
			
	elif check_length_of_string == 9:
		for k in range(len(text)):
			if(text[0].isalpha() and text[1].isalpha and text[2].isdigit and text[3].isdigit and text[4].isalpha and text[5].isdigit and text[6].isdigit and text[7].isdigit and text[8].isdigit):
				if (ord(text[s])> 64 and ord(text[s]) < 91):
					s = x
				else:
					x = x + 1
	
				state = text[x] + text[x+1]
				district = text[x] + text [x+1] + text [x+2] + text[x+3]
				unique_num = text[x+4:]
			else:
				print('Incorrect segmentation or Wrong format')
				sys.exit()
	elif (check_length_of_string != 10 and check_length_of_string != 9):
		print('Incorrect segmentation or Wrong format')
		sys.exit()
			
				 
	
####### CALLING FUNCTION TO CHECK IF THE STATE FORMATE IS VALID #######	
	check_state = fun_state(state);
	print (check_state)

####### CALLING FUNCTION TO CHECK IF THE NUMBER IS VALID #######
	check_if_valid = fun_valid(district)
	print (check_if_valid)

####### STORING DATA #######

	data = {'Date_Time': [time.asctime(time.localtime(time.time()))],'Vehicle_number': [text], 'State' : [check_state], 'Valid/Invalid' : [check_if_valid], 'Unique_code' : [unique_num]}
	df = pd.DataFrame(data, columns = ['Date_Time', 'Vehicle_number', 'State', 'Valid/Invalid', 'Unique_code' ])
	df.to_csv('Dataset_VehicleNo.csv')
main()


