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


cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
start_time = time.time()
while(True):
	ret, frame = cap.read()
	if ret==True:
		out.write(frame)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	cv2.imshow('frame', gray)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
out.release()
cv2.destroyAllWindows()
