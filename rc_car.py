import numpy as np
import pygame
from pygame.locals import *
import paramiko
import socket

TURN_RIGHT = K_LEFT
TURN_LEFT  = K_RIGHT
ACCELERATE = K_UP
DECELERATE = K_DOWN

ssh_cmd = "cd donkeycar/donkeycar/parts; "
ssh_cmd += "/home/pi/.virtualenvs/dk/bin/python -c 'from actuator import PCA9685, PWMSteering, PWMThrottle;"
ssh_cmd += "cs = PCA9685(0); s = PWMSteering(cs); ct = PCA9685(1); t = PWMThrottle(ct);"

class RC_CAR:
  def __init__(self):
    self.angle = 0
    self.thrust = 0
    self.quit = False

  def send(self):
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server_address = ("192.168.0.30", 80)
      s.connect(server_address)
      s.sendall(("%f:%f"%(self.angle, self.thrust)).encode())

  def getKey(self):
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    # print(keys)
    # print(keys[TURN_LEFT], keys[TURN_RIGHT], keys[ACCELERATE], keys[DECELERATE])
    if keys[TURN_RIGHT]:
      self.angle += .01
      self.angle = min(self.angle, .73)
      print("t", self.angle)
    elif keys[TURN_LEFT]:
      self.angle -= .01
      self.angle = max(self.angle, -.73)

    if keys[ACCELERATE]:
      self.thrust -= .001
      self.thrust = max(self.thrust, -1)
    elif keys[DECELERATE]:
      self.thrust += .001
      self.thrust = min(self.thrust, 1)
    if keys[K_ESCAPE]:
        self.quit = True
    if keys[K_0]:
        self.thrust = 0
        self.angle = 0

  def run(self):
      print(ssh_cmd)
      pygame.init()
      pygame.display.set_mode((100,100))
      quit = False
      angle_old = self.angle
      thrust_old = self.thrust
      ssh = paramiko.SSHClient()
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh.connect("192.168.0.30", username="pi", password="Vamp1re")
      while not quit:
          quit = self.quit
          # quit = pygame.key.get_pressed()[K_ESCAPE]
          self.getKey()
          # print(self.angle, self.thrust)
          # if self.thrust != thrust_old:
          if self.angle != angle_old or self.thrust != thrust_old:
              # print('send angle')
              # ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(ssh_cmd + "s.run(%f); t.run(%f)'" % (self.angle, self.thrust))
              # print(ssh_stdout.read(), ssh_stderr.read())
              # print(ssh_stdout)
              self.send()
          angle_old = self.angle
          thrust_old = self.thrust
          #TODO send steering command
          #TODO send thrust command
      #TODO kill thrust and zero out steering

a = RC_CAR()
a.run()
