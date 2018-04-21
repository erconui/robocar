import numpy as np
import cv2
import time
#from getch import _Getch
import sys
import signal

def signal_handler(signal, frame):
    print('you pressed ctrl+c')
    cap.release()
    #out.release()
    cv2.destroyAllWindows()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


cap = cv2.VideoCapture(0)
lower_blue = np.array([100,50,50])
upper_blue = np.array([130,255,255])
#cap.set(3,320)
#cap.set(4,240)
#fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
#out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
start_time = time.time()
while(True):
    ret, frame = cap.read()
    #if ret==True:
    #   out.write(frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    print(hsv[0])
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res',res) 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
#out.release()
cv2.destroyAllWindows()
