from raw_control import Rune
import cv2
import sys
import signal
import numpy as np
from time import sleep
from math import ceil
r = Rune()
cap = cv2.VideoCapture(0)


def signal_handler(signal, frame):
    cap.release()
    cv2.destroyAllWindows()
    r.kill()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def segmentBlocks(hsv):
    h = hsv[0:480,0:640,0]
    # print(h.shape)
    #a = [[]]
    a = np.zeros((10,10))
    for i in range(10):
        for j in range(10):
            segh = hsv[48*i:48*i+48,64*j:64*j+64,0]
            # segs = hsv[48*i:48*i+48,64*j:64*j+64,1]
            segb = hsv[48*i:48*i+48,64*j:64*j+64,2]

            seg_avg = np.average(segh)
            segb_avg = np.average(segb)
            a[i,j] = (1 if seg_avg > 10 and seg_avg < 30 and segb_avg > 70 else 0)
        #a.append([])
    #print(len(a), len(a[0]))
    return a

def getAverages(arr, horizontal, vertical):
    avgs = []
    width = len(arr[0])-1
    height = len(arr[:,0])-1
    print(width, height)
    for j in range(horizontal):
        for i in range(vertical):
            avgs.append(
                np.average(arr[
                    ceil(i*height/vertical):ceil((i+1)*height/vertical), 
                    ceil(j*width/horizontal):ceil((j+1)*width/horizontal)]))
            #avgs.append(arr[int(i*height/vertical):int((i+1)*height/vertical0,int(j*width/horizontal):int((j+1)*width/horizontal]))
    print(avgs)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    a = segmentBlocks(hsv)
    l1, l2, l3, r1, r2, r3 = getAverages(a,2,3)
    break
    #print(a.shape)
    left = a[:,0:5]
    right = a[:,5:9]
    left_avg = [np.average(left[0:3])]
    right_avg = [np.average(right)]
    r.setThrottle(.3)
    print(int(left_avg>.7), int(right_avg>.7))
    
    #if left_avg > .7 and right_avg < .7:
    #    r.midLeft()
    #elif left_avg < .7 and right_avg > .7:
    #    r.midRight()
    #else:
    #    r.setAngle(0)
    #
    #if left_avg < .7 and right_avg < .7:
    #    r.setThrottle(0)#kill()
    #    #r.reverse()
    #    #r.leanRight()
    #    #r.setThrottle(.3)
    #    #r.setThrottle(0)
    #    #r.setThrottle(.3)
    #    #sleep(.2)
    #    #r.reverse()
    #else:
    #    r.setThrottle(.3)
