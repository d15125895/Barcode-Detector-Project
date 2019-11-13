import pyzbar.pyzbar as pyzbar
import cv2 
import webbrowser as web

cap = cv2.VideoCapture(0)

while(cap.isOpened()):

    # Read frame by frame
    ret, frame = cap.read()

    decoded = pyzbar.decode(frame)

    for d in decoded:

        # These are used to store the location of detected barcode or QR code
        x, y, width, height = d.rect

        # Based on the above variables, draw the rectangle shape covering the detected barcode or QR code
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)

        # Get the information and type of the detected barcode or QR code 
        Data = d.data.decode('utf-8')
        Type = d.type

        print(Data + ' [' + Type + ']')

        # Show the above Data and Type information on the top of the rectangle shape
        text = Data + ' [' + Type + ']'

        # putText function
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    cv2.imshow('Barcode Detection', frame)

    key = cv2.waitKey(1)

    # Press 'q' to quit
    if key == ord('q'):
        break

    # Press 'o' to open the website based on the above Data variable
    if key == ord('o') and Type == 'QRCODE':
        web.open(Data)
        break

cap.release()
cv2.destroyAllWindows()