#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys

CLASSES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_Classes')
if CLASSES_PATH not in sys.path:
  sys.path.insert(0, CLASSES_PATH)

from CL_GPIO import CL_GPIO
from CL_PortExpander import CL_PortExpander
from CL_MusicBox import CL_MusicBox
# from CL_WiiMote import CL_WiiMote
from CL_RFID import CL_RFID
from CL_NFC import CL_NFC

import signal


# *************** RFID init *************************
# Create an object of the class MFRC522
##import MFRC522Edit


class MyToolBox:
    b_PE    = True
    b_print = True
    b_RFID_select = True
    Sektor_ID = 8 # for RFID reading and writing
    chartnum = 1
    
    continue_reading = True
    
    def __init__(self,_programname=""):
        # Welcome message
        print(f"Welcome to <{_programname}>") 
        self.GPIO = CL_GPIO()
        self.PE = CL_PortExpander()
        self.MusicBox = CL_MusicBox()
        # self.WiiMote = CL_WiiMote()
        self.RFID = CL_RFID()
        self.NFC = CL_NFC()
        
        # Hook the SIGINT
        signal.signal(signal.SIGINT, self.end_read)
        
    def init(self):
        if self.b_PE:
            self.PE    = CL_PortExpander()
            self.PE.Blink_all_lights(0.5,3)
            
    def terminate(self):
        self.continue_reading = False
        self.GPIO.cleanup()
        
    # Capture SIGINT for cleanup when the script is aborted
    def end_read(self, signal,frame):
        print("Ctrl+C captured, ending read.")
        self.terminate()
    
    def init_sayhello(self):
        self.PE.Blink_all_lights(1)
        self.GPIO.set_output(self.GPIO.LED, 1)

    def check_update_new_slide(self):
        status = False
        #check for new layer / game
        if self.b_RFID_select == True:
            (status,TagType) = self.NFC.MFRC522_Request(self.NFC.PICC_REQIDL)

            ## If a card is found
            if status == self.NFC.MI_OK:
                (status,uid) = self.RFID.MFRC522_Anticoll()
                if status == self.NFC.MI_OK:    
                    #print("UID : " + str(uid))
                    answer = self.RFID.MFRC522_SelectTag(uid)
                    #print("SelectTag : " + str(answer))
                    BackData = self.RFID.MFRC522_Read(self.Sektor_ID)
                    #print("Card detected")
                    self.MusicBox.chartnum= self.NFC.NFC_get_ID()
    ##                print("NewTag : " + str(chartnum))
    ##                sleep(1)
                    status = True                
        else:
            in_data = self.PE.get_byte()
            if (in_data == 3):
                while  (in_data == 3):
                    self.MusicBox.chartnum = self.PE.read_BarCode()            
                    if self.b_print>0:
                        print("button byte: "+str(in_data)+"  ;   Chartnumber"+str(self.MusicBox.chartnum))
                    in_data = self.PE.get_byte()
            
                status = True
                        
        
        if status:
            #refresh game folder / playlist
            status = self.MusicBox.refresh_PlayList(self.MusicBox.chartnum)
            if status == True:
                self.PE.Blink_all_lights(1,1)


    def check_song_button_press(self):
        #check for song selection
        if self.b_PE == True:
            (songnum,b_buttonPressed) = self.PE.get_activ_bit()
        else:
            (songnum,b_buttonPressed) = self.RFID.Read_ID()
            if songnum>-1:
                songnum -= 1
        return (songnum,b_buttonPressed)
    
    def control_Lights(self):
        # switch lights according to song number
        if self.b_PE == True:
            #print("Music_is_playing = "+str(self.Music.is_playing()))
            if self.MusicBox.is_playing():
    ##            self.PE.set_bit(7-self.Music.songnum,1)
                self.PE.set_bit(self.MusicBox.songnum,1)
            else:
                self.PE.all_lights_off()
                
    def update_Volume(self): 
        # Volume Control
        if self.GPIO.get_input(self.GPIO.PIN_Volume_Up):
            # print("Volume plus")
            self.MusicBox.volume_plus()        

        if self.GPIO.get_input(self.GPIO.PIN_Volume_Down):
            # print("Volume minus")
            self.MusicBox.volume_minus()
    
    def check_app_termination(self):   
        print("Abort")
        self.GPIO.cleanup()

        print("End")
            