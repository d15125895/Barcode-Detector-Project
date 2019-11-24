# Project - Barcode Detector
# D17123466
# Seungki Jeong

#################################################################################################################################
## Introduction
##
##  The purpose of this project called 'Barcode Detector' is to scan a barcode or QR code in an image or video.
## In addition, the 'Barcode Detector' has additional functions notifying the data and type of a barcode or QR code being 
## detected and opening then a corresponding web page from the extracted data of a QR code. 
#################################################################################################################################

#################################################################################################################################
## The entire steps of processing for the project
##
##  Step 1. Import of the necessary libraries 
##  Step 2. Definition function cleaning a frame from video capture function
##  Step 3. Definition function decoding the prepared frame
##  Step 4. Definition function drawing a bounding box around a barcode or QR code
##  Step 5. Definition function texting information of a barcode or QR code
##  Step 6. Definition function implementing additional work
##  Step 7. Integration of all the defined functions
##  Step 8. Build 
## 
#################################################################################################################################

#################################################################################################################################
## Step 1. Import of the necessary libraries
##  - OpenCV
##  - Pyzbar
##  - Numpy
##  - Webbrowser
#################################################################################################################################

import cv2                              ## OpenCV is most used for the project in order to implement entire work
import pyzbar.pyzbar as pyzbar          ## Pyzbar is the core library for the project to handle information of a barcode or QR code
import numpy as np                      ## Numpy is used to deal with the coordinates of polygon 
import webbrowser as web                ## Webbrowser is the additional library that is used to figure out web page

#################################################################################################################################
## Step 2. Definition function cleaning a frame from video capture function
#################################################################################################################################

def Cleaning(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    gaussian = cv2.GaussianBlur(gray, (3, 3), 0)

    return gaussian

#################################################################################################################################
## Step 3. Definition function decoding the prepared frame
#################################################################################################################################

def Decoding(gaussian):

    decodes = pyzbar.decode(frame)

    return decodes

#################################################################################################################################
## Step 4. Definition function drawing a bounding box around a barcode or QR code
#################################################################################################################################

def Drawing(decodes, frame):

    for decode in decodes:

        coordinates = decode.polygon

        points = np.array(coordinates, np.int32)

        hull = cv2.convexHull(points)
        
        cv2.polylines(frame, [points], True, (0, 255, 0), 3)

        # cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)


#################################################################################################################################
## Step 5. Definition function showing information of a barcode or QR code
#################################################################################################################################

def Texting(decodes, frame):

    data = []
    type = []

    for decode in decodes:

        data = decode.data.decode('utf-8')

        type = decode.type

        text = data + ' [' + type + ']'

        x, y, _, _ = decode.rect

        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)
    
    return data, type

#################################################################################################################################
## Step 6. Definition function implementing additional work
#################################################################################################################################

def WorkingAddtional(option, data, type, frame):

    exit = False

    if option == ord('q'):

        exit = True

    elif option == ord('o') and type == 'QRCODE':

        web.open(data)

    elif option == ord('w'):

        if type == 'QRCODE':
            image_title = 'QR Code'
        else:
            image_title = 'Barcode'
        
        cv2.imwrite(image_title + '.png', frame)

    return exit


#############################################################################################################################
## Step 7. Integration of all functions
#############################################################################################################################

def Barcode_Detector(frame):

    gaussian = Cleaning(frame)

    decodes = Decoding(gaussian)

    Drawing(decodes, frame)

    data, type = Texting(decodes, frame)

    option = cv2.waitKey(1)

    commend = WorkingAddtional(option, data, type, frame)

    return commend

#############################################################################################################################
## Step 8. Build
#############################################################################################################################

cap = cv2.VideoCapture(0)

cap.set(3, 600)
cap.set(4, 400)

while(cap.isOpened()):

    frame = cap.read()[1]

    commend = Barcode_Detector(frame)

    cv2.imshow('Barcode Detector', frame)

    if commend == True:
        break


cap.release()
cv2.destroyAllWindows()