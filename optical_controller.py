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
        print("%d\t%d\t%d" %(np.linalg.norm(ofc.l_avg), np.linalg.norm(ofc.c_avg), np.linalg.norm(ofc.r_avg)))
        out.write(img)
        # img = ofc.annotate(img)
        ret, img = cam.read()
