#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
from time import sleep

CLASSES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','_Classes')
if CLASSES_PATH not in sys.path:
    sys.path.insert(0, CLASSES_PATH)

import RPi.GPIO as GPIO
import MFRC522Edit
import signal

GPIO.setwarnings(False)

#=============================================================
#======================= initialize ==========================
#=============================================================

authcode = [114, 97, 115, 112, 98, 101, 114, 114, 121] # die ersten 9 Ziffern sind der Authentifizierungscode

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
    
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
##MIFAREReader = MFRC522.MFRC522()
MIFAREReader = MFRC522Edit.MFRC522Edit()


#=============================================================
#================== function definition ======================
#=============================================================

def Read_Write_RFID(key,Number):
    global MIFAREReader
    global continue_reading

    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            BackData = MIFAREReader.MFRC522_Read(8)            
            NewData =[]
            for x in range(0,16):
                NewData.append(Number)
            print("old data: "+str(BackData))
            MIFAREReader.MFRC522_Write(8,NewData)    
            BackData = MIFAREReader.MFRC522_Read(8)
            print("Data is written: "+str(BackData))            
##            continue_reading = False
##            GPIO.cleanup()
    MIFAREReader.MFRC522_StopCrypto1()
            
    

def print_Tag_Status(b_detect,uid,backData,b_authent):
    if b_detect == True:
        print("---------------")
        print("Card detected")
        # Print UID
        #if len(uid[])==4:
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
        if b_authent == True:
            blockAddr = 8
            if len(backData) == 16:
                print "Sector "+str(blockAddr)+" "+str(backData)
            print("Authentication okay")
        else:
            print("Authentication error")
            
#=============================================================
#================== main program =============================
#=============================================================
def main_function():
    global MIFAREReader
    global continue_reading
    # This is the default key for authentication
    key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
    Number = int(raw_input("Set ID for next Token:")) 
    Read_Write_RFID(key,Number)        
    sleep(1)


#=============================================================
#================= execute main loop =========================
#=============================================================
# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

try:
    while continue_reading ==True:
        main_function()

except KeyboardInterrupt:
    print("Abbruch")
    GPIO.cleanup()

print("Ende")
