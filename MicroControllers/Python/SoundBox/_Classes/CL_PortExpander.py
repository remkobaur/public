#!/usr/bin/env python
# -*- coding: utf8 -*-

class CL_PortExpander:
##  import RPi.GPIO as GPIO
  import os
  import smbus
  import time
  from time import sleep

  adress = 0x20 # I2C adress of port expander
  bankA_Cfg = 0x00 #inputs
  bankB_Cfg = 0x01 #outputs
  bankA_RW  = 0x14 #inputs
  bankB_RW  = 0x13 #outputs

  LEDs     = bankA_RW
  Switches = bankB_RW

  def __init__(self):
    self.extIO = None
    last_error = None

    # Most Raspberry Pi boards use /dev/i2c-1; older boards may use bus 0.
    for bus in (1, 0):
      try:
        self.extIO = self.smbus.SMBus(bus)
        break
      except FileNotFoundError as err:
        last_error = err

    if self.extIO is None:
      raise FileNotFoundError(
        "No I2C bus device found (/dev/i2c-1 or /dev/i2c-0). "
        "Enable I2C in raspi-config and reboot: 'sudo raspi-config' -> Interface Options -> I2C."
      ) from last_error

    try:
      self.extIO.write_byte_data(self.adress,self.bankA_Cfg,0x00) # Bank A all outputs
      self.extIO.write_byte_data(self.adress,self.bankB_Cfg,0xFF) # Bank B all inputs
    except OSError as err:
      raise OSError(
        "I2C device did not acknowledge at address 0x%02X. "
        "Check wiring/power and confirm address with 'sudo i2cdetect -y 1'." % self.adress
      ) from err

  def get_byte(self):
    #because of inverted bits
    self.in_data = 255-self.extIO.read_byte_data(self.adress,self.Switches)
##    print "{0:b}".format(self.in_data)
    return self.in_data

  def set_byte(self):
    self.extIO.write_byte_data(self.adress,self.LEDs,self.out_data)
    return

  def in2out(self):
    self.get_byte()
    self.out_data = self.in_data
    self.set_byte()


  def get_bit(self,ID):
##    self.get_all_inputs()
    self.get_byte()
    return ( self.in_data and (0x01<<(ID)) )

  def set_bit(self,num,val):
    if num<0:
      #print("Songnum = "+str(num))
      return

    if val == 1:                                                                                                               ##        out_data = ( out_data|(0x01<<(num)) )  # set LED num and keep others
        self.out_data = ( (0x01<<(num)) )    #  set only LED num and switch off all others
    else:
        self.out_data = ( self.out_data& ~(0x01<<(num)) )
    self.set_byte()

  def get_activ_bit(self):
    self.get_byte()
    mask = 0x01
    for ID in range(0,7):
      if (((mask<<ID) & self.in_data)):
        #print (mask<<ID),"   ",in_data
        return (ID,True)
    return (-1,False)

  def all_lights_out(self):
    self.out_data = 0X00
    self.set_byte()

  def all_lights_on(self):
    self.out_data = 0XFF
    self.set_byte()

  def all_lights_off(self):
    self.out_data = 0X00
    self.set_byte()

  def Blink_all_lights(self,dur,repeat = 1):
    for _ in range(repeat):
        self.all_lights_on()
        self.sleep(dur)
        self.all_lights_off()
        self.sleep(dur)
