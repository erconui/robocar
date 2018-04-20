from raw_control import Rune
import cv2
import sys
import signal

def signal_handler(signal, frame):
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def segmentBlocks(hsv):
    h = hsv[0:480,0:640,0]
    # print(h.shape)
    a = [[]]
    for i in range(10):
        for j in range(10):
            segh = hsv[48*i:48*i+48,64*j:64*j+64,0]
            # segs = hsv[48*i:48*i+48,64*j:64*j+64,1]
            segb = hsv[48*i:48*i+48,64*j:64*j+64,2]

            seg_avg = np.average(segh)
            segb_avg = np.average(segb)
            a[i].append(1 if seg_avg > 35 and seg_avg < 70 and segb_avg > 70 else 0)
            # a[i].append(1 if seg_avg > 90 else 0)
            # a[i].append(int(seg_avg))
        a.append([])
    return a


r = Rune()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BRG2HSV)
    a = segmentBlocks(hsv)

    print(:,1)
