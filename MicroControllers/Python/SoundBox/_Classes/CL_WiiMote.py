#!/usr/bin/env python
# -*- coding: utf8 -*-

class CL_WiiMote:
  import cwiid
  import time
  #import i2c



## --- constructor ---
  def __init__(self):
    self.song_num = 0
    self.wii_LED = 0
    self.wm = None
    self.wii_MAC = "00:22:AA:8C:20:BF" # sudo hcitool scan

##  def wii_init():
##    global wm
##    global song_num
##    global wii_LED
##    song_num = 0
##    wii_LED  = 0
##    wm = None

  def wii_isconnected(self):
    if (not self.wm):
        return (False)
    else:
        return (True)

  def wii_connect(self):
    if(self.wii_isconnected()):
##        if (wii_LED == 1):
##            wii_LED = 0
##            wm.led = 0
##        else:
##            wii_LED = 1
##            wm.led = 1
        return

    #connecting to the Wiimote. This allows several attempts
    # as first few often fail.
    print 'Press 1+2 on your Wiimote now...'
    self.wm = None

    try:
        self.wm=self.cwiid.Wiimote()
    except RuntimeError:
        print "Error opening wiimote connection"
##        quit()


    i=2
    while not self.wm:
      try:
        self.wm=self.cwiid.Wiimote()
      except RuntimeError:
        if (i>3):
          #quit()
          break
        print "Error opening wiimote connection"
        print "attempt " + str(i)
        i +=1
    if (not self.wm):
        return

  #set Wiimote to report button presses and accelerometer state
    self.wm.rpt_mode = self.cwiid.RPT_BTN | self.cwiid.RPT_ACC

    #turn on led to show connected
    self.wm.led = 1

    print 'connected'
    return

  def wii_get_button(self):
    global wm
    status = self.wii_isconnected()
    if (self.wii_isconnected()==False):
        #print "abort  wii_get_button"
        return

    buttons = self.wm.state['buttons']
    switcher ={
        0: "?",
        1: "2",
        2: "1",
        4: "B",
        8: "A",
        16: "-",
        32: "?",
        64: "?",
        128: "home",
        256: "left",
        512: "right",
        1024: "down",
        2048: "up",
        4096: "+"
    }
    button = switcher.get(buttons, "?")
##    print buttons
##    print button
    return button
