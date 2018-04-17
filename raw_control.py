import Adafruit_PCA9685

# pwmSteering = Adafruit_PCA9685.PCA9685()
#
# servo_min = 150
# servo_max = 600

# def set_servo_pulse(channel, pulse)
#     pulse_length = 1000000
#     pulse_length //= 60
#     pulse_length //= 4096
#     pulse *= 1000
#     pulse //= pulse_length
#     pwm.set_pwm(channel, 0, pulse)
#
# pwm.set_pwm_freq(60)
#
# for i in range(10)
#     pwm.set_pwm(0, 0, servo_min)
#     time.sleep(1)
#     pwm.set_pwm(0, 0, servo_max)
#     time.sleep(1)
#
# pwm.set_pwm(0, 0, 0)

class Rune:
    def __init__(self):
        self.left_pulse = 250
        self.right_pulse = 520
        self.left = -1
        self.right = 1

        self.min_throttle = -1
        self.max_throttle = 1
        self.min_pulse = 460
        self.zero_pulse = 350
        self.max_pulse = 290
        self.forward = True

        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)

    # def map_range(self, x, Y_)

    def getPulse(self, x, x_min, x_max, y_min, y_max):
        x_range = x_max - x_min
        y_range = y_max - y_min
        xy_ratio = x_range/y_range
        y = ((x-x_min)/xy_ratio + y_min)//1
        return int(y)

    def setAngle(self, angle):
        self.angle = min(max(angle, -1), 1)
        self.pwm.set_pwm(
            0, 0, self.getPulse(
                self.angle,
                self.left_angle, self.right_angle,
                self.left_pulse, self.right_pulse))

    def setThrottle(self, throttle):
        self.throttle = min(max(abs(throttle), 0), 1)
        if self.forward:
            throttle = -1 * self.throttle
            pulse = self.getPulse(
                throttle, self.min_throttle, 0, self.min_pulse, self.zero_pulse)
        else:
            throttle = self.throttle
            pulse = self.getPulse(
                throttle, 0, self.max_throttle, self.zero_pulse, self.max_pulse)
        self.pwm.set_pwm(1, 0, pulse)

    def leanLeft(self):
        self.setAngle(self.angle - .1)

    def leanRight(self):
        self.setAngle(self.angle + .1)

    def reverse(self):
        self.forward = not self.forward
        self.setThrottle(throttle)
        self.setThrottle(0)
        self.setThrottle(throttle)

    def accelerate(self):
        if abs(self.throttle) < .3:
            self.setThrottle(0)
        else:
            self.setThrottle(self.throttle + .1)

    def decelerate(self):
        if abs(self.throttle) < .3:
            self.setThrottle(0)
        else:
            self.setThrottle(self.throttle - .1)
