#! /usr/bin/python
# -*- coding: utf-8 -*-

Programname = "SoundBox RFID"

import os
import sys
from time import sleep

CLASSES_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_Classes'))
if CLASSES_PATH not in sys.path:
    sys.path.insert(0, CLASSES_PATH)

import MyToolBox as MyToolBox
TB = MyToolBox.MyToolBox(Programname)


#=============================================================
#=================== init method =============================
#=============================================================
    
def init():
    
    TB.b_PE    = True # Use PortExpander
    TB.b_print = True # Print all infos
    TB.b_RFID_select = True # Use RFID-Scanner   
    
    # Define Music Path
    projectPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
    TB.MusicBox.Path =  os.path.join(projectPath,'Files','Sounds')
    # TB.MusicBox.Path =  os.path.join(projectPath,'Files','Sounds_All')
    TB.MusicBox.b_print = TB.b_print
    TB.MusicBox.import_jsonConfigFile(os.path.join(TB.MusicBox.Path,'Config.json')) # load specifc config json
    
    TB.MusicBox.chartnum = 1 # set default chartnum to 1 (can be changed by RFID-Tag) 
    TB.MusicBox.refresh_PlayList(1)
    TB.init()
      
    # init hardware
    TB.MusicBox.set_volume(80)    
    TB.GPIO.set_Led(1)
    
    
#=============================================================
#================== main method (LOOP) =======================
#=============================================================

def loop():

    TB.check_update_new_slide()

    #check for song selection
    (songnum,b_buttonPressed) = TB.check_song_button_press()
        
    if b_buttonPressed:
        #play / stop audio file
        TB.MusicBox.stop_music()
        TB.MusicBox.play_song(songnum)
        sleep(0.2)           
    
    # Control lights w.r.t. song number
    TB.control_Lights()
    
    # Volume Control by buttons
    TB.update_Volume()
        
#=============================================================
#================= execute main loop =========================
#=============================================================


try:
    init()
    while TB.continue_reading ==True:
        loop()     
except KeyboardInterrupt:
    print("ABORT due to KeyboardInterrupt.")
    TB.terminate()  
except Exception as e:
    print(f"ABORT due to Exception: \n --> {e}")
    TB.terminate()
