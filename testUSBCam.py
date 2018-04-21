import numpy as np
import cv2
import time
#from getch import _Getch
import sys
import signal

def signal_handler(signal, frame):
        print('you pressed ctrl+c')
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def segmentBlocks(hsv):
    h = hsv[0:480,0:640,0]
    print(h.shape)
    a = [[]]
    for i in range(10):
        for j in range(10):
            segh = hsv[48*i:48*i+48,64*j:64*j+64,0]
            segs = hsv[48*i:48*i+48,64*j:64*j+64,1]
            segb = hsv[48*i:48*i+48,64*j:64*j+64,2]

            seg_avg = np.average(segh)
            segb_avg = np.average(segb)
            #a[i].append(1 if seg_avg > 5 and seg_avg < 30 and segb_avg > 70 else 0)
            # a[i].append(1 if seg_avg > 90 else 0)
            a[i].append(int(seg_avg))
        a.append([])
    for line in a:
        print(line)

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
start_time = time.time()
while(True):
    ret, frame = cap.read()
    if ret==True:
        out.write(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # lower = np.array([40, 10, 0])
    # upper = np.array([50, 255, 255])
    # lower = np.array([150,50,50])
    # upper = np.array([180,255,255])

    # mask = cv2.inRange(hsv, lower, upper)
    # res = cv2.bitwise_and(frame, frame, mask=mask)
    # hue = hsv[0]
    segmentBlocks(hsv)
    # break
    # print(hue)
    cv2.imshow('frame', frame)
    # cv2.imshow('mask', mask)
    # cv2.imshow('res', res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
