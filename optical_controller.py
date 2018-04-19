import cv2
import numpy as np
import sys
import signal
from flow_test import OpticFlowControl
from raw_control import Rune
from time import sleep

r = Rune()
cam = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

#allow for a clean kill
def signal_handler(signal, frame):
    r.kill()
    cam.release()
    out.release()
    cv2.destroyAllWindows()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def rightCenter():
    print('r-center')
    r.setAngle(-1)
    sleep(.2)
    #r.setAngle(1)
    #sleep(.1)
    #r.setAngle(0)
    #sleep(.1)

def turnRight():
    print('r-turn')
    r.setAngle(-1)
    sleep(.4)
    r.setAngle(0)
    #sleep(.1)

def leftCenter():
    print('l-center')
    r.setAngle(1)
    sleep(.2)
    #r.setAngle(-1)
    #sleep(.1)
    #r.setAngle(0)
    #sleep(.1)

def turnLeft():
    print('l-turn')
    r.setAngle(1)
    sleep(1)
    r.setAngle(0)
    #sleep(.1)

if __name__ == '__main__':

    ofc = OpticFlowControl(480, 640)
    ret, img = cam.read()
    #r.setAngle(0)
    r.setThrottle(.3)
    kill_count = 0
    left_count = 0
    right_count = 0
    #r.kill()
    while True:
        ofc.calc_optic_flow(img)
        left, center, right = np.linalg.norm(ofc.l_avg), np.linalg.norm(ofc.c_avg), np.linalg.norm(ofc.r_avg)
        print("%d\t%d\t%d\t-\t%d\t%d\t%d\t\t%f" % (left, center, right, left_count, kill_count, right_count, r.angle))
        if left*.9 > right:
            left_count += 1
        else:
            left_count = 0
        if right*.9 > left:
            right_count += 1
        else:
            right_count = 0

        if center > 220 and left_count == right_count:
            kill_count += 1
            if kill_count > 2:
                print('kill')
                r.kill()
                break
        elif center > 120 and left_count - 1 > right_count:
            turnRight()
            left_count = 0
            right_count = 0
        elif center > 120 and right_count - 1 > left_count:
            turnLeft()
            right_count = 0
            left_count = 0
        else:
            kill_count = 0
            if left*.8 > right:
                if left_count > 2:
                    leftCenter()
            elif right*.8 > left:
                if right_count > 2:
                    rightCenter()
            else:
                r.setAngle(0)
        #out.write(img)
        # img = ofc.annotate(img)
        ret, img = cam.read()

cam.release()
out.release()
cv2.destroyAllWindows()
