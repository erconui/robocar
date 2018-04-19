import cv2
import numpy as np
import sys
import signal
from object_sensor import OpticFlowControl
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
    r.leanLeft()
    #r.setAngle(-.5)
    #sleep(.2)
    #r.setAngle(1)
    #sleep(.1)
    #r.setAngle(0)
    #sleep(.1)

def turnRight():
    print('r-turn')
    #r.setAngle(-1)
    r.leanLeft()
    r.leanLeft()
    #sleep(.4)
    #r.setAngle(0)
    #sleep(.1)

def leftCenter():
    print('l-center')
    #r.setAngle(.5)
    r.leanRight()
    #sleep(.2)
    #r.setAngle(-1)
    #sleep(.1)
    #r.setAngle(0)
    #sleep(.1)

def turnLeft():
    print('l-turn')
    #r.setAngle(1)
    r.leanRight()
    r.leanRight()
    #sleep(1)
    #r.setAngle(0)
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
        angle = r.angle * 180/np.pi
        left_orig, right_orig = np.linalg.norm(ofc.l_avg), np.linalg.norm(ofc.r_avg)
        if r.angle < 0:
            right = right_orig - left_orig*r.angle/1
            left = left_orig + left_orig*r.angle/1
        else:
            left = left_orig + right_orig*r.angle/1
            right = right_orig - right_orig*r.angle/1
        #left = left + left*r.angle/1 + right*r.angle/1
        #right = right - right*r.angle/1 - left*r.angle/1
        #left, right = left_orig/abs(angle*10), right_orig/abs(angle*10)
        if abs(angle) < 1:
            left, right = left_orig, right_orig
        print("%d\t%d\t\t%d\t\t%d\t%d" % (left_orig, right_orig, angle, left, right))
        if left < 150 and right < 150:
            if left * .9 > right:
                print('l-right')
                for i in range(2):
                    r.leanLeft()
            elif right * .9 > left:
                print('l-left')
                for i in range(2):
                    r.leanRight()
            else:
                r.setAngle(0)
        else:
            if left * .9 > right:
                print('t-right')#turnLeft()
                for i in range(5):
                    r.leanLeft()
            elif right * .9 > left:
                print('t-left')#turnRight()
                for i in range(5):
                    r.leanRight()
            else:
                r.setAngle(0)
        if (left+right)/2 > 700:
            r.reverse()
            r.setThrottle(1)
            sleep(.3)
            #r.setThrottle(.3)
            r.reverse()
        #if left*.9 > right:
        #    left_count += 1
        #else:
        #    left_count = 0
        #if right*.9 > left:
        #    right_count += 1
        #else:
        #    right_count = 0

        #if center > 220 and left_count == right_count:
        #    kill_count += 1
        #    if kill_count > 2:
        #        print('kill')
        #        r.kill()
        #        break
        #elif center > 120 and left_count - 1 > right_count:
        #    turnRight()
        #    left_count = 0
        #    right_count = 0
        #elif center > 120 and right_count - 1 > left_count:
        #    turnLeft()
        #    right_count = 0
        #    left_count = 0
        #else:
        #    kill_count = 0
        #    if left*.8 > right:
        #        if left_count > 2:
        #            leftCenter()
        #    elif right*.8 > left:
        #        if right_count > 2:
        #            rightCenter()
        #    else:
        #        r.setAngle(0)
        #out.write(img)
        # img = ofc.annotate(img)
        ret, img = cam.read()

cam.release()
out.release()
cv2.destroyAllWindows()
