from actuator import PCA9685, PWMSteering, PWMThrottle
import socket

cs = PCA9685(0)
ct = PCA9685(1)

s = PWMSteering(cs)
t = PWMThrottle(ct)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 80))
s.listen(5)
# conn, addr = s.accept()
print("test")
s_val = 0
t_val = 0
while 1:
    print("accept")
    (connection, address) = s.accept()
    while True:
        data = connection.recv(16)
        print(data)
        if not data:
            break
    s.run(s_val)
    t.run(t_val)
