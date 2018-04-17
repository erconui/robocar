import cv2
import numpy as np
import sys
import signal
from optical_controller import OpticFlowControl
from raw_control import Rune

#allow for a clean kill
def signal_handler(signal, frame):
    r.kill()
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    ofc = OpticFlowControl(480, 640)
    r = Rune()
    r.setThrottle(.3)
