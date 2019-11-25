## Project - Barcode Detector

## D15125895 FAISAL ALGAHTANI​
## D17123466 SEUNGKI JEONG
## D15125709 ABDULAZIZ ALJABRI 


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
##  1. OpenCV
##      - OpenCV is most used for the project in order to implement entire work
##  2. Pyzbar
##      - Pyzbar is the core library for the project to handle information of a barcode or QR code
##  3. Numpy
##      - Numpy is used to deal with the coordinates of polygon 
##  4. Webbrowser
##      -  Webbrowser is the additional library that is used to figure out web page
#################################################################################################################################
import cv2                              
import pyzbar.pyzbar as pyzbar          
import numpy as np                      
import webbrowser as web                 

#################################################################################################################################
## Step 2. Definition function cleaning a frame from video capture function
##  1. Gray scale 
##      - Gray scale is most used to improve recognition by reducing complexity than other colour spaces.
##  2. Gaussian Blur
##      - Gaussian is used to blur image or to reduce noise.
#################################################################################################################################
def Cleaning(frame):

    # Converting the colour space of the frame to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Applying Gaussian filter 
    gaussian = cv2.GaussianBlur(gray, (3, 3), 0)

    # Returning the cleaned frame
    return gaussian

#################################################################################################################################
## Step 3. Definition function decoding the prepared frame
##  1. Pyzbar.decode 
##      - This is the core function of the core library pyzbar and used to decode barcode and QR code.
##      - The decoded object has the useful information of data, type, and location for barcode and QR code being detected.
#################################################################################################################################
def Decoding(gaussian):

    # Decoding the object extracted from barcode and QR code within a frame
    decodes = pyzbar.decode(frame)

    # Returning the decoded object
    return decodes

#################################################################################################################################
## Step 4. Definition function drawing a bounding box around a barcode or QR code
##  1. Decode.polygon
##      - The polygon of decode function is used to obtain 4 vertices for barcode and QR code being detected.
##  2. Numpy.array
##      - The numpy.array is used to make the coordinates into an array of shape having 2D.
##  3. Convex Hull
##      - ConvexHull is used to fit convex boundary around 4 vertices of barcode and QR code being detected.
##      - However, it is still required to be connected.
##  4. Polylines
##      - Polylines function of OpenCV is used to draw lines connecting the convex hull without parts broken.
#################################################################################################################################
def Drawing(decodes, frame):

    # Looping to use an object by object
    for decode in decodes:

        # Getting the coordinates of vertices from information for polygon of the decoded object
        coordinates = decode.polygon

        # Converting the coordinates to array format with int32
        points = np.array(coordinates, np.int32)

        # Making the coordinates like a contour but it is still required to connect
        hull = cv2.convexHull(points)
        
        # Connecting the coordinates with closing lines
        cv2.polylines(frame, [hull], True, (0, 255, 0), 3)

#################################################################################################################################
## Step 5. Definition function showing information of a barcode or QR code
##  1. Decode.data
##      - This is used to get data for barcode and QR code being detected.
##      - For example, data can be the barcode numbers for detection of barcode or the web site address for detection of QR code.
##      - In addition, data should be decoded into UTF-8 format due to an error that the data cannot be concatenated string to byte.
##  2. Decode.type
##      - This is used to obtain a kind of type
##      - For example, type can be EAN13, Code 39, Code 128, and so on for barcode or QRCODE for QR code.
##  3. Decode.rect
##      - This is used to get the location of the most left and upper side vertex.
##  4. PutText
##      - PutText function of OpenCV is used to put a text in a frame
##      - In this case, the text notifying data and type of barcode and QR code being detected can be placed.
#################################################################################################################################
def Texting(decodes, frame):

    data = []
    type = []

    # Looping to use an object by object
    for decode in decodes:

        # Storing the data from information of the decoded object
        data = decode.data.decode('ascii')

        # Storing the type from information of the decoded object
        type = decode.type

        text = data + ' [' + type + ']'

        print(data + ' [' + type + ']')

        # Obtaining the location of the most left and upper side vertex
        x, y, _, _ = decode.rect

        # Putting the text at the coordinate of the vertex 
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)
    
    return data, type

#################################################################################################################################
## Step 6. Definition function implementing additional works
##  1. Exit 
##  2. Webbrowser.open
##      - This is used to open a web site based on the address from the data of decoded object.
##  3. Imwrite
##      - Imwrite function of OpenCV is used to save the frame.
#################################################################################################################################
def WorkingAdditional(option, data, type, frame):

    exit = False

    # Press 'q' to exit
    if option == ord('q'):

        print('Closing Detector')
        exit = True
    
    # Press 'o' to open a web site and to exit
    elif option == ord('o') and type == 'QRCODE':

        # Opening a web site
        web.open(data)
        print('Opening a Web Site')
        print('Closing Detector')
        exit = True

    # Press 'w' to take a screen shot and to save as png file and to exit
    elif option == ord('w'):

        if type == 'QRCODE':
            image_title = 'QR Code'
        else:
            image_title = 'Barcode'
        
        # Saving the frame as a png file
        cv2.imwrite(image_title + '.png', frame)

        print('Taking a Screen Shot')
        print('Closing Detector')
        exit = True

    return exit


#############################################################################################################################
## Step 7. Integration of all functions
##  1. Waitkey
##      - Waitkey function of OpenCV is used to get a value from user input.
#############################################################################################################################
def Barcode_Detector(frame):

    # Cleaning
    gaussian = Cleaning(frame)

    # Decoding
    decodes = Decoding(gaussian)

    # Drawing
    Drawing(decodes, frame)

    # Texting
    data, type = Texting(decodes, frame)

    # User input
    option = cv2.waitKey(1)

    # Additional job
    commend = WorkingAdditional(option, data, type, frame)

    return commend

#############################################################################################################################
## Step 8. Build
##  1. Videocapture
##      - VideoCapture function of OpenCV is used to capture a video frame by frame.
##  2. Videocapture.set
##      - This is used to adjust size of screen.
##  3. Videocapture.isOpened
##      - This is used to know whether video capturing has been initialized or not.
##      - It returns true if video capturing has been initialized already.
##  4. Imshow
##      - Imshow function of OpenCV is used to show the frame.
##  5. Videocapture.release
##      - This is used to close video capturing.
##  6. Destroyallwindows
##      - DestroyAllWindows function of OpenCV is used to destroy all windows created.
#############################################################################################################################
# Capturing a video frame by frame
cap = cv2.VideoCapture(0)

# Adjusting screen size
cap.set(3, 600)
cap.set(4, 400)

# Looping to make detection in real time
while(cap.isOpened()):

    # Reading a frame by frame
    frame = cap.read()[1]

    # Implementing detection and returning True or False to break the loop 
    commend = Barcode_Detector(frame)

    # Showing the frame
    cv2.imshow('Barcode Detector', frame)

    if commend == True:
        break

# Releasing a video capturing
cap.release()
# Destroying all windows created
cv2.destroyAllWindows()