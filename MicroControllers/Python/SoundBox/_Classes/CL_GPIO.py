#!/usr/bin/env python
# -*- coding: utf8 -*-

class CL_GPIO:
  import RPi.GPIO as GPIO
  from time import sleep

  def __init__(self):
    #--- Define PINS [7,11,12,13,15,16,18]
    self.LED  = 7 # status LED: programm is running
    self.BarCode = [12,16,18,22] # GPIO pint for reading 4bit metal barcode
    self.PIN_Volume_Up   = 13
    self.PIN_Volume_Down = 11
    self.T_blink = 0.25

    GPIO =self.GPIO
    GPIO.setmode(GPIO.BOARD)  # RPi.GPIO Layout verwenden (wie Pin-Nummern)
    GPIO.setwarnings(False)   # channel in use warnings off
    GPIO.setup(self.LED,        GPIO.OUT)
    GPIO.setup(self.BarCode[0], GPIO.IN)
    GPIO.setup(self.BarCode[1], GPIO.IN)
    GPIO.setup(self.BarCode[2], GPIO.IN)
    GPIO.setup(self.BarCode[3], GPIO.IN)
    GPIO.setup(self.PIN_Volume_Up, GPIO.IN)
    GPIO.setup(self.PIN_Volume_Down, GPIO.IN)

  def set_output(self,ID,Bit):
    if Bit > 0:
      self.GPIO.output(ID,self.GPIO.HIGH) # set bit
    else:
      self.GPIO.output(ID,self.GPIO.LOW) # clear bit

  def get_input(self,ID):
    return self.GPIO.input(ID)

  def set_Led(self,Bit):
    self.set_output(self.LED,Bit)

  def read_BarCode(self):
      self.Byte = 1
      B0 = self.get_input(self.BarCode[0])
      B1 = self.get_input(self.BarCode[1])
      B2 = self.get_input(self.BarCode[2])
      B3 = self.get_input(self.BarCode[3])
      self.Byte = 15- (B3*8+B2*4+B1*2+B0)
##      print Byte
##      sleep(1)
      return (self.Byte)


  def alert(self,BlinkNum):
      for f in range(0,BlinkNum):
          self.set_Led(0)
          self.sleep(self.T_blink)
          self.set_Led(1)
          self.sleep(self.T_blink)

  def cleanup(self):
    self.GPIO.cleanup()
