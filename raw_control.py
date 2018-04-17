import Adafruit_PCA9685

pwmSteering = Adafruit_PCA9685.PCA9685()

servo_min = 150
servo_max = 600

def set_servo_pulse(channel, pulse)
    pulse_length = 1000000
    pulse_length //= 60
    pulse_length //= 4096
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

pwm.set_pwm_freq(60)

for i in range(10)
    pwm.set_pwm(0, 0, servo_min)
    time.sleep(1)
    pwm.set_pwm(0, 0, servo_max)
    time.sleep(1)

pwm.set_pwm(0, 0, 0)
