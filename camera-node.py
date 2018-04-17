import socket
import numpy as np
from cStringIO import StringI0
import cv2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 81))
s.listen(5)
print("test")
while 1:
    print("accept")
    (clientsocket, address) = s.accept()
    allData = ''
    while True:
        data = connection.recv(16)
        if not data:
            break
        allData += data
    image = np.load(StringIO(allData))
    cv2.imshow('test', image)
    connection.close()
print('done')
