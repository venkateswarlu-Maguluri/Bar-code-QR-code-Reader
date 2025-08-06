#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install pyzbar


# In[ ]:





# In[2]:


pip install opencv-python


# In[3]:


import cv2
from pyzbar import pyzbar

import winsound  # For beep sound on Windows

# Set to store already scanned codes
scanned_codes = set()
import time 
# Dictionary to track last scan time for each code
scanned_codes = {}

# Delay before same code can be scanned again (in seconds)
REPEAT_DELAY = 3


# In[4]:


def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        current_time = time.time()

        # Check if this code was scanned recently
        last_scanned = scanned_codes.get(barcode_info, 0)
        if current_time - last_scanned >= REPEAT_DELAY:
            scanned_codes[barcode_info] = current_time  # update scan time

            # Draw green rectangle and show text
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 1.0, (255, 0, 0), 2)

            # Save to file
            with open("barcode_result.txt", mode='a') as file:
                file.write("Recognized Code: " + barcode_info + "\n")

            # Beep sound
            winsound.Beep(1000, 200)

        else:
            # Optional: show that this code was already scanned recently
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, "Scanned recently", (x + 6, y - 6), font, 0.6, (100, 100, 100), 1)

    return frame


# In[ ]:


def main():
    #1
    open("barcode_result.txt", 'w')

    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    #2
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    #3
    camera.release()
    cv2.destroyAllWindows()
#4
if __name__ == '__main__':
    main()


# In[ ]:





# In[ ]:




