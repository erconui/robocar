import cv2
import numpy as np
import sys
import signal
from wallTracker import OpticFlowControl
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
    cv2.destroyAllWindows()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':

    ofc = OpticFlowControl(480, 640)
    ret, img = cam.read()
    r.setAngle(0)
    r.setThrottle(.3)
    left_count = 0
    right_count = 0
    while True:
        ofc.calc_optic_flow(img)
        angle = r.angle * 180/np.pi
        left_orig, right_orig = np.linalg.norm(ofc.l_avg), np.linalg.norm(ofc.r_avg)
        center = np.linalg.norm(ofc.c_avg)
        down = np.linalg.norm(ofc.d_avg)
        left, right = left_orig, right_orig
        print("%d\t%d\t%d" % (left, down, right))
        
        if down > 300:
            r.reverse()
            r.kill()
            break
        if left > 30 or right > 30:
            if left *.7 > right:
                left_count += 1
                if left_count > 1:
                    print('right')
                    r.sharpRight()
                    sleep(.2)
                    r.sharpLeft()
                    sleep(.3)
                    r.setAngle(0)
                    sleep(.1)
            if right * .7> left:
                right_count += 1
                if right_count > 1:
                    print('left')
                    r.sharpLeft()
                    sleep(.2)
                    r.sharpRight()
                    sleep(.3)
                    r.setAngle(0)
                    sleep(.1)
        ret, img = cam.read()

cam.release()
cv2.destroyAllWindows()
