import cv2
import numpy as np
import sys
import signal
from optical_controller import OpticFlowControl
from raw_control import Rune

#allow for a clean kill
def signal_handler(signal, frame):
    r.kill()
    cam.release()
    out.release()
    cv2.destroyAllWindows()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

    ofc = OpticFlowControl(480, 640)
    r = Rune()
    r.setThrottle(.5)
    ret, img = cam.read()
    while True:
        ofc.calc_optic_flow(img)
        left, center, right = np.linalg.norm(ofc.l_avg), np.linalg.norm(ofc.c_avg), np.linalg.norm(ofc.r_avg)
        if left - 5 > right:
            r.setAngle(-1)
            sleep(.1)
            r.setAngle(1)
            sleep(.05)
            r.setAngle(0)
        if right - 5 > left:
            r.setAngle(1)
        if center > 10:
            r.kill()
            break
        out.write(img)
        # img = ofc.annotate(img)
        ret, img = cam.read()

cam.release()
out.release()
cv2.destroyAllWindows()
