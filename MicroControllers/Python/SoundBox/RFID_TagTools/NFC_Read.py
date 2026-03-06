#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from time import sleep

CLASSES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','_Classes')
if CLASSES_PATH not in sys.path:
    sys.path.insert(0, CLASSES_PATH)

from CL_NFC import CL_NFC

RFID  = CL_NFC()
Programname = "NFC_Read"

#=============================================================
#================== init program =============================
#=============================================================
    
def init():
   
    RFID  = CL_NFC()
    RFID.MAX_LEN=16

#=============================================================
#================== main program =============================
#=============================================================

def main():

    Sektor_ID = 8

    while(True):
        # Scan for cards    
        (status,TagType) = RFID.MFRC522_Request(RFID.PICC_REQIDL)

        ## If a card is found
        if status == RFID.MI_OK:
            print("Card detected")

            (status,uid) = RFID.MFRC522_Anticoll()
            print("UID : " + str(uid))
            answer = RFID.MFRC522_SelectTag(uid)
            print("SelectTag : " + str(answer))
            BackData = RFID.MFRC522_Read(Sektor_ID)
            print("Data : " + str(BackData))
            break
        else:            
            sleep(1)

##    RFID.NFC_get_ID(Number)
    ID = RFID.NFC_get_ID()
    print("ID " + str(ID))

    BackData = RFID.MFRC522_Read(Sektor_ID)
    print("Data : " + str(BackData))    
    print("---------------------")
               
#=============================================================
#================= execute main loop =========================
#=============================================================
# Welcome message
print("Welcome to the "+Programname) 
print("Press Ctrl-C to stop.")

try:
    init()
    while True:
        main()     
except KeyboardInterrupt:
    print("Abbruch")

print("Ende")

