import pyzbar.pyzbar as pyzbar
import cv2

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
  
  # Read frame by frame 
  ret, img = cap.read()

  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  decoded = pyzbar.decode(gray)

  for d in decoded: 
    # These are used to store the location of detected barcode or QR code
    x, y, w, h = d.rect

    # Based on the above variables, draw the rectangle shape covering the detected barcode or QR code
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Get the information and type of the detected barcode or QR code
    Data = d.data.decode("utf-8")
    Type = d.type

    print(Data + ' [' + Type + ']')

    # Show the above Data and Type information on the top of the rectangle shape
    text = Data + ' [' + Type + ']'

    # putText function
    cv2.putText(img, text, (x, y-10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 1)

  cv2.imshow('img', img)

  key = cv2.waitKey(1)

  # Press 'q' to quit
  if key == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
