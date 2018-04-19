#import pygame
#from pygame import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_q, K_r
from raw_control import Rune
from time import sleep
from getch import _Getch

r = Rune()
getch = _Getch()
#pygame.init()
#pygame.display.set_mode([256,256])
#pygame.event.pump()

while True:
        sleep(.01)
        key = getch()
        print(key)
        if key == 'a':
                r.leanLeft()
        if key == 'e':
                r.leanRight()
        if key == ',':
                r.accelerate()
        if key == 'o':
                r.decelerate()
        if key == 'r':
                r.reverse()
        if key == 't':
            r.setThrottle(.5)
            sleep(.1)
            r.setThrottle(0)
            #r.setAngle(1)
            #r.setThrottle(.3)
        if key == '0':
                r.kill()
        if key in ['1','2','3','4','5','6','7','8','9']:
                throttle = int(key)/10.0
                print(throttle)
                r.setThrottle(throttle)
        if key == 'q':
                break
        #keys = pygame.key.get_pressed()
        #if keys[K_LEFT]:
        #       r.leanLeft()
        #       print('left')
        #if keys[K_RIGHT]:
        #       r.leanRight()
        #       print('right')
        #if keys[K_UP]:
        #       r.accelerate()
        #       print('up')
        #if keys[K_DOWN]:
        #       r.decelerate()
        #       print('down')
        #if keys[K_0]:
        #       r.kill()
        #       print('zero')
        #if sum(keys[K_1:K_9+1])>0:
        #       print(keys[K_1:K_9])
        #       thrust = .1
        #       for i in range(9):
        #               thrust += .1
        #               if keys[K_1 + i] == 1:
        #                       break
        #       if thrust == 1:
        #               thrust = 0
        #       r.setThrust(thrust)
        #if keys[K_r]:
        #       r.reverse()
        #if keys[K_q]:
        #       break
        #pygame.event.pump()

r.kill()
