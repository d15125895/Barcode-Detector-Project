import cv2
import pyzbar.pyzbar as pyzbar
import matplotlib.pyplot as plt

img = cv2.imread('../Images/qrcode.jpg')

plt.imshow(img)

decoded = pyzbar.decode(img)

print(decoded, '\n')

for d in decoded:
    print('Data : ', d.data.decode('utf-8'))
    print('Type : ', d.type)
    
    cv2.rectangle(img, (d.rect[0], d.rect[1]), (d.rect[0] + d.rect[2], d.rect[1] + d.rect[3]), (255, 0, 0), 2)
    
    
plt.title('QR code detection')
plt.imshow(img)
plt.show()